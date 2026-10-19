# -*- coding: utf-8 -*-
"""Minimal YAML-subset parser (zero-dependency fallback).

Supports the subset aspireforge configs actually use:
  * ``key: value`` scalars (str / int / float / bool / null)
  * nested mappings by indentation
  * block lists (``- item``) and lists of mappings (``- key: value``)
  * inline lists ``[a, b, c]`` and inline comments ``# ...``

Tabs are rejected; indentation must use spaces.
"""
from __future__ import annotations

from typing import Any, List, Tuple


def _strip_comment(s: str) -> str:
    in_s = in_d = False
    for i, ch in enumerate(s):
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        elif ch == "#" and not in_s and not in_d and (i == 0 or s[i - 1] == " "):
            return s[:i].rstrip()
    return s


def _split_key(s: str) -> Tuple[str, str]:
    in_s = in_d = False
    for i, ch in enumerate(s):
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        elif ch == ":" and not in_s and not in_d:
            return s[:i].strip(), s[i + 1:].strip()
    return s.strip(), ""


def _scalar(s: str) -> Any:
    s = s.strip()
    if not s:
        return None
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_scalar(x) for x in inner.split(",")]
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    low = s.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "none", "~"):
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _tokenize(text: str) -> List[Tuple[int, str]]:
    lines: List[Tuple[int, str]] = []
    for raw in text.splitlines():
        if "\t" in raw:
            raise ValueError("tabs are not allowed in yamlish")
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        content = _strip_comment(raw.strip())
        if not content:
            continue
        lines.append((indent, content))
    return lines


def _parse_block(lines: List[Tuple[int, str]], i: int, min_indent: int):
    if i >= len(lines):
        return {}, i
    first_indent = lines[i][0]
    if lines[i][1].startswith("- "):
        return _parse_list(lines, i, first_indent)

    result: dict = {}
    while i < len(lines):
        indent, content = lines[i]
        if indent < min_indent:
            break
        if content.startswith("- "):
            break
        key, val = _split_key(content)
        if val:
            result[key] = _scalar(val)
            i += 1
        else:
            if i + 1 < len(lines) and lines[i + 1][0] > indent:
                nxt = lines[i + 1]
                if nxt[1].startswith("- "):
                    sub, i = _parse_list(lines, i + 1, nxt[0])
                else:
                    sub, i = _parse_block(lines, i + 1, nxt[0])
                result[key] = sub
            else:
                result[key] = None
                i += 1
    return result, i


def _parse_list(lines: List[Tuple[int, str]], i: int, item_indent: int):
    lst: list = []
    while i < len(lines):
        indent, content = lines[i]
        if indent != item_indent or not (content.startswith("- ") or content == "-"):
            break
        body = content[2:].strip() if content.startswith("- ") else ""
        i += 1
        if not body:
            if i < len(lines) and lines[i][0] > item_indent:
                val, i = _parse_block(lines, i, lines[i][0])
                lst.append(val)
            else:
                lst.append(None)
        else:
            key, val = _split_key(body)
            if ":" in body and val:
                lst.append({key: _scalar(val)})
            elif ":" in body and not val:
                d: dict = {}
                if i < len(lines) and lines[i][0] > item_indent:
                    sub, i = _parse_block(lines, i, lines[i][0])
                    d[key] = sub
                else:
                    d[key] = None
                lst.append(d)
            else:
                lst.append(_scalar(body))
    return lst, i


def parse(text: str) -> dict:
    lines = _tokenize(text)
    if not lines:
        return {}
    value, _ = _parse_block(lines, 0, lines[0][0])
    return value if isinstance(value, dict) else {"items": value}
