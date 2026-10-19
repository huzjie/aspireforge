# -*- coding: utf-8 -*-
"""Execution trajectory capture."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from .observation import Observation


@dataclass
class Step:
    step: int = 0
    observation: Observation = field(default_factory=Observation)
    action: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"step": self.step, "observation": self.observation.to_dict(), "action": self.action}


@dataclass
class Trajectory:
    task_id: str = ""
    success: bool = False
    steps: List[Step] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.steps)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "success": self.success,
            "steps": [s.to_dict() for s in self.steps],
        }
