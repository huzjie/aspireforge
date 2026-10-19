# -*- coding: utf-8 -*-
import unittest

from aspireforge.reflect.failure import FAILURE_CLASSES, FailureAnalyzer
from aspireforge.robot.task import make_task
from aspireforge.utils.codegen import render_program


PRIMS = ["move_to", "grasp", "place", "push", "rotate", "open", "close", "wait"]


class TestFailureAnalyzer(unittest.TestCase):
    def test_classifies_missing(self):
        an = FailureAnalyzer(PRIMS)
        task = make_task("fail-0", PRIMS)
        if not task.required_primitives:
            return
        prog = render_program("fail-0", task.required_primitives[:-1]).code
        report = an.analyze(task, prog)
        self.assertIn(report.failure_class, FAILURE_CLASSES)
        self.assertTrue(report.missing_primitives)


if __name__ == "__main__":
    unittest.main()
