# -*- coding: utf-8 -*-
"""Prompt templates for control-program generation and repair.

These are the exact prompts used to drive generation; they are structured so the
model emits code with declarative primitive calls that the simulator can check.
"""
from __future__ import annotations

from typing import List, Optional

from ..robot.task import Task
from ..skill.schema import Skill

GENERATE_TEMPLATE = (
    "You are a robot control programmer.\n"
    "Task: {instruction}\n"
    "Available primitives: {primitives}\n"
    "{skills_block}"
    "Write a Python function run(robot) that performs the task by calling robot "
    "primitives in order, then returns robot.success().\n"
)

REPAIR_TEMPLATE = (
    "The previous program failed with root cause: {failure_class}.\n"
    "Evidence: {evidence}\n"
    "Task: {instruction}\n"
    "Previous program:\n{program}\n"
    "Write a corrected run(robot) that fixes this failure and returns "
    "robot.success().\n"
)


class PromptBuilder:
    """Builds deterministic prompts from a task and optional skills."""

    def __init__(self, primitive_set: Optional[List[str]] = None):
        from ..config import default_config
        self.primitive_set = primitive_set or default_config().robot.primitive_set

    def generate(self, task: Task, skills: Optional[List[Skill]] = None) -> str:
        skills_block = ""
        if skills:
            lines = ["Relevant skills from the library:"]
            for s in skills:
                lines.append("- %s (%s)" % (s.name, ", ".join(s.tags)))
            skills_block = "\n".join(lines) + "\n"
        return GENERATE_TEMPLATE.format(
            instruction=task.instruction,
            primitives=", ".join(self.primitive_set),
            skills_block=skills_block,
        )

    def repair(self, task: Task, program_code: str, failure_class: str, evidence: str) -> str:
        return REPAIR_TEMPLATE.format(
            failure_class=failure_class,
            evidence=evidence,
            instruction=task.instruction,
            program=program_code,
        )


def build_prompt(task: Task, skills: Optional[List[Skill]] = None) -> str:
    return PromptBuilder().generate(task, skills)
