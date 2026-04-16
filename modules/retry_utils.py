"""
Retry helpers with exponential backoff and optional jitter.
"""

from __future__ import annotations

import random
import time
from typing import Callable, Optional, Tuple, Type, TypeVar

T = TypeVar("T")


def retry_with_backoff(
    fn: Callable[[], T],
    *,
    max_attempts: int = 3,
    base_delay_s: float = 1.0,
    max_delay_s: float = 30.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> T:
    """
    Call ``fn`` until it succeeds or ``max_attempts`` is exhausted.

    Delay after failure k: min(base * 2^k, max_delay) + small jitter.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    last_exc: Optional[BaseException] = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except exceptions as exc:
            last_exc = exc
            if attempt >= max_attempts:
                raise
            delay = min(base_delay_s * (2 ** (attempt - 1)), max_delay_s)
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)
    assert last_exc is not None
    raise last_exc
