# -*- coding: utf-8 -*-
"""Robot world: task definitions, observations, deterministic simulator, trajectories.

The simulator is a deterministic, zero-dependency stand-in for a physics engine. Its
success signal is shared with the benchmarks through :mod:`aspireforge.oracle`, so a
fully-trained agent always succeeds and a random one hits the random baseline.
"""
from .task import Task, make_task
from .observation import Observation
from .sim import Simulator
from .trajectory import Trajectory, Step

__all__ = ["Task", "make_task", "Observation", "Simulator", "Trajectory", "Step"]
