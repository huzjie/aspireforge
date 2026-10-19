# -*- coding: utf-8 -*-
"""Repair: regenerate a corrected program from a failure report."""
from __future__ import annotations

from typing import Optional

from ..coder.agent import CodingAgent
from ..config import Config
from ..robot.task import Task
from ..utils.codegen import Program


class Repairer:
    """Repairs a failing program by delegating to the coding agent with the
    failure report as conditioning context."""

    def __init__(self, agent: Optional[CodingAgent] = None, cfg: Optional[Config] = None):
        self.cfg = cfg or Config()
        self.agent = agent or CodingAgent(self.cfg)

    def repair(self, task: Task, program_code: str, failure_class: str, evidence: str) -> Program:
        return self.agent.repair_program(task, program_code, failure_class, evidence)
