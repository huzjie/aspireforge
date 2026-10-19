# -*- coding: utf-8 -*-
"""Skill library: content-addressed, semantically retrievable store of verified
control-code snippets with full provenance.

This is the "experience memory" of the agent. Every successful program (and the
trajectory that produced it) is distilled into a Skill; later tasks retrieve
skills by tag overlap + embedding similarity and cold-start from them.
"""
from .schema import Skill, SkillProvenance
from .library import SkillLibrary, MemorySkillLibrary
from .retrieval import retrieve, RetrievalResult

__all__ = [
    "Skill", "SkillProvenance",
    "SkillLibrary", "MemorySkillLibrary",
    "retrieve", "RetrievalResult",
]
