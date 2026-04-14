"""Tests for retry_with_backoff."""

from __future__ import annotations

import pytest

from modules.retry_utils import retry_with_backoff


def test_retry_succeeds_first_try():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        return "ok"

    assert retry_with_backoff(fn, max_attempts=3) == "ok"
    assert calls["n"] == 1


def test_retry_then_succeeds():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] < 2:
            raise TimeoutError("transient")
        return "ok"

    assert retry_with_backoff(fn, max_attempts=3, base_delay_s=0.01, max_delay_s=0.05) == "ok"
    assert calls["n"] == 2


def test_retry_exhausted():
    def fn():
        raise RuntimeError("always")

    with pytest.raises(RuntimeError, match="always"):
        retry_with_backoff(fn, max_attempts=2, base_delay_s=0.01, max_delay_s=0.05)
