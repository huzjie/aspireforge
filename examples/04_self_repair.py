# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Show the failure-reflection loop repairing a failing program."""
from aspireforge.config import Config
from aspireforge.reflect.loop import SelfRepairLoop
from aspireforge.robot.task import make_task
from aspireforge.skill import MemorySkillLibrary

cfg = Config()
loop = SelfRepairLoop(cfg, library=MemorySkillLibrary())
task = make_task("repair-demo", cfg.robot.primitive_set)

result = loop.run(task)
print("task       :", task.task_id)
print("required   :", task.required_primitives)
print("success    :", result.success)
print("attempts   :", result.attempts)
print("failures   :", result.failure_history)
print("distilled  :", result.distilled_skills)
