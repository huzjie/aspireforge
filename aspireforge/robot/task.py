# -*- coding: utf-8 -*-
"""Robot task model (LIBERO-Pro style: instruction + goal + tags + horizon)."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from ..oracle import task_primitives


@dataclass
class Task:
    task_id: str = ""
    instruction: str = ""
    tags: List[str] = field(default_factory=list)
    horizon: int = 64
    difficulty: int = 1                 # 1..5 (long-horizon when high)
    required_primitives: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Task":
        return cls(
            task_id=d.get("task_id", ""),
            instruction=d.get("instruction", ""),
            tags=list(d.get("tags", [])),
            horizon=d.get("horizon", 64),
            difficulty=d.get("difficulty", 1),
            required_primitives=list(d.get("required_primitives", [])),
        )


def make_task(task_id: str, primitive_set: List[str], horizon: int = 64) -> Task:
    """Build a deterministic task from an id. The required primitives and tags are
    derived deterministically so every consumer sees the same task."""
    from ..utils.stable import stable_ints
    prims = task_primitives(task_id, primitive_set, horizon)
    # tags: a few primitives plus a domain word, stable per task
    domain = ["kitchen", "warehouse", "assembly", "pickplace"][stable_ints("task:dom:" + task_id, 1, 0, 3)[0]]
    tags = sorted(set(prims + [domain]))
    instruction = "Perform %s in %s" % (" then ".join(prims), domain)
    return Task(
        task_id=task_id,
        instruction=instruction,
        tags=tags,
        horizon=horizon,
        difficulty=min(5, max(1, len(prims))),
        required_primitives=prims,
    )
