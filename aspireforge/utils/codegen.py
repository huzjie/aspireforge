# -*- coding: utf-8 -*-
"""Deterministic code rendering for robot control programs.

Programs are plain Python source whose calls declare the ordered primitives the
simulator checks (see oracle.program_primitives). Rendering is deterministic so a
given (task, skill) pair always produces the same source.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Program:
    """A generated control program: source text plus parsed metadata."""
    code: str
    primitives: List[str] = field(default_factory=list)
    task_id: str = ""
    model: str = "mock"

    def to_dict(self):
        return {
            "code": self.code,
            "primitives": self.primitives,
            "task_id": self.task_id,
            "model": self.model,
        }


def primitives_line(primitives: List[str]) -> str:
    """Render the ordered primitive-call lines for a program body."""
    lines = []
    for p in primitives:
        lines.append("    robot.%s(target)" % p)
    return "\n".join(lines)


def render_program(task_id: str, primitives: List[str], model: str = "mock") -> Program:
    """Render a full, syntactically valid control program from an ordered list."""
    body = primitives_line(primitives)
    if not body:
        body = "    pass"
    code = (
        "# auto-generated control program for task %s\n"
        "def run(robot):\n"
        "    target = robot.goal()\n"
        "%s\n"
        "    return robot.success()\n"
    ) % (task_id, body)
    return Program(code=code, primitives=list(primitives), task_id=task_id, model=model)
