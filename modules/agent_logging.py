"""
Central logging setup for the Storage Flipper Agent.

All modules should use: logger = logging.getLogger("flipper.<module>")
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def configure_logging(
    log_dir: Optional[Path] = None,
    *,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    Configure the ``flipper`` logger tree: file (logs/agent.log) + console.

    Safe to call multiple times; handlers are attached only once.
    """
    log_dir = log_dir or (_project_root() / "logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "agent.log"

    log = logging.getLogger("flipper")
    if log.handlers:
        return log

    log.setLevel(logging.DEBUG)
    log.propagate = False

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(file_level)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(console_level)
    ch.setFormatter(fmt)

    log.addHandler(fh)
    log.addHandler(ch)
    return log
