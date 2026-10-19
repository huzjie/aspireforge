# -*- coding: utf-8 -*-
"""Deterministic synthetic task factory.

Every task is derived from its id via the shared oracle, so two consumers building
the same id always see the same task. This is the data source for benchmarks.
"""
from __future__ import annotations

from typing import List

from ..robot.task import Task, make_task


class TaskFactory:
    """Builds deterministic task suites."""

    def __init__(self, primitive_set: List[str], horizon: int = 64):
        self.primitive_set = primitive_set
        self.horizon = horizon

    def seen(self, n: int) -> List[Task]:
        return [make_task("seen-%d" % i, self.primitive_set, self.horizon) for i in range(n)]

    def unseen(self, n: int) -> List[Task]:
        """Unseen tasks mirroring the seen tasks' primitives (novel surface)."""
        out = []
        for i in range(n):
            base = make_task("seen-%d" % i, self.primitive_set, self.horizon)
            out.append(Task(
                task_id="unseen-%d" % i,
                instruction="Novel arrangement %d" % i,
                tags=list(base.tags),
                horizon=self.horizon,
                difficulty=base.difficulty,
                required_primitives=list(base.required_primitives),
            ))
        return out


def generate_task_suite(cfg=None, n_seen=32, n_unseen=32):
    from ..config import Config
    cfg = cfg or Config()
    factory = TaskFactory(cfg.robot.primitive_set, cfg.robot.horizon)
    return {"seen": factory.seen(n_seen), "unseen": factory.unseen(n_unseen)}
