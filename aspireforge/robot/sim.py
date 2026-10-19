# -*- coding: utf-8 -*-
"""Deterministic robot simulator.

The simulator does not simulate physics; it deterministically evaluates whether the
program the agent generated satisfies the task's required primitive sequence. This
keeps the reference implementation dependency-free while still producing a clean,
monotonic success signal shared with the benchmarks.
"""
from __future__ import annotations

from typing import List, Optional

from ..oracle import program_correct_for
from .task import Task
from .trajectory import Step, Trajectory


class Simulator:
    """Deterministic stand-in for a physics engine."""

    def __init__(self, primitive_set: Optional[List[str]] = None):
        from ..config import default_config
        self.primitive_set = primitive_set or default_config().robot.primitive_set

    def reset(self, task: Task) -> Observation:
        from .observation import Observation
        from ..utils.stable import stable_vector
        obs = Observation(
            state=stable_vector("obs:" + task.task_id, 8, 0.0, 1.0),
            objects=["obj-%d" % i for i in range(3)],
            goal=task.instruction,
            step=0,
        )
        return obs

    def run(self, task: Task, program_code: str) -> Trajectory:
        """Execute a program against a task, recording a trajectory.

        The success flag is :func:`oracle.program_correct`, shared with benchmarks.
        """
        success = program_correct_for(task.required_primitives, program_code, self.primitive_set)
        n_steps = 1 if success else 1 + (len(task.required_primitives) - len(
            [p for p in task.required_primitives if p + "(" in program_code]))
        traj = Trajectory(task_id=task.task_id, success=success)
        for s in range(max(1, n_steps)):
            from .observation import Observation
            from ..utils.stable import stable_vector
            obs = Observation(
                state=stable_vector("obs:%s:%d" % (task.task_id, s), 8, 0.0, 1.0),
                objects=["obj-%d" % i for i in range(3)],
                goal=task.instruction,
                step=s,
            )
            traj.steps.append(Step(step=s, observation=obs, action="primitive"))
        return traj
