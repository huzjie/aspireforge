# -*- coding: utf-8 -*-
"""Inverted index: tag -> set of skill ids, for fast retrieval."""
from __future__ import annotations

from typing import Dict, List, Set

from .schema import Skill


class TagIndex:
    """Maps each tag to the set of skill ids carrying that tag."""

    def __init__(self):
        self._index: Dict[str, Set[str]] = {}

    def add(self, skill: Skill):
        for tag in skill.tags:
            self._index.setdefault(tag, set()).add(skill.skill_id)

    def remove(self, skill: Skill):
        for tag in skill.tags:
            if tag in self._index:
                self._index[tag].discard(skill.skill_id)

    def lookup(self, tags: List[str]) -> Set[str]:
        hits: Set[str] = set()
        for tag in tags:
            hits |= self._index.get(tag, set())
        return hits

    def clear(self):
        self._index.clear()
