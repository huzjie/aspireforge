# -*- coding: utf-8 -*-
"""Train the mock backend skill monotonically toward 1.0."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from ..config import Config
from ..engine import AspireEngine
from ..oracle import program_correct


@dataclass
class SkillCurve:
    initial: float = 0.5
    final: float = 1.0
    history: List[Tuple[int, float]] = field(default_factory=list)

    def monotonic(self) -> bool:
        vals = [h[1] for h in self.history]
        return all(b >= a for a, b in zip(vals, vals[1:]))


def train_skill(cfg=None, task_ids=None, lr: float = 0.15, steps: int = 12) -> SkillCurve:
    cfg = cfg or Config()
    engine = AspireEngine(cfg)
    backend = engine.agent.backend
    task_ids = task_ids or ["train-%d" % i for i in range(steps)]
    curve = SkillCurve(initial=getattr(backend, "skill", 0.5))
    for step, tid in enumerate(task_ids):
        task = engine._task(tid)
        program = backend.generate_program(task, [], "")
        correct = program_correct(task.task_id, program.code, engine.primitive_set)
        backend.train_step(lr=lr, correct=correct)
        curve.history.append((step + 1, backend.skill))
    curve.final = getattr(backend, "skill", 1.0)
    return curve
