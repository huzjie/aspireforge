# -*- coding: utf-8 -*-
"""Shared ground truth for the mock simulator and the benchmarks.

Both the mock backend and the benchmark must derive success from the SAME
deterministic function, so that a fully-trained skill (skill = 1.0) yields
success = 1.0 and a random skill (0.5) yields the random baseline. This is the
single source of truth that keeps every number reproducible and monotonic.
"""
from __future__ import annotations

from typing import List, Optional


def task_primitives(task_id: str, primitive_set: List[str], horizon: int = 64) -> List[str]:
    """Deterministically derive the ordered primitives a task requires.

    The order matters: executing the primitives in the correct order is what a
    correct control program does, which is exactly what the simulator checks.
    """
    from .utils.stable import stable_ints
    n = 2 + (stable_ints("task:len:" + task_id, 1, 0, 3)[0] % min(5, len(primitive_set)))
    idxs = stable_ints("task:prims:" + task_id, n, 0, len(primitive_set) - 1)
    # dedupe preserving order
    seen = set()
    out = []
    for i in idxs:
        if i not in seen:
            seen.add(i)
            out.append(primitive_set[i])
    return out


def program_primitives(program_code: str, primitive_set: List[str]) -> List[str]:
    """Extract the primitives a program performs, in code order (by textual marker
    position, not primitive-set order)."""
    found = []
    for p in primitive_set:
        marker = p + "("
        pos = program_code.find(marker)
        if pos >= 0:
            found.append((pos, p))
    found.sort()
    return [p for _, p in found]


def program_correct_for(required: List[str], program_code: str, primitive_set: List[str]) -> bool:
    """A program is correct iff it performs ``required`` in order (a superset with
    extra steps still counts as long as the required sequence is a subsequence)."""
    actual = program_primitives(program_code, primitive_set)
    if not required:
        return True
    # check required is a subsequence of actual (in order)
    it = iter(actual)
    return all(any(p == x for x in it) for p in required)


def program_correct(task_id: str, program_code: str, primitive_set: List[str]) -> bool:
    """Convenience wrapper: derive the required primitives from the task id."""
    return program_correct_for(task_primitives(task_id, primitive_set), program_code, primitive_set)


def failure_class_for(required: List[str], task_id: str, program_code: str, primitive_set: List[str]) -> str:
    """Deterministic root-cause classification of a failing program."""
    from .utils.stable import stable_float
    actual = program_primitives(program_code, primitive_set)
    missing = [p for p in required if p not in actual]
    if missing:
        # classify the kind of missing primitive
        kind = missing[0]
        if kind in ("move_to",):
            return "goal_not_reached"
        if kind in ("grasp",):
            return "grasp_failure"
        if kind in ("wait",):
            return "timing_error"
        if kind in ("open", "close", "rotate"):
            return "precondition_violation"
        if kind in ("push", "place"):
            return "collision"
        return "none"
    # wrong order -> timing
    r = stable_float("fcls:" + task_id, 0.0, 1.0)
    return "timing_error" if r < 0.7 else "collision"
