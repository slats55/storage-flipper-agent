"""Tests for ItemIdentifier."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import modules.item_identifier as item_identifier_mod
from modules.item_identifier import ItemIdentifier


def test_identify_missing_photo(tmp_path):
    ident = ItemIdentifier()
    with pytest.raises(FileNotFoundError):
        ident.identify(tmp_path / "nope.jpg")


def test_identify_uses_hermes_mock(tmp_path, monkeypatch):
    photo = tmp_path / "item.jpg"
    photo.write_bytes(b"\xff\xd8\xff")

    def fake_run(query, *, timeout):
        m = MagicMock()
        m.returncode = 0
        m.stdout = "{}"
        m.stderr = ""
        return m

    monkeypatch.setattr(item_identifier_mod, "run_hermes_chat", fake_run)
    ident = ItemIdentifier()
    data = ident.identify(photo)
    assert data["photo_path"] == str(photo)
    assert "title" in data


def test_identify_fallback_when_hermes_missing(tmp_path, monkeypatch):
    photo = tmp_path / "my_widget.jpg"
    photo.write_bytes(b"x")

    def boom(*args, **kwargs):
        raise FileNotFoundError("hermes")

    monkeypatch.setattr(item_identifier_mod, "run_hermes_chat", boom)
    ident = ItemIdentifier()
    data = ident.identify(photo)
    assert data["title"] == "My Widget"


def test_parse_vision_plain_json():
    ident = ItemIdentifier()
    raw = json.dumps(
        {
            "title": "Vintage Camera",
            "brand": "Kodak",
            "model": "Instamatic",
            "category": "Electronics",
            "condition": "Good",
            "features": ["lens cap", "strap"],
            "confidence": 0.92,
        }
    )
    out = ident._parse_vision_response(raw)
    assert out is not None
    assert out["title"] == "Vintage Camera"
    assert out["brand"] == "Kodak"
    assert out["model"] == "Instamatic"
    assert out["category"] == "Electronics"
    assert out["condition"] == "Good"
    assert out["features"] == ["lens cap", "strap"]
    assert out["confidence"] == 0.92


def test_parse_vision_markdown_fence():
    ident = ItemIdentifier()
    payload = {"item_title": "Desk Lamp", "manufacturer": "IKEA", "item_category": "Household"}
    raw = f"Here is the analysis:\n```json\n{json.dumps(payload)}\n```\nDone."
    out = ident._parse_vision_response(raw)
    assert out is not None
    assert out["title"] == "Desk Lamp"
    assert out["brand"] == "IKEA"
    assert out["category"] == "Household"


def test_parse_vision_prose_wrapped_object():
    ident = ItemIdentifier()
    inner = '{"description": "Red wagon", "brand": "Radio Flyer", "condition": "Fair"}'
    raw = f"The item appears to be a toy. JSON: {inner} Thanks."
    out = ident._parse_vision_response(raw)
    assert out is not None
    assert out["title"] == "Red wagon"
    assert out["brand"] == "Radio Flyer"
    assert out["condition"] == "Fair"


def test_parse_vision_invalid_returns_none():
    ident = ItemIdentifier()
    assert ident._parse_vision_response("") is None
    assert ident._parse_vision_response("not json") is None
    assert ident._parse_vision_response("[1, 2, 3]") is None


def test_parse_vision_empty_object_returns_none():
    ident = ItemIdentifier()
    assert ident._parse_vision_response("{}") is None


def test_parse_vision_features_string():
    ident = ItemIdentifier()
    raw = json.dumps(
        {"title": "Mug", "features": "chip on handle; dishwasher safe"}
    )
    out = ident._parse_vision_response(raw)
    assert out is not None
    merged = {
        "title": "fallback",
        "brand": "Unknown",
        "model": "",
        "category": "General",
        "condition": "Good",
        "features": [],
    }
    ident._merge_vision_into_item(merged, out)
    assert merged["title"] == "Mug"
    assert len(merged["features"]) == 2


def test_identify_merges_vision_json(tmp_path, monkeypatch):
    photo = tmp_path / "photo.jpg"
    photo.write_bytes(b"x")
    vision = {
        "title": "Canon AE-1",
        "brand": "Canon",
        "model": "AE-1",
        "category": "Electronics",
        "condition": "Like New",
        "features": ["body cap"],
        "confidence": 0.88,
    }

    def fake_run(query, *, timeout):
        m = MagicMock()
        m.returncode = 0
        m.stdout = json.dumps(vision)
        m.stderr = ""
        return m

    monkeypatch.setattr(item_identifier_mod, "run_hermes_chat", fake_run)
    ident = ItemIdentifier()
    data = ident.identify(photo)
    assert data["title"] == "Canon AE-1"
    assert data["brand"] == "Canon"
    assert data["model"] == "AE-1"
    assert data["category"] == "Electronics"
    assert data["condition"] == "Like New"
    assert data["features"] == ["body cap"]
    assert data["vision_confidence"] == pytest.approx(0.88)
    assert json.loads(data["raw_analysis"]) == vision
