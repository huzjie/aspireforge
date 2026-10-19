# -*- coding: utf-8 -*-
"""Deterministic pseudo-random helpers.

Every function is seeded by ``md5(key)`` (first 8 bytes) driving a local
``random.Random``. Identical keys always produce identical output, which makes the
mock backend reproducible and lets the simulator and benchmarks share one truth.
"""
from __future__ import annotations

import hashlib
import random
from typing import List, Sequence, TypeVar

T = TypeVar("T")


def _seed(key: str) -> int:
    digest = hashlib.md5(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def stable_float(key: str, lo: float = 0.0, hi: float = 1.0) -> float:
    r = random.Random(_seed(key))
    return lo + (hi - lo) * r.random()


def stable_ints(key: str, n: int, lo: int, hi: int) -> List[int]:
    r = random.Random(_seed(key))
    return [r.randint(lo, hi) for _ in range(n)]


def stable_vector(key: str, n: int, lo: float = -1.0, hi: float = 1.0) -> List[float]:
    r = random.Random(_seed(key))
    return [lo + (hi - lo) * r.random() for _ in range(n)]


def stable_bool(key: str, p: float = 0.5) -> bool:
    r = random.Random(_seed(key))
    return r.random() < p


def stable_sample(key: str, population: Sequence[T], k: int) -> List[T]:
    r = random.Random(_seed(key))
    return r.sample(list(population), k)


def cosine(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two equal-length vectors (zero-safe)."""
    if len(a) != len(b):
        raise ValueError("vector length mismatch")
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)
