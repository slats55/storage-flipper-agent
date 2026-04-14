"""
Item Identifier Module
Uses vision AI to identify items from photos
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from hermes_cli import run_hermes_chat
from retry_utils import retry_with_backoff

logger = logging.getLogger("flipper.item_identifier")


class ItemIdentifier:
    """Identifies items from photos using Hermes vision tools"""

    def __init__(self):
        self.categories = [
            "Electronics",
            "Furniture",
            "Tools",
            "Collectibles",
            "Clothing",
            "Household",
            "Toys",
            "Books",
            "Appliances",
            "Sporting Goods",
            "Jewelry",
            "Art",
            "Musical Instruments",
        ]

    def identify(self, photo_path):
        """
        Analyze photo and extract item information

        Returns dict with:
        - title: Item name/description
        - brand: Brand name if identifiable
        - model: Model number if visible
        - category: Item category
        - condition: Estimated condition
        - features: Notable features
        """
        photo_path = Path(photo_path)
        if not photo_path.exists():
            logger.error("Photo not found: %s", photo_path)
            raise FileNotFoundError(f"Photo not found: {photo_path}")

        logger.info("Analyzing photo: %s", photo_path.name)
        print(f"   Analyzing photo: {photo_path.name}...")

        question = """Identify this item for resale purposes. Provide:
1. Item type and description
2. Brand name (if visible)
3. Model number (if visible)
4. Category (Electronics/Furniture/Tools/etc)
5. Condition (New/Like New/Good/Fair/Poor)
6. Notable features or damage
7. Estimated age/era

Format as JSON."""

        full_query = f"Analyze image {photo_path} and answer: {question}"

        def _run_hermes():
            return run_hermes_chat(full_query, timeout=60)

        try:
            result = retry_with_backoff(
                _run_hermes,
                max_attempts=3,
                base_delay_s=1.0,
                max_delay_s=20.0,
                exceptions=(subprocess.TimeoutExpired,),
            )
            if result.returncode != 0:
                logger.warning(
                    "Hermes vision returned non-zero exit %s stderr=%s",
                    result.returncode,
                    (result.stderr or "").strip()[:500],
                )

            raw_stdout = (result.stdout or "").strip()
            item_data = {
                "photo_path": str(photo_path),
                "title": self._extract_title_from_photo(photo_path.name),
                "brand": "Unknown",
                "model": "",
                "category": "General",
                "condition": "Good",
                "features": [],
                "analyzed_at": datetime.now().isoformat(),
                "raw_analysis": raw_stdout if result.returncode == 0 else "Analysis pending",
            }

            if result.returncode == 0 and raw_stdout:
                parsed = self._parse_vision_response(raw_stdout)
                if parsed:
                    self._merge_vision_into_item(item_data, parsed)
                else:
                    logger.debug("Vision stdout present but no structured JSON parsed")
        except FileNotFoundError:
            logger.warning("Hermes CLI not found; using filename fallback")
            item_data = self._fallback_item_data(photo_path)
        except subprocess.TimeoutExpired as exc:
            logger.warning("Vision analysis timed out after retries: %s", exc)
            item_data = self._fallback_item_data(photo_path)
        except Exception as exc:
            logger.warning("Vision analysis failed: %s", exc, exc_info=True)
            item_data = self._fallback_item_data(photo_path)

        return item_data

    def _merge_vision_into_item(self, item_data: Dict[str, Any], parsed: Dict[str, Any]) -> None:
        """Merge normalized vision fields into ``item_data`` in place."""
        if parsed.get("title"):
            item_data["title"] = str(parsed["title"]).strip()
        if parsed.get("brand") is not None and str(parsed["brand"]).strip():
            item_data["brand"] = str(parsed["brand"]).strip()
        if parsed.get("model") is not None:
            item_data["model"] = str(parsed["model"]).strip()
        if parsed.get("category"):
            cat = str(parsed["category"]).strip()
            if cat:
                item_data["category"] = cat
        if parsed.get("condition"):
            cond = str(parsed["condition"]).strip()
            if cond:
                item_data["condition"] = cond
        if isinstance(parsed.get("features"), list):
            item_data["features"] = [str(f).strip() for f in parsed["features"] if str(f).strip()]
        elif parsed.get("features"):
            item_data["features"] = self._coerce_features(parsed["features"])
        if parsed.get("confidence") is not None:
            try:
                item_data["vision_confidence"] = float(parsed["confidence"])
            except (TypeError, ValueError):
                pass

    def _coerce_features(self, value: Any) -> List[str]:
        """Turn string or other types into a list of feature strings."""
        if isinstance(value, str):
            parts = re.split(r"[\n,;]", value)
            return [p.strip() for p in parts if p.strip()]
        return [str(value).strip()] if str(value).strip() else []

    def _parse_vision_response(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse Hermes vision stdout into a normalized dict.

        Expects JSON (plain or inside a markdown ```json ... ``` fence). Tolerates
        leading/trailing prose by extracting the first balanced JSON object.

        Returns None if no usable object or no meaningful identification fields.
        """
        if not raw_text or not raw_text.strip():
            return None

        candidate = self._extract_json_string(raw_text.strip())
        if candidate is None:
            return None

        try:
            data = json.loads(candidate)
        except json.JSONDecodeError as exc:
            logger.debug("Vision JSON decode failed: %s", exc)
            return None

        if not isinstance(data, dict):
            return None

        normalized = self._normalize_vision_dict(data)
        if not self._vision_parse_has_signal(normalized):
            return None
        return normalized

    def _extract_json_string(self, text: str) -> Optional[str]:
        """Return a JSON object/array substring suitable for ``json.loads``."""
        # Markdown fenced block
        fence = re.search(
            r"```(?:json)?\s*([\s\S]*?)\s*```",
            text,
            re.IGNORECASE,
        )
        if fence:
            inner = fence.group(1).strip()
            if inner:
                text = inner

        text = text.strip()
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError:
            pass

        start = text.find("{")
        if start == -1:
            return None
        end = self._find_matching_brace(text, start)
        if end == -1:
            return None
        snippet = text[start : end + 1]
        try:
            json.loads(snippet)
            return snippet
        except json.JSONDecodeError:
            return None

    @staticmethod
    def _find_matching_brace(text: str, start: int) -> int:
        """Index of closing ``}`` for object starting at ``start``, or -1."""
        depth = 0
        in_string: Optional[str] = None
        escape = False
        for i in range(start, len(text)):
            ch = text[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == in_string:
                    in_string = None
                continue
            if ch in ('"', "'"):
                in_string = ch
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i
        return -1

    def _normalize_vision_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Map common Hermes / API keys to canonical fields."""
        title = (
            _first_str(
                data,
                (
                    "title",
                    "item_title",
                    "name",
                    "item_type",
                    "description",
                    "item_description",
                    "summary",
                ),
            )
            or ""
        )
        brand = _first_str(data, ("brand", "brand_name", "manufacturer", "make")) or ""
        model = _first_str(data, ("model", "model_number", "model_name", "sku_model")) or ""
        category = _first_str(
            data,
            ("category", "item_category", "product_category"),
        ) or ""
        condition = _first_str(
            data,
            ("condition", "estimated_condition", "item_condition"),
        ) or ""

        features_val = None
        for key in ("features", "notable_features", "highlights", "attributes"):
            if key in data and data[key] is not None:
                features_val = data[key]
                break

        conf = _first_scalar(data, ("confidence", "confidence_score", "score"))

        out: Dict[str, Any] = {}
        if title:
            out["title"] = title
        if brand:
            out["brand"] = brand
        if model:
            out["model"] = model
        if category:
            out["category"] = category
        if condition:
            out["condition"] = condition
        if features_val is not None:
            out["features"] = features_val
        if conf is not None:
            out["confidence"] = conf
        return out

    @staticmethod
    def _vision_parse_has_signal(parsed: Dict[str, Any]) -> bool:
        """True if parsed dict has at least one usable identification field."""
        if parsed.get("title") or parsed.get("brand") or parsed.get("model"):
            return True
        if parsed.get("category") or parsed.get("condition"):
            return True
        feats = parsed.get("features")
        if isinstance(feats, list) and any(str(x).strip() for x in feats):
            return True
        if feats and not isinstance(feats, list) and str(feats).strip():
            return True
        return False

    def _fallback_item_data(self, photo_path: Path) -> dict:
        """Minimal item record when vision/Hermes is unavailable."""
        return {
            "photo_path": str(photo_path),
            "title": self._extract_title_from_photo(photo_path.name),
            "brand": "Unknown",
            "model": "",
            "category": "General",
            "condition": "Good",
            "features": [],
            "analyzed_at": datetime.now().isoformat(),
        }

    def _extract_title_from_photo(self, filename):
        """Extract a basic title from filename"""
        title = Path(filename).stem
        title = title.replace("_", " ").replace("-", " ")
        title = " ".join(word.capitalize() for word in title.split())
        return title if title else "Item"

    def batch_identify(self, photos_dir):
        """Identify multiple items from a directory"""
        photos_path = Path(photos_dir)
        photo_files = list(photos_path.glob("*.jpg")) + list(photos_path.glob("*.png"))

        results = []
        for photo in photo_files:
            try:
                item_data = self.identify(photo)
                results.append(item_data)
            except FileNotFoundError:
                raise
            except Exception as exc:
                logger.exception("Error processing %s: %s", photo.name, exc)
                print(f"Error processing {photo.name}: {exc}")

        return results


def _first_str(data: Dict[str, Any], keys: tuple) -> Optional[str]:
    for k in keys:
        v = data.get(k)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return None


def _first_scalar(data: Dict[str, Any], keys: tuple) -> Any:
    for k in keys:
        if k in data and data[k] is not None and data[k] != "":
            return data[k]
    return None
