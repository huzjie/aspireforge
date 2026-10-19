# -*- coding: utf-8 -*-
"""Content addressing for skills and programs."""
from __future__ import annotations

import hashlib


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def md5_hex(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def skill_id_of(code: str) -> str:
    """Content-address a skill by the hash of its canonical code."""
    return md5_hex(code.encode("utf-8"))
