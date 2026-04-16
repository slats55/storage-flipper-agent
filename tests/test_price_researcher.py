"""Tests for PriceResearcher."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import modules.price_researcher as price_researcher
from modules.price_researcher import PriceResearcher


def test_research_with_mock_hermes(monkeypatch):
    payload = {"sold_prices": [29.99, 34.99, 27.50, 32.00, 30.00]}

    def fake_run(query, *, timeout):
        m = MagicMock()
        m.returncode = 0
        m.stdout = json.dumps(payload)
        m.stderr = ""
        return m

    monkeypatch.setattr(price_researcher, "run_hermes_chat", fake_run)
    r = PriceResearcher()
    out = r.research({"title": "Camera", "brand": "Kodak", "category": "Electronics"})
    assert "suggested_price" in out
    assert out["comp_count"] == 5
    assert out["search_query"] == "Kodak Camera"


def test_research_fallback_when_hermes_missing(monkeypatch):
    def boom(*args, **kwargs):
        raise FileNotFoundError("no hermes")

    monkeypatch.setattr(price_researcher, "run_hermes_chat", boom)
    r = PriceResearcher()
    out = r.research({"title": "X", "brand": "", "category": "Books"})
    assert out["comp_count"] == 0
    assert out["suggested_price"] == 8.0


def test_parse_pricing_plain_object():
    r = PriceResearcher()
    raw = json.dumps({"prices": [10.0, 20.0, 15.5]})
    out = r._parse_pricing_response(raw)
    assert out == [10.0, 20.0, 15.5]


def test_parse_pricing_array():
    r = PriceResearcher()
    raw = "[12.5, 13.0, 11.25]"
    out = r._parse_pricing_response(raw)
    assert out == [12.5, 13.0, 11.25]


def test_parse_pricing_markdown_fence():
    r = PriceResearcher()
    inner = json.dumps({"comps": [{"price": "$29.99"}, {"sold_price": 34.0}]})
    raw = f"Here:\n```json\n{inner}\n```"
    out = r._parse_pricing_response(raw)
    assert out == [29.99, 34.0]


def test_parse_pricing_invalid_none():
    r = PriceResearcher()
    assert r._parse_pricing_response("") is None
    assert r._parse_pricing_response("not json") is None
