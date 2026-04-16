"""
Price Researcher Module
Researches market prices across platforms
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

from modules.hermes_cli import run_hermes_chat
from modules.json_extract import extract_json_value_string
from modules.retry_utils import retry_with_backoff

logger = logging.getLogger("flipper.price_researcher")


class PriceResearcher:
    """Research prices on eBay, Facebook Marketplace, etc."""

    def __init__(self):
        self.platforms = ["ebay", "facebook", "mercari", "offerup"]

    def research(self, item_data):
        """
        Research market prices for an item.

        Always returns a pricing dict; on Hermes/network failure uses category fallback
        so batch workflows do not abort.
        """
        title = item_data.get("title", "")
        brand = item_data.get("brand", "")
        category = item_data.get("category", "")

        search_query = f"{brand} {title}".strip()

        logger.info("Price research search_query=%r", search_query)
        print(f"   Searching: '{search_query}'...")

        try:
            pricing_data = self._search_ebay_sold(search_query)
        except Exception as exc:
            logger.exception("Price research unexpected error: %s", exc)
            pricing_data = {"prices": []}

        if pricing_data["prices"]:
            avg_price = sum(pricing_data["prices"]) / len(pricing_data["prices"])
            suggested_price = round(avg_price * 0.85, 2)
        else:
            suggested_price = self._estimate_by_category(category)
            logger.debug("No comps; category fallback price=%s", suggested_price)

        return {
            "suggested_price": suggested_price,
            "price_range": (
                min(pricing_data["prices"]) if pricing_data["prices"] else 0,
                max(pricing_data["prices"]) if pricing_data["prices"] else 0,
            ),
            "comp_count": len(pricing_data["prices"]),
            "ebay_sold_prices": pricing_data["prices"][:5],
            "research_date": datetime.now().isoformat(),
            "search_query": search_query,
        }

    def _search_ebay_sold(self, query):
        """Search eBay sold listings for comparable prices"""

        full_query = (
            f'Search eBay sold listings for "{query}" and return a JSON object with '
            f'sold prices. Use keys like "sold_prices" or "prices" with an array of '
            f"numbers (USD), or a list of objects with a price field."
        )

        def _run_hermes():
            return run_hermes_chat(full_query, timeout=30)

        prices: List[float] = []
        try:
            result = retry_with_backoff(
                _run_hermes,
                max_attempts=3,
                base_delay_s=1.0,
                max_delay_s=15.0,
                exceptions=(subprocess.TimeoutExpired,),
            )
            if result.returncode != 0:
                logger.warning(
                    "Hermes eBay search non-zero exit=%s stderr=%s",
                    result.returncode,
                    (result.stderr or "").strip()[:500],
                )
            raw_stdout = (result.stdout or "").strip()
            if result.returncode == 0 and raw_stdout:
                parsed = self._parse_pricing_response(raw_stdout)
                if parsed:
                    prices = parsed
                    logger.debug("Parsed %s comparable prices from Hermes stdout", len(prices))
                else:
                    logger.debug("eBay stdout present but no structured prices parsed")
        except FileNotFoundError:
            logger.warning("Hermes CLI not found; skipping eBay search")
        except subprocess.TimeoutExpired as exc:
            logger.warning("eBay search timed out after retries: %s", exc)
        except Exception as exc:
            logger.warning("eBay search failed: %s", exc, exc_info=True)

        return {"prices": prices}

    def _parse_pricing_response(self, raw_text: str) -> Optional[List[float]]:
        """
        Parse Hermes stdout into a list of comparable sold prices (floats).

        Accepts JSON object or array (plain or in markdown fence). Normalizes keys such as
        ``sold_prices``, ``prices``, ``comps`` with ``price`` fields, etc.

        Returns None if nothing usable is found.
        """
        if not raw_text or not raw_text.strip():
            return None

        candidate = extract_json_value_string(raw_text.strip())
        if candidate is None:
            return None

        try:
            data = json.loads(candidate)
        except json.JSONDecodeError as exc:
            logger.debug("Pricing JSON decode failed: %s", exc)
            return None

        prices = self._normalize_pricing_data(data)
        if not prices:
            return None
        return prices

    def _normalize_pricing_data(self, data: Any) -> List[float]:
        """Collect positive float prices from dict or list JSON."""
        out: List[float] = []
        if isinstance(data, list):
            out.extend(_floats_from_sequence(data))
        elif isinstance(data, dict):
            for key in (
                "prices",
                "sold_prices",
                "ebay_sold_prices",
                "comparable_prices",
                "comps_prices",
                "recent_sold_prices",
            ):
                val = data.get(key)
                if isinstance(val, list):
                    out.extend(_floats_from_sequence(val))
            comps = data.get("comparables") or data.get("comps") or data.get("sales")
            if isinstance(comps, list):
                for row in comps:
                    if isinstance(row, dict):
                        for pk in ("price", "sold_price", "amount", "sale_price"):
                            if pk in row and row[pk] is not None:
                                p = _to_positive_float(row[pk])
                                if p is not None:
                                    out.append(p)
                                break
                    else:
                        p = _to_positive_float(row)
                        if p is not None:
                            out.append(p)
            pr = data.get("price_range") or data.get("priceRange")
            if isinstance(pr, dict):
                for pk in ("min", "max", "low", "high"):
                    if pk in pr:
                        p = _to_positive_float(pr[pk])
                        if p is not None:
                            out.append(p)
            elif isinstance(pr, (list, tuple)) and len(pr) >= 2:
                for x in pr[:2]:
                    p = _to_positive_float(x)
                    if p is not None:
                        out.append(p)

        # Dedupe preserving order
        seen = set()
        unique: List[float] = []
        for p in out:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        return unique

    def _estimate_by_category(self, category: str) -> float:
        """Fallback pricing estimates by category"""
        estimates = {
            "Electronics": 45.00,
            "Furniture": 75.00,
            "Tools": 30.00,
            "Collectibles": 25.00,
            "Clothing": 15.00,
            "Household": 12.00,
            "Toys": 10.00,
            "Books": 8.00,
            "Appliances": 50.00,
            "Sporting Goods": 35.00,
            "Jewelry": 40.00,
            "Art": 60.00,
            "Musical Instruments": 100.00,
            "General": 20.00,
        }
        return estimates.get(category, 20.00)


def _floats_from_sequence(seq: List[Any]) -> List[float]:
    out: List[float] = []
    for x in seq:
        if isinstance(x, dict):
            for pk in ("price", "sold_price", "amount", "sale_price", "value"):
                if pk in x and x[pk] is not None:
                    p = _to_positive_float(x[pk])
                    if p is not None:
                        out.append(p)
                    break
        else:
            p = _to_positive_float(x)
            if p is not None:
                out.append(p)
    return out


def _to_positive_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        p = float(value)
        return p if p > 0 else None
    s = str(value).strip()
    if not s:
        return None
    s = re.sub(r"[^\d.\-]", "", s.replace(",", ""))
    if not s or s in ("-", ".", "-."):
        return None
    try:
        p = float(s)
        return p if p > 0 else None
    except ValueError:
        return None
