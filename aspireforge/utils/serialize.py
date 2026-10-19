# -*- coding: utf-8 -*-
"""Skill / task serialization to and from JSON."""
from __future__ import annotations

import json
from typing import Any

from ..robot.task import Task
from ..skill import Skill


def skill_to_json(skill: Skill, indent: int = 2) -> str:
    return json.dumps(skill.to_dict(), ensure_ascii=False, indent=indent)


def skill_from_json(text: str) -> Skill:
    return Skill.from_dict(json.loads(text))


def task_to_json(task: Task, indent: int = 2) -> str:
    return json.dumps(task.to_dict(), ensure_ascii=False, indent=indent)


def task_from_json(text: str) -> Task:
    return Task.from_dict(json.loads(text))


def dumps(obj: Any, indent: int = 2) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=indent)
