# -*- coding: utf-8 -*-
"""Simple in-process metric accumulation (no external deps)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class RunMetrics:
    solves: int = 0
    successes: int = 0
    memory_hits: int = 0
    total_attempts: int = 0
    distilled: int = 0
    failure_class_counts: Dict[str, int] = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        return self.successes / self.solves if self.solves else 0.0

    @property
    def memory_hit_rate(self) -> float:
        return self.memory_hits / self.solves if self.solves else 0.0

    def record(self, result):
        self.solves += 1
        self.successes += int(result.success)
        self.memory_hits += int(result.memory_hit)
        self.total_attempts += result.attempts
        self.distilled += len(result.distilled)
        for cls in result.failure_history:
            self.failure_class_counts[cls] = self.failure_class_counts.get(cls, 0) + 1


class MetricAccumulator:
    def __init__(self):
        self.metrics = RunMetrics()

    def record(self, result):
        self.metrics.record(result)

    def summary(self) -> dict:
        m = self.metrics
        return {
            "solves": m.solves,
            "success_rate": round(m.success_rate, 4),
            "memory_hit_rate": round(m.memory_hit_rate, 4),
            "avg_attempts": round(m.total_attempts / m.solves, 3) if m.solves else 0,
            "distilled": m.distilled,
            "failure_classes": dict(m.failure_class_counts),
        }
