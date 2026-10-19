# -*- coding: utf-8 -*-
"""Deterministic, trainable mock backend.

``skill`` in [0, 1] drives generation fidelity. The signal is monotonic by
construction: at skill=0.5 the boost is exactly zero, so each required primitive is
kept with p=0.5 (success = 0.5**len, the random baseline); at skill=1.0 the boost is
1.0 and every required primitive is kept in order (success = 1.0).
"""
from __future__ import annotations

from ..config import Config
from ..oracle import program_primitives
from ..utils.stable import stable_bool
from ..utils.codegen import render_program
from .registry import register_backend


@register_backend("mock")
class MockBackend:
    name = "mock"

    def __init__(self, cfg=None):
        self.cfg = cfg or Config()
        self.skill = 0.5
        self.primitive_set = self.cfg.robot.primitive_set

    def _boost(self) -> float:
        return (self.skill - 0.5) * 2.0

    def generate_program(self, task, skills, prompt):
        required = task.required_primitives
        boost = self._boost()
        chosen = [p for p in required
                  if stable_bool("gen:%s:keep:%s" % (task.task_id, p), p=0.5 + 0.5 * boost)]
        return render_program(task.task_id, chosen, model="mock")

    def repair_program(self, task, program_code, failure_class, prompt):
        required = task.required_primitives
        actual = set(program_primitives(program_code, self.primitive_set))
        boost = self._boost()
        # repair re-adds missing primitives with higher confidence than naive gen
        chosen = [p for p in required
                  if p in actual or stable_bool("repair:%s:%s" % (task.task_id, p),
                                                p=min(1.0, 0.6 + 0.4 * boost))]
        return render_program(task.task_id, chosen, model="mock")

    def train_step(self, lr: float = 0.1, correct: bool = True):
        """Monotonically raise skill toward 1.0 (never decrease)."""
        # every step moves skill toward 1.0 by a fixed amount (deterministic)
        self.skill = min(1.0, self.skill + lr * (1.0 - self.skill))
        return self.skill
