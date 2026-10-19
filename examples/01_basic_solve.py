# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Minimal example: solve a single task with the default (mock) engine."""
from aspireforge.config import Config
from aspireforge.engine import AspireEngine
from aspireforge.robot.task import make_task

engine = AspireEngine(Config())
task = make_task("demo-0", engine.primitive_set)
result = engine.solve(task)

print("task          :", task.task_id)
print("instruction   :", task.instruction)
print("required      :", task.required_primitives)
print("success       :", result.success)
print("attempts      :", result.attempts)
print("memory_hit    :", result.memory_hit)
print("failure path  :", result.failure_history)
