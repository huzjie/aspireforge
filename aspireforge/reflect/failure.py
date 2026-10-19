# -*- coding: utf-8 -*-
"""Root-cause classification of failed executions."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from ..oracle import failure_class_for
from ..robot.task import Task
from ..robot.trajectory import Trajectory

FAILURE_CLASSES = [
    "collision", "timing_error", "grasp_failure",
    "goal_not_reached", "precondition_violation", "none",
]

EVIDENCE_BY_CLASS = {
    "collision": "an object blocked the end-effector mid-trajectory",
    "timing_error": "an action fired before its precondition was met",
    "grasp_failure": "the gripper closed without an object in contact",
    "goal_not_reached": "the end-effector never reached the goal pose",
    "precondition_violation": "a primitive ran while its guard was false",
    "none": "no specific root cause identified",
}


@dataclass
class FailureReport:
    task_id: str = ""
    failure_class: str = "none"
    evidence: str = ""
    missing_primitives: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FailureAnalyzer:
    """Classifies why a program failed, using the shared oracle and the trajectory."""

    def __init__(self, primitive_set: Optional[List[str]] = None):
        from ..config import default_config
        self.primitive_set = primitive_set or default_config().robot.primitive_set

    def analyze(self, task: Task, program_code: str, trajectory: Optional[Trajectory] = None) -> FailureReport:
        cls = failure_class_for(task.required_primitives, task.task_id, program_code, self.primitive_set)
        # derive missing primitives deterministically
        from ..oracle import program_primitives
        actual = program_primitives(program_code, self.primitive_set)
        missing = [p for p in task.required_primitives if p not in actual]
        return FailureReport(
            task_id=task.task_id,
            failure_class=cls,
            evidence=EVIDENCE_BY_CLASS.get(cls, "unknown"),
            missing_primitives=missing,
        )
