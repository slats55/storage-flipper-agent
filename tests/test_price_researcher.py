"""Tests for PriceResearcher."""

from __future__ import annotations

from unittest.mock import MagicMock

import price_researcher
from price_researcher import PriceResearcher


def test_research_with_mock_hermes(monkeypatch):
    def fake_run(query, *, timeout):
        m = MagicMock()
        m.returncode = 0
        m.stdout = "ok"
        m.stderr = ""
        return m

    # Patch where used (module already bound ``run_hermes_chat``).
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
