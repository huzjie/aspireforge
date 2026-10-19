# -*- coding: utf-8 -*-
"""Top-level engine: solve tasks with retrieval + failure-reflection self-improvement."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from .coder.agent import CodingAgent
from .config import Config
from .oracle import program_correct_for
from .reflect.loop import SelfRepairLoop
from .robot.sim import Simulator
from .robot.task import Task
from .skill import MemorySkillLibrary, retrieve


@dataclass
class SolveResult:
    task_id: str = ""
    success: bool = False
    attempts: int = 0
    memory_hit: bool = False
    program: Optional[str] = None
    distilled: List[str] = field(default_factory=list)
    failure_history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AspireEngine:
    """Coordinates the full solve pipeline for a fleet of tasks."""

    def __init__(self, cfg: Optional[Config] = None, backend_name: Optional[str] = None):
        self.cfg = cfg or Config()
        self.backend_name = backend_name or self.cfg.coder.model
        self.primitive_set = self.cfg.robot.primitive_set
        self.library = MemorySkillLibrary(max_skills=self.cfg.skill.max_skills)
        self.sim = Simulator(self.primitive_set)
        self.loop = SelfRepairLoop(self.cfg, library=self.library)
        self.agent = self.loop.agent

    def solve(self, task: Task, use_library: bool = True, allow_repair: bool = True) -> SolveResult:
        """Solve one task. Optionally warm-start from the library and repair failures."""
        result = SolveResult(task_id=task.task_id)

        # 1) memory hit: a retrieved skill whose code is already correct
        if use_library:
            for r in retrieve(self.library, task.tags, task.task_id,
                              top_k=3, threshold=self.cfg.skill.similarity_threshold,
                              embed_dim=self.cfg.skill.embed_dim):
                if program_correct_for(task.required_primitives, r.skill.code, self.primitive_set):
                    result.success = True
                    result.memory_hit = True
                    result.attempts = 1
                    result.program = r.skill.code
                    return result

        # 2) generate (+ repair) via the self-improvement loop
        loop_result = self.loop.run(task) if allow_repair else self._generate_once(task)
        result.success = loop_result.success
        result.attempts = loop_result.attempts
        result.program = loop_result.program.code if loop_result.program else None
        result.distilled = list(loop_result.distilled_skills)
        result.failure_history = list(loop_result.failure_history)
        return result

    def _generate_once(self, task: Task):
        from .reflect.loop import LoopResult
        program = self.agent.generate_program(task, self.library)
        traj = self.sim.run(task, program.code)
        return LoopResult(task_id=task.task_id, success=traj.success, attempts=1, program=program)

    def train(self, task_ids: List[str], lr: float = 0.1):
        """Train the mock backend skill toward 1.0 over a list of tasks."""
        backend = self.agent.backend
        for tid in task_ids:
            task = self._task(tid)
            program = backend.generate_program(task, [], "")
            correct = program_correct_for(task.required_primitives, program.code, self.primitive_set)
            backend.train_step(lr=lr, correct=correct)
        return getattr(backend, "skill", 0.5)

    def _task(self, task_id: str) -> Task:
        from .robot.task import make_task
        return make_task(task_id, self.primitive_set, self.cfg.robot.horizon)

    def library_size(self) -> int:
        return len(self.library)
