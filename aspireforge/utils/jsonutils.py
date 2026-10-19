# -*- coding: utf-8 -*-
"""JSON helpers (deterministic, ensure_ascii=False by default)."""
from __future__ import annotations

import json
from typing import Any


def dumps(obj: Any, indent: int = 2) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=indent)


def loads(text: str) -> Any:
    return json.loads(text)
