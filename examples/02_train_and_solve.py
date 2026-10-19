# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Train the mock skill toward 1.0 and watch the success rate climb."""
from aspireforge.config import Config
from aspireforge.engine import AspireEngine
from aspireforge.robot.task import make_task

engine = AspireEngine(Config())

def success_rate(engine, n=60):
    ok = 0
    for i in range(n):
        r = engine.solve(make_task("eval-%d" % i, engine.primitive_set),
                         use_library=False, allow_repair=False)
        ok += int(r.success)
    return ok / n

print("before training: success_rate=%.3f" % success_rate(engine))
for _ in range(8):
    engine.train(["train-%d" % i for i in range(8)], lr=0.3)
print("after training : success_rate=%.3f" % success_rate(engine))
