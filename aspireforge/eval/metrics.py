# -*- coding: utf-8 -*-
"""Evaluation metrics over a list of SolveResult objects."""
from __future__ import annotations

from typing import List


def success_rate(results) -> float:
    """Fraction of results with success=True."""
    if not results:
        return 0.0
    return sum(1 for r in results if r.success) / len(results)


def mean_attempts(results) -> float:
    if not results:
        return 0.0
    return sum(r.attempts for r in results) / len(results)


def memory_hit_rate(results) -> float:
    if not results:
        return 0.0
    return sum(1 for r in results if r.memory_hit) / len(results)
