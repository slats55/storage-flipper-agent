"""
Invoke the Hermes CLI for chat/vision workflows.

Centralizes subprocess calls so tests can patch ``run_hermes_chat``.
"""

from __future__ import annotations

import logging
import subprocess
from typing import List

logger = logging.getLogger("flipper.hermes_cli")


def build_hermes_chat_cmd(query: str) -> List[str]:
    """Build argv for ``hermes chat -q <query>``."""
    return ["hermes", "chat", "-q", query]


def run_hermes_chat(query: str, *, timeout: int) -> subprocess.CompletedProcess:
    """Run ``hermes chat`` and return ``CompletedProcess``."""
    cmd = build_hermes_chat_cmd(query)
    logger.debug("hermes cmd=%s timeout=%s", cmd[0:3], timeout)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
