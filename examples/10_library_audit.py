# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aspireforge.config import Config
from aspireforge.engine import AspireEngine
from aspireforge.robot.task import make_task

engine = AspireEngine(Config())
engine.agent.backend.skill = 1.0
for i in range(16):
    engine.solve(make_task("audit-%d" % i, engine.primitive_set))

for s in engine.library.all():
    print("%-32s verified=%s attempts=%d src=%s" % (
        s.name[:32], s.provenance.verified, s.provenance.attempts, s.provenance.source_task_id))
