# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aspireforge.config import Config
from aspireforge.engine import AspireEngine
from aspireforge.robot.task import make_task
from aspireforge.eval.metrics import success_rate

cfg = Config()
# cold: fresh agent, skill 0.5, no library
cold = AspireEngine(cfg)
results = [cold.solve(make_task("cold-%d" % i, cfg.robot.primitive_set),
                     use_library=False, allow_repair=False) for i in range(64)]
print("cold-start success rate: %.3f" % success_rate(results))
