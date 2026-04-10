"""Tests for ListingGenerator."""

from __future__ import annotations

from listing_generator import ListingGenerator


def test_generate_all_platforms():
    gen = ListingGenerator()
    item = {
        "title": "Test Widget",
        "brand": "Acme",
        "model": "X1",
        "category": "Electronics",
        "condition": "Good",
        "features": ["Works"],
        "suggested_price": 25.0,
        "photo_path": "photos/x.jpg",
    }
    listings = gen.generate(item)
    assert set(listings.keys()) == {"ebay", "facebook", "mercari", "offerup"}
    assert listings["ebay"]["platform"] == "ebay"
    assert listings["ebay"]["price"] == 25.0


def test_title_truncation():
    gen = ListingGenerator()
    item = {
        "title": "A" * 100,
        "brand": "B" * 20,
        "condition": "Good",
        "suggested_price": 1.0,
    }
    title = gen._create_title(item, max_chars=40)
    assert len(title) <= 40
