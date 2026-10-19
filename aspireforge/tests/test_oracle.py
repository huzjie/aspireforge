# -*- coding: utf-8 -*-
import unittest

from aspireforge.oracle import program_correct, program_primitives, task_primitives
from aspireforge.utils.codegen import render_program


PRIMS = ["move_to", "grasp", "place", "push", "rotate", "open", "close", "wait"]


class TestOracle(unittest.TestCase):
    def test_task_deterministic(self):
        self.assertEqual(task_primitives("t0", PRIMS), task_primitives("t0", PRIMS))

    def test_correct_program(self):
        req = task_primitives("t0", PRIMS)
        prog = render_program("t0", req).code
        self.assertTrue(program_correct("t0", prog, PRIMS))

    def test_missing_primitive(self):
        req = task_primitives("t0", PRIMS)
        if req:
            prog = render_program("t0", req[:-1]).code
            self.assertFalse(program_correct("t0", prog, PRIMS))

    def test_extract_primitives(self):
        code = "robot.move_to(t)\nrobot.grasp(t)"
        self.assertEqual(program_primitives(code, PRIMS), ["move_to", "grasp"])


if __name__ == "__main__":
    unittest.main()
