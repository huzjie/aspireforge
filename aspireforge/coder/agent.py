# -*- coding: utf-8 -*-
"""The coding agent: generate control programs with retrieval augmentation."""
from __future__ import annotations

from typing import List, Optional

from ..config import Config
from ..model import get_backend
from ..robot.task import Task
from ..skill import retrieve
from ..utils.codegen import Program
from .prompt import PromptBuilder


class CodingAgent:
    """Generates robot control programs, optionally augmented by skill retrieval."""

    def __init__(self, cfg: Optional[Config] = None, backend_name: Optional[str] = None):
        self.cfg = cfg or Config()
        self.backend = get_backend(backend_name or self.cfg.coder.model, self.cfg)
        self.prompts = PromptBuilder(self.cfg.robot.primitive_set)

    def generate_program(self, task: Task, library=None) -> Program:
        skills: List = []
        if library is not None:
            results = retrieve(
                library, task.tags, task.task_id,
                top_k=3, threshold=self.cfg.skill.similarity_threshold,
                embed_dim=self.cfg.skill.embed_dim,
            )
            skills = [r.skill for r in results]
        prompt = self.prompts.generate(task, skills)
        return self.backend.generate_program(task, skills, prompt)

    def repair_program(self, task: Task, program_code: str, failure_class: str, evidence: str) -> Program:
        prompt = self.prompts.repair(task, program_code, failure_class, evidence)
        return self.backend.repair_program(task, program_code, failure_class, prompt)
