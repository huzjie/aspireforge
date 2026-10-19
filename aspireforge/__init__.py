# -*- coding: utf-8 -*-
"""aspireforge - robot skill library + failure-reflection self-improving coding agent.

A zero-dependency Python reference implementation of the ideas behind NVIDIA ASPIRE:
a coding agent writes robot control programs, learns from failed executions by
reflecting on the trajectory and repairing the code, and distills every successful
method into a reusable skill library so that later, long-horizon unseen tasks can be
solved zero-shot.

Core concepts (see docs/ARCHITECTURE.md):
  * skill library - content-addressed, semantically retrievable store of verified
    control-code snippets with full provenance (which trajectory produced them).
  * failure reflection - capture the execution trajectory, classify the root cause
    (collision / timing / grasp / goal-not-reached / precondition), then regenerate.
  * self-improvement loop - generate -> execute -> reflect -> repair -> verify ->
    distill, so the library compounds over time.
  * zero-shot generalization - unseen tasks cold-start from library retrieval plus a
    bounded repair budget, lifting long-horizon success well above naive baselines.
"""

__version__ = "1.0.0"

from .config import Config, load_config
from .engine import AspireEngine

__all__ = ["Config", "load_config", "AspireEngine", "__version__"]
