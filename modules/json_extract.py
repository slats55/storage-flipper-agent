"""
Extract JSON object/array substrings from Hermes stdout (fences, prose wrappers).
Shared by vision and pricing parsers.
"""

from __future__ import annotations

import json
import re
from typing import Optional


def extract_json_object_string(text: str) -> Optional[str]:
    """Return a JSON **object** substring suitable for ``json.loads``."""
    if not text or not text.strip():
        return None

    fence = re.search(
        r"```(?:json)?\s*([\s\S]*?)\s*```",
        text,
        re.IGNORECASE,
    )
    if fence:
        inner = fence.group(1).strip()
        if inner:
            text = inner

    text = text.strip()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return text
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    if start == -1:
        return None
    end = find_matching_brace(text, start)
    if end == -1:
        return None
    snippet = text[start : end + 1]
    try:
        json.loads(snippet)
        return snippet
    except json.JSONDecodeError:
        return None


def extract_json_value_string(text: str) -> Optional[str]:
    """Return the first JSON **object or array** substring."""
    if not text or not text.strip():
        return None

    fence = re.search(
        r"```(?:json)?\s*([\s\S]*?)\s*```",
        text,
        re.IGNORECASE,
    )
    if fence:
        inner = fence.group(1).strip()
        if inner:
            text = inner

    text = text.strip()
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    start_obj = text.find("{")
    start_arr = text.find("[")
    if start_obj != -1 and (start_arr == -1 or start_obj < start_arr):
        end = find_matching_brace(text, start_obj)
        if end != -1:
            snippet = text[start_obj : end + 1]
            try:
                json.loads(snippet)
                return snippet
            except json.JSONDecodeError:
                pass
    if start_arr != -1:
        end = find_matching_bracket(text, start_arr)
        if end != -1:
            snippet = text[start_arr : end + 1]
            try:
                json.loads(snippet)
                return snippet
            except json.JSONDecodeError:
                pass
    return None


def find_matching_brace(text: str, start: int) -> int:
    """Index of closing ``}`` for object starting at ``start``, or -1."""
    depth = 0
    in_string: Optional[str] = None
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_string:
                in_string = None
            continue
        if ch in ('"', "'"):
            in_string = ch
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def find_matching_bracket(text: str, start: int) -> int:
    """Index of closing ``]`` for array starting at ``start``, or -1."""
    depth = 0
    in_string: Optional[str] = None
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_string:
                in_string = None
            continue
        if ch in ('"', "'"):
            in_string = ch
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return i
    return -1
