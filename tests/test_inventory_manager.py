"""Tests for InventoryManager."""

from __future__ import annotations

import csv

from inventory_manager import InventoryManager


def test_add_item_writes_csv_and_json(tmp_path):
    inv = InventoryManager(data_dir=tmp_path)
    item = {
        "title": "Thing",
        "brand": "Brand",
        "category": "General",
        "condition": "Good",
        "suggested_price": 10.0,
        "photo_path": "p.jpg",
    }
    listings = {"ebay": {"title": "t"}}
    sku = inv.add_item(item, listings)
    assert item["sku"] == sku
    csv_path = tmp_path / "inventory.csv"
    assert csv_path.exists()
    rows = list(csv.DictReader(csv_path.open(newline="", encoding="utf-8")))
    assert any(r["sku"] == sku for r in rows)
    assert (tmp_path / f"{sku}.json").exists()


def test_get_analytics_empty(tmp_path):
    inv = InventoryManager(data_dir=tmp_path)
    a = inv.get_analytics()
    assert a["total_items"] == 0
    assert a["unsold_items"] == 0
