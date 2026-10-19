# -*- coding: utf-8 -*-
"""Semantic + tag-based retrieval over the skill library."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ..utils.hashing import md5_hex
from ..utils.stable import cosine, stable_vector
from .schema import Skill


@dataclass
class RetrievalResult:
    skill: Skill
    score: float
    tag_overlap: int = 0


def _tag_similarity(a: List[str], b: List[str]) -> int:
    return len(set(a) & set(b))


def obs_signature(tags: List[str], task_id: str) -> str:
    """Deterministic observation signature for a task (tags + id)."""
    return md5_hex(("|".join(sorted(tags)) + "@" + task_id).encode("utf-8"))[:12]


def embed_task(tags: List[str], task_id: str, dim: int = 32) -> List[float]:
    """Deterministic embedding for a task (tag-driven)."""
    return stable_vector("embed:" + "|".join(sorted(tags)) + ":" + task_id, dim)


def retrieve(
    library,
    tags: List[str],
    task_id: str,
    top_k: int = 3,
    threshold: float = 0.6,
    embed_dim: int = 32,
) -> List[RetrievalResult]:
    """Retrieve the top-k skills for a task, ranked by tag overlap then embedding
    similarity. Returns an empty list when nothing clears the threshold."""
    query_emb = embed_task(tags, task_id, embed_dim)
    scored: List[RetrievalResult] = []
    for skill in library.all():
        overlap = _tag_similarity(tags, skill.tags)
        sim = cosine(query_emb, skill.embedding) if skill.embedding else 0.0
        # tag overlap dominates, embedding refines within the same overlap
        score = overlap + 0.2 * sim
        if overlap == 0 and sim < threshold:
            continue
        scored.append(RetrievalResult(skill=skill, score=score, tag_overlap=overlap))
    scored.sort(key=lambda r: (r.score, r.tag_overlap), reverse=True)
    return scored[:top_k]
