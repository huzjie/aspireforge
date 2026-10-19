# -*- coding: utf-8 -*-
"""The self-improvement loop: generate -> execute -> reflect -> repair -> verify -> distill."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from ..coder.agent import CodingAgent
from ..config import Config
from ..distill.skill_distill import SkillDistiller
from ..reflect.failure import FailureAnalyzer
from ..robot.sim import Simulator
from ..robot.task import Task
from ..skill import SkillLibrary
from ..utils.codegen import Program


@dataclass
class LoopResult:
    task_id: str = ""
    success: bool = False
    attempts: int = 0
    program: Optional[Program] = None
    distilled_skills: List[str] = field(default_factory=list)
    failure_history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["program"] = self.program.to_dict() if self.program else None
        return d


class SelfRepairLoop:
    """Runs one task through the full generate-execute-reflect-repair-verify cycle."""

    def __init__(self, cfg: Optional[Config] = None, agent: Optional[CodingAgent] = None,
                 library: Optional[SkillLibrary] = None):
        self.cfg = cfg or Config()
        self.agent = agent or CodingAgent(self.cfg)
        self.sim = Simulator(self.cfg.robot.primitive_set)
        self.analyzer = FailureAnalyzer(self.cfg.robot.primitive_set)
        self.distiller = SkillDistiller(self.cfg)
        self.library = library

    def run(self, task: Task) -> LoopResult:
        result = LoopResult(task_id=task.task_id)
        program = self.agent.generate_program(task, self.library)
        traj = self.sim.run(task, program.code)
        attempts = 1
        while not traj.success and attempts <= self.cfg.reflect.max_repairs:
            report = self.analyzer.analyze(task, program.code, traj)
            result.failure_history.append(report.failure_class)
            program = self.agent.repair_program(
                task, program.code, report.failure_class, report.evidence)
            traj = self.sim.run(task, program.code)
            attempts += 1
        result.success = traj.success
        result.attempts = attempts
        result.program = program
        if traj.success and self.library is not None:
            skill = self.distiller.distill(task, program, traj)
            self.library.put(skill)
            result.distilled_skills.append(skill.skill_id)
        return result
