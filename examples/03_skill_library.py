# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Demonstrate the skill library: solve seen tasks, then retrieve skills."""
from aspireforge.config import Config
from aspireforge.engine import AspireEngine
from aspireforge.robot.task import make_task
from aspireforge.skill import retrieve

engine = AspireEngine(Config())
engine.agent.backend.skill = 1.0

for i in range(12):
    engine.solve(make_task("seen-%d" % i, engine.primitive_set))

print("library size:", engine.library_size())
task = make_task("seen-3", engine.primitive_set)
results = retrieve(engine.library, task.tags, task.task_id, top_k=3)
for r in results:
    print("  skill=%-32s tags=%s score=%.2f" % (r.skill.name[:32], r.skill.tags, r.score))
