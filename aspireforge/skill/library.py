# -*- coding: utf-8 -*-
"""Content-addressed skill store."""
from __future__ import annotations

from typing import Dict, Iterator, List, Optional

from .schema import Skill


class SkillLibrary:
    """Abstract skill store, keyed by content address (skill_id)."""

    def put(self, skill: Skill) -> str:
        raise NotImplementedError

    def get(self, skill_id: str) -> Optional[Skill]:
        raise NotImplementedError

    def has(self, skill_id: str) -> bool:
        raise NotImplementedError

    def all(self) -> List[Skill]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Skill]:
        raise NotImplementedError

    def evict(self, n: int) -> List[str]:
        """Evict the least-recently-used skills, returning their ids."""
        raise NotImplementedError


class MemorySkillLibrary(SkillLibrary):
    """In-memory skill store with LRU eviction and a size cap."""

    def __init__(self, max_skills: int = 4096):
        self.max_skills = max_skills
        self._skills: Dict[str, Skill] = {}
        self._order: List[str] = []       # most-recently-used at the end

    def put(self, skill: Skill) -> str:
        sid = skill.skill_id
        if sid in self._skills:
            # bump recency, keep newest provenance
            self._skills[sid] = skill
            self._order = [x for x in self._order if x != sid] + [sid]
            return sid
        self._skills[sid] = skill
        self._order.append(sid)
        if len(self._order) > self.max_skills:
            self._evict_one()
        return sid

    def _evict_one(self):
        victim = self._order.pop(0)
        self._skills.pop(victim, None)

    def get(self, skill_id: str) -> Optional[Skill]:
        skill = self._skills.get(skill_id)
        if skill is not None:
            self._order = [x for x in self._order if x != skill_id] + [skill_id]
        return skill

    def has(self, skill_id: str) -> bool:
        return skill_id in self._skills

    def all(self) -> List[Skill]:
        return list(self._skills.values())

    def __len__(self) -> int:
        return len(self._skills)

    def __iter__(self) -> Iterator[Skill]:
        return iter(self._skills.values())

    def evict(self, n: int) -> List[str]:
        evicted = self._order[:n]
        for sid in evicted:
            self._skills.pop(sid, None)
        self._order = self._order[n:]
        return evicted
