# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Use a named backend and a custom config."""
from aspireforge.config import Config
from aspireforge.engine import AspireEngine
from aspireforge.robot.task import make_task
from aspireforge.model import list_backends

print("backends:", list_backends())

cfg = Config()
cfg.coder.model = "openai"   # degrades to mock when no key is set
engine = AspireEngine(cfg, backend_name="openai")
task = make_task("custom-0", engine.primitive_set)
print("solve:", engine.solve(task).to_dict())
