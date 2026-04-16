"""
Inventory Manager Module
Tracks items in Google Sheets or local database
"""

from __future__ import annotations

import csv
import json
import logging
import random
import string
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("flipper.inventory_manager")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Canonical CSV column order (must match header and every row)
INVENTORY_FIELDS: List[str] = [
    "sku",
    "title",
    "brand",
    "category",
    "condition",
    "cost",
    "suggested_price",
    "listed_price",
    "ebay_listed",
    "facebook_listed",
    "mercari_listed",
    "offerup_listed",
    "sold",
    "sold_platform",
    "sold_price",
    "sold_date",
    "date_acquired",
    "date_listed",
    "days_on_market",
    "photo_path",
    "notes",
]


class InventoryManager:
    """Manage inventory tracking and analytics"""

    def __init__(self, data_dir=None):
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = _PROJECT_ROOT / "data" / "inventory"

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.inventory_file = self.data_dir / "inventory.csv"
        logger.debug("Inventory data_dir=%s", self.data_dir)
        self._init_inventory_file()

    def _init_inventory_file(self) -> None:
        """Initialize inventory CSV if it doesn't exist"""
        if not self.inventory_file.exists():
            with open(self.inventory_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=INVENTORY_FIELDS)
                writer.writeheader()

    def generate_sku(self) -> str:
        """Generate unique SKU"""
        date_part = datetime.now().strftime("%Y%m%d")
        random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"{date_part}-{random_part}"

    def _row_from_item(self, sku: str, item_data: Dict[str, Any], listings: Optional[dict]) -> Dict[str, Any]:
        """Build a full CSV row dict with stable keys."""
        return {
            "sku": sku,
            "title": item_data.get("title", ""),
            "brand": item_data.get("brand", ""),
            "category": item_data.get("category", ""),
            "condition": item_data.get("condition", ""),
            "cost": item_data.get("cost", 0),
            "suggested_price": item_data.get("suggested_price", 0),
            "listed_price": item_data.get("suggested_price", 0),
            "ebay_listed": "Yes" if listings and "ebay" in listings else "No",
            "facebook_listed": "Yes" if listings and "facebook" in listings else "No",
            "mercari_listed": "Yes" if listings and "mercari" in listings else "No",
            "offerup_listed": "Yes" if listings and "offerup" in listings else "No",
            "sold": "No",
            "sold_platform": "",
            "sold_price": 0,
            "sold_date": "",
            "date_acquired": datetime.now().strftime("%Y-%m-%d"),
            "date_listed": datetime.now().strftime("%Y-%m-%d"),
            "days_on_market": 0,
            "photo_path": item_data.get("photo_path", ""),
            "notes": item_data.get("notes", ""),
        }

    def add_item(self, item_data, listings=None):
        """Add item to inventory"""
        sku = self.generate_sku()
        item_data["sku"] = sku

        record = self._row_from_item(sku, item_data, listings)

        with open(self.inventory_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=INVENTORY_FIELDS)
            writer.writerow(record)

        json_file = self.data_dir / f"{sku}.json"
        detailed_record = {**item_data, "listings": listings, "inventory_record": record}

        with open(json_file, "w", encoding="utf-8") as jf:
            json.dump(detailed_record, jf, indent=2)

        return sku

    def mark_sold(self, sku, platform, sold_price):
        """Mark an item as sold"""
        with open(self.inventory_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            items = list(reader)

        if not items:
            logger.warning("mark_sold: inventory empty, sku=%s", sku)
            print(f"   ⚠ No inventory rows; could not mark {sku}")
            return

        updated = False
        for item in items:
            if item.get("sku") == sku:
                item["sold"] = "Yes"
                item["sold_platform"] = platform
                item["sold_price"] = sold_price
                item["sold_date"] = datetime.now().strftime("%Y-%m-%d")
                updated = True
                break

        if not updated:
            logger.warning("mark_sold: sku not found: %s", sku)
            print(f"   ⚠ SKU not found: {sku}")
            return

        with open(self.inventory_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=INVENTORY_FIELDS)
            writer.writeheader()
            writer.writerows(items)

        logger.info("Marked sold sku=%s platform=%s price=%s", sku, platform, sold_price)
        print(f"   ✅ Marked {sku} as sold on {platform} for ${sold_price}")

    def get_analytics(self):
        """Get inventory analytics"""
        with open(self.inventory_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            items = list(reader)

        total_items = len(items)
        sold_items = sum(1 for item in items if item.get("sold") == "Yes")
        unsold_items = total_items - sold_items

        total_value = sum(
            float(item.get("suggested_price") or 0) for item in items if item.get("sold") == "No"
        )
        total_revenue = sum(
            float(item.get("sold_price") or 0) for item in items if item.get("sold") == "Yes"
        )

        return {
            "total_items": total_items,
            "sold_items": sold_items,
            "unsold_items": unsold_items,
            "total_inventory_value": total_value,
            "total_revenue": total_revenue,
            "sell_through_rate": (sold_items / total_items * 100) if total_items > 0 else 0,
        }
