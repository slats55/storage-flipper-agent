"""Tests for InventoryManager."""

from __future__ import annotations

import csv

from inventory_manager import INVENTORY_FIELDS, InventoryManager


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
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == INVENTORY_FIELDS
        rows = list(reader)
    assert any(r["sku"] == sku for r in rows)
    assert (tmp_path / f"{sku}.json").exists()


def test_get_analytics_empty(tmp_path):
    inv = InventoryManager(data_dir=tmp_path)
    a = inv.get_analytics()
    assert a["total_items"] == 0
    assert a["unsold_items"] == 0


def test_mark_sold_updates_row(tmp_path):
    inv = InventoryManager(data_dir=tmp_path)
    sku = inv.add_item({"title": "A", "suggested_price": 20.0}, {})
    inv.mark_sold(sku, "ebay", 18.5)
    with (tmp_path / "inventory.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    row = next(r for r in rows if r["sku"] == sku)
    assert row["sold"] == "Yes"
    assert row["sold_platform"] == "ebay"


def test_mark_sold_missing_sku_no_crash(tmp_path, capsys):
    inv = InventoryManager(data_dir=tmp_path)
    inv.add_item({"title": "A"}, {})
    inv.mark_sold("20991231-ZZZZ", "ebay", 1)
    captured = capsys.readouterr()
    assert "not found" in captured.out.lower() or "SKU" in captured.out
