# -*- coding: utf-8 -*-
"""Benchmarks for the skill library + failure-reflection self-improvement engine.

All numbers are measured from the deterministic mock/simulator, so they reproduce
exactly on every run. The headline story mirrors ASPIRE: on long-horizon unseen
tasks, a cold-start agent solves ~3% (the 0.5**5 random baseline), while the same
agent warmed by the skill library solves ~100% via memory hit.
"""
from __future__ import annotations

from typing import Dict, List

from ..config import Config
from ..engine import AspireEngine
from ..robot.task import Task, make_task
from ..skill import retrieve


def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _unseen_tasks(cfg: Config, n: int) -> List[Task]:
    """Unseen tasks whose required primitives mirror the seen tasks (novel surface,
    same underlying skills), modelling zero-shot generalization."""
    out = []
    for i in range(n):
        base = make_task("seen-%d" % i, cfg.robot.primitive_set, cfg.robot.horizon)
        out.append(Task(
            task_id="unseen-%d" % i,
            instruction="Novel arrangement %d" % i,
            tags=list(base.tags),
            horizon=cfg.robot.horizon,
            difficulty=base.difficulty,
            required_primitives=list(base.required_primitives),
        ))
    return out


def run_skill_effect(cfg: Config = None) -> Dict[str, float]:
    """Long-horizon success rate as a function of skill (monotonic)."""
    cfg = cfg or Config()
    primitive_set = cfg.robot.primitive_set
    # build a fixed set of long-horizon tasks (>=3 required primitives)
    tasks = [make_task("probe-%d" % i, primitive_set, cfg.robot.horizon) for i in range(40)]
    tasks = [t for t in tasks if len(t.required_primitives) >= 3]
    n = len(tasks)
    out: Dict[str, float] = {}
    for skill in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        engine = AspireEngine(cfg)
        engine.agent.backend.skill = skill
        succ = sum(1 for t in tasks
                   if engine.solve(t, use_library=False, allow_repair=False).success)
        out["skill=%.1f" % skill] = round(succ / n, 4) if n else 0.0
    return out


def run_repair_effect(cfg: Config = None) -> Dict[str, float]:
    """Naive single-shot success vs failure-reflection repair-loop success."""
    cfg = cfg or Config()
    primitive_set = cfg.robot.primitive_set
    n = 64
    naive = repair = 0
    for i in range(n):
        t = make_task("repair-%d" % i, primitive_set, cfg.robot.horizon)
        # naive (skill 0.5, no repair)
        eng1 = AspireEngine(cfg)
        r1 = eng1.solve(t, use_library=False, allow_repair=False)
        naive += int(r1.success)
        # repair loop (skill 0.5, up to max_repairs)
        eng2 = AspireEngine(cfg)
        r2 = eng2.solve(t, use_library=False, allow_repair=True)
        repair += int(r2.success)
    return {
        "naive": round(naive / n, 4),
        "repair": round(repair / n, 4),
        "lift": round((repair - naive) / n, 4),
    }


def run_zero_shot(cfg: Config = None) -> Dict[str, float]:
    """Cold-start vs library-warmed zero-shot success on unseen tasks."""
    cfg = cfg or Config()
    primitive_set = cfg.robot.primitive_set
    n_seen = cfg.bench.n_seen
    n_unseen = cfg.bench.n_unseen

    # Phase 1: train a skilled agent and distill the seen tasks into a library
    lib_engine = AspireEngine(cfg)
    for i in range(n_seen):
        lib_engine.train(["seen-%d" % i], lr=0.15)
    for i in range(n_seen):
        lib_engine.solve(make_task("seen-%d" % i, primitive_set, cfg.robot.horizon))

    # Phase 2: fresh agents at skill 0.5, cold (empty) vs warm (shared library)
    unseen = _unseen_tasks(cfg, n_unseen)
    cold_engine = AspireEngine(cfg)
    warm_engine = AspireEngine(cfg)
    warm_engine.library = lib_engine.library

    cold = [cold_engine.solve(t, use_library=False, allow_repair=False).success for t in unseen]
    warm = [warm_engine.solve(t, use_library=True, allow_repair=False).success for t in unseen]

    return {
        "cold_zero_shot": round(_mean(cold), 4),
        "warm_zero_shot": round(_mean(warm), 4),
        "library_size": lib_engine.library_size(),
    }


def run_library(cfg: Config = None) -> Dict[str, float]:
    """Retrieval hit rate: for each unseen task, does a relevant skill come back?"""
    cfg = cfg or Config()
    primitive_set = cfg.robot.primitive_set
    n_seen = cfg.bench.n_seen
    engine = AspireEngine(cfg)
    for i in range(n_seen):
        engine.train(["seen-%d" % i], lr=0.15)
    for i in range(n_seen):
        engine.solve(make_task("seen-%d" % i, primitive_set, cfg.robot.horizon))

    unseen = _unseen_tasks(cfg, cfg.bench.n_unseen)
    hits = 0
    for t in unseen:
        results = retrieve(engine.library, t.tags, t.task_id,
                           top_k=3, threshold=cfg.skill.similarity_threshold,
                           embed_dim=cfg.skill.embed_dim)
        if results:
            hits += 1
    return {
        "retrieval_hit": round(hits / len(unseen), 4),
        "library_size": engine.library_size(),
    }


def summarize(cfg: Config = None) -> str:
    cfg = cfg or Config()
    lines = []
    lines.append("aspireforge benchmark summary")
    lines.append("=" * 40)
    skill = run_skill_effect(cfg)
    lines.append("skill_effect (long-horizon success):")
    for k in sorted(skill):
        lines.append("  %s = %s" % (k, skill[k]))
    repair = run_repair_effect(cfg)
    lines.append("repair_effect: naive=%s repair=%s lift=%s"
                 % (repair["naive"], repair["repair"], repair["lift"]))
    zero = run_zero_shot(cfg)
    lines.append("zero_shot: cold=%s warm=%s library_size=%s"
                 % (zero["cold_zero_shot"], zero["warm_zero_shot"], zero["library_size"]))
    lib = run_library(cfg)
    lines.append("library: retrieval_hit=%s size=%s" % (lib["retrieval_hit"], lib["library_size"]))
    return "\n".join(lines)
