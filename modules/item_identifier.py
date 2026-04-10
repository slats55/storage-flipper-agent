"""
Item Identifier Module
Uses vision AI to identify items from photos
"""

from __future__ import annotations

import logging
import subprocess
from datetime import datetime
from pathlib import Path

from retry_utils import retry_with_backoff

logger = logging.getLogger("flipper.item_identifier")


class ItemIdentifier:
    """Identifies items from photos using Hermes vision tools"""

    def __init__(self):
        self.categories = [
            "Electronics", "Furniture", "Tools", "Collectibles",
            "Clothing", "Household", "Toys", "Books", "Appliances",
            "Sporting Goods", "Jewelry", "Art", "Musical Instruments",
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

        def _run_hermes():
            return subprocess.run(
                [
                    "hermes",
                    "chat",
                    "-q",
                    f"Analyze image {photo_path} and answer: {question}",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

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

            item_data = {
                "photo_path": str(photo_path),
                "title": self._extract_title_from_photo(photo_path.name),
                "brand": "Unknown",
                "model": "",
                "category": "General",
                "condition": "Good",
                "features": [],
                "analyzed_at": datetime.now().isoformat(),
                "raw_analysis": result.stdout if result.returncode == 0 else "Analysis pending",
            }
        except FileNotFoundError:
            logger.exception("Hermes CLI not found; install or add to PATH")
            raise
        except subprocess.TimeoutExpired as exc:
            logger.warning("Vision analysis timed out after retries: %s", exc)
            item_data = self._fallback_item_data(photo_path)
        except Exception as exc:
            logger.warning("Vision analysis failed: %s", exc, exc_info=True)
            item_data = self._fallback_item_data(photo_path)

        return item_data

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
