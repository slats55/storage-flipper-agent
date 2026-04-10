"""Tests for ItemIdentifier."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

import hermes_cli
from item_identifier import ItemIdentifier


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

    monkeypatch.setattr(hermes_cli, "run_hermes_chat", fake_run)
    ident = ItemIdentifier()
    data = ident.identify(photo)
    assert data["photo_path"] == str(photo)
    assert "title" in data


def test_identify_fallback_when_hermes_missing(tmp_path, monkeypatch):
    photo = tmp_path / "my_widget.jpg"
    photo.write_bytes(b"x")

    def boom(*args, **kwargs):
        raise FileNotFoundError("hermes")

    monkeypatch.setattr(hermes_cli, "run_hermes_chat", boom)
    ident = ItemIdentifier()
    data = ident.identify(photo)
    assert data["title"] == "My Widget"
