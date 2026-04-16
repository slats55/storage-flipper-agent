"""Smoke tests for logging setup."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from modules.agent_logging import configure_logging


@pytest.fixture(autouse=True)
def reset_flipper_logger():
    """Remove handlers between tests."""
    log = logging.getLogger("flipper")
    log.handlers.clear()
    log.setLevel(logging.DEBUG)
    yield
    log.handlers.clear()


def test_configure_logging_creates_file(tmp_path):
    log_dir = tmp_path / "logs"
    configure_logging(log_dir=log_dir)
    log = logging.getLogger("flipper.tests")
    log.info("hello")
    assert (log_dir / "agent.log").exists()
    text = (log_dir / "agent.log").read_text(encoding="utf-8")
    assert "hello" in text
