# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aspireforge.config import Config
from aspireforge.engine import AspireEngine
from aspireforge.robot.task import make_task
from aspireforge.observability.metrics import MetricAccumulator

acc = MetricAccumulator()
engine = AspireEngine(Config())
engine.agent.backend.skill = 1.0
for i in range(24):
    acc.record(engine.solve(make_task("m-%d" % i, engine.primitive_set)))

import json
print(json.dumps(acc.summary(), ensure_ascii=False, indent=2))
