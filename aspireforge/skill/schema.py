# -*- coding: utf-8 -*-
"""Skill schema."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


@dataclass
class SkillProvenance:
    """Where a skill came from and how it was verified."""
    source_task_id: str = ""
    trajectory_id: str = ""
    verified: bool = False
    success: bool = False
    attempts: int = 0
    distilled_from: str = ""          # original program or parent skill id

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Skill:
    """A reusable, verified control-code snippet."""
    skill_id: str = ""                # content address (md5 of code)
    name: str = ""
    tags: List[str] = field(default_factory=list)
    obs_signature: str = ""           # hashed observation signature it applies to
    code: str = ""                    # control program source
    embedding: List[float] = field(default_factory=list)
    success_rate: float = 0.0
    version: int = 1
    provenance: SkillProvenance = field(default_factory=SkillProvenance)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Skill":
        prov = SkillProvenance(**d.get("provenance", {})) if d.get("provenance") else SkillProvenance()
        return cls(
            skill_id=d.get("skill_id", ""),
            name=d.get("name", ""),
            tags=list(d.get("tags", [])),
            obs_signature=d.get("obs_signature", ""),
            code=d.get("code", ""),
            embedding=list(d.get("embedding", [])),
            success_rate=d.get("success_rate", 0.0),
            version=d.get("version", 1),
            provenance=prov,
        )
