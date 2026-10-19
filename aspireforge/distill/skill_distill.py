# -*- coding: utf-8 -*-
"""Distill a successful program + trajectory into a reusable Skill.

The distilled skill captures: the (canonicalized) code, the task tags, the
observation signature, a semantic embedding, and provenance (which trajectory
produced it, how many attempts it took, and that it was verified).
"""
from __future__ import annotations

from typing import Optional

from ..config import Config
from ..robot.task import Task
from ..robot.trajectory import Trajectory
from ..skill import Skill, SkillProvenance
from ..skill.retrieval import embed_task, obs_signature
from ..utils.codegen import Program
from ..utils.hashing import skill_id_of


class SkillDistiller:
    """Creates a reusable Skill from a successful (program, trajectory) pair."""

    def __init__(self, cfg: Optional[Config] = None):
        self.cfg = cfg or Config()

    def distill(self, task: Task, program: Program, trajectory: Trajectory,
                name: Optional[str] = None) -> Skill:
        code = program.code
        sid = skill_id_of(code)
        tags = sorted(set(task.tags))
        return Skill(
            skill_id=sid,
            name=name or ("skill-" + task.task_id),
            tags=tags,
            obs_signature=obs_signature(tags, task.task_id),
            code=code,
            embedding=embed_task(tags, task.task_id, self.cfg.skill.embed_dim),
            success_rate=1.0,
            version=1,
            provenance=SkillProvenance(
                source_task_id=task.task_id,
                trajectory_id=task.task_id + ":0",
                verified=True,
                success=True,
                attempts=len(trajectory.steps),
                distilled_from=program.model,
            ),
        )
