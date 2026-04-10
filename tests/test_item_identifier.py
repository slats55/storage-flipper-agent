"""Tests for ItemIdentifier."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from item_identifier import ItemIdentifier


def test_identify_missing_photo(tmp_path):
    ident = ItemIdentifier()
    with pytest.raises(FileNotFoundError):
        ident.identify(tmp_path / "nope.jpg")


def test_identify_uses_hermes_mock(tmp_path, monkeypatch):
    photo = tmp_path / "item.jpg"
    photo.write_bytes(b"\xff\xd8\xff")  # minimal placeholder

    def fake_run(*args, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = "{}"
        m.stderr = ""
        return m

    monkeypatch.setattr(subprocess, "run", fake_run)
    ident = ItemIdentifier()
    data = ident.identify(photo)
    assert data["photo_path"] == str(photo)
    assert "title" in data
