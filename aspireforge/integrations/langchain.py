# -*- coding: utf-8 -*-
"""LangChain integration: expose the engine as a langchain Tool (optional)."""
from __future__ import annotations

from ..config import Config
from ..engine import AspireEngine


def make_skill_tool(cfg=None):
    """Return a callable compatible with langchain Tool when langchain is present."""
    cfg = cfg or Config()
    engine = AspireEngine(cfg)

    def _solve(task_id: str) -> str:
        task = engine._task(task_id)
        res = engine.solve(task)
        return "success=%s attempts=%d memory_hit=%s" % (res.success, res.attempts, res.memory_hit)

    _solve.engine = engine
    return _solve
