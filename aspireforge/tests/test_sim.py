# -*- coding: utf-8 -*-
import unittest

from aspireforge.robot.sim import Simulator
from aspireforge.robot.task import make_task
from aspireforge.utils.codegen import render_program


PRIMS = ["move_to", "grasp", "place", "push", "rotate", "open", "close", "wait"]


class TestSimulator(unittest.TestCase):
    def test_success_and_failure(self):
        sim = Simulator(PRIMS)
        task = make_task("sim-0", PRIMS)
        good = render_program("sim-0", task.required_primitives).code
        self.assertTrue(sim.run(task, good).success)
        bad = render_program("sim-0", []).code
        if task.required_primitives:
            self.assertFalse(sim.run(task, bad).success)


if __name__ == "__main__":
    unittest.main()
