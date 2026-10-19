# -*- coding: utf-8 -*-
"""Deterministic task corpus builder (LIBERO-Pro style seen/unseen splits)."""
from __future__ import annotations

from typing import Dict, List

from .synth import TaskFactory


def build_corpus(cfg=None, n_seen: int = 32, n_unseen: int = 32) -> Dict[str, List]:
    """Return {"seen": [...], "unseen": [...]} deterministic splits."""
    from ..config import Config
    cfg = cfg or Config()
    factory = TaskFactory(cfg.robot.primitive_set, cfg.robot.horizon)
    return {
        "seen": factory.seen(n_seen),
        "unseen": factory.unseen(n_unseen),
    }
