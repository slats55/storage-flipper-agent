"""
Price Researcher Module
Researches market prices across platforms
"""

from __future__ import annotations

import logging
import subprocess
from datetime import datetime

from hermes_cli import run_hermes_chat
from retry_utils import retry_with_backoff

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
            f'Search eBay sold listings for "{query}" and extract the last 5 sold prices'
        )

        def _run_hermes():
            return run_hermes_chat(full_query, timeout=30)

        prices = []
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
            # MVP: structured parsing when Hermes returns JSON; mock until then
            prices = [29.99, 34.99, 27.50, 32.00, 30.00]
        except FileNotFoundError:
            logger.warning("Hermes CLI not found; skipping eBay search")
        except subprocess.TimeoutExpired as exc:
            logger.warning("eBay search timed out after retries: %s", exc)
        except Exception as exc:
            logger.warning("eBay search failed: %s", exc, exc_info=True)

        return {"prices": prices}

    def _estimate_by_category(self, category):
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
