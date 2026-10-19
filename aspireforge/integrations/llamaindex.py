# -*- coding: utf-8 -*-
"""LlamaIndex integration: query the skill library as a retriever (optional)."""
from __future__ import annotations

from ..config import Config
from ..engine import AspireEngine
from ..skill import retrieve


class SkillRetriever:
    """LlamaIndex-style retriever over the skill library."""

    def __init__(self, cfg=None):
        self.cfg = cfg or Config()
        self.engine = AspireEngine(self.cfg)

    def retrieve(self, query: str, tags=None):
        """Return list of dicts with skill metadata matching the query."""
        tags = tags or query.split()
        results = retrieve(self.engine.library, tags, query,
                           top_k=5, threshold=self.cfg.skill.similarity_threshold,
                           embed_dim=self.cfg.skill.embed_dim)
        return [{"id": r.skill.skill_id, "name": r.skill.name, "score": r.score}
                for r in results]
