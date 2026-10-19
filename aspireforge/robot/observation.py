# -*- coding: utf-8 -*-
"""Observation model: scene state, objects, goal."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


@dataclass
class Observation:
    """A snapshot of the robot's world at a timestep."""
    state: List[float] = field(default_factory=list)      # proprioception
    objects: List[str] = field(default_factory=list)      # object ids in scene
    goal: str = ""
    step: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
