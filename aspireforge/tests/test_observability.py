# -*- coding: utf-8 -*-
import unittest

from aspireforge.engine import SolveResult
from aspireforge.observability.metrics import MetricAccumulator


class TestObservability(unittest.TestCase):
    def test_summary(self):
        acc = MetricAccumulator()
        acc.record(SolveResult(success=True, memory_hit=True, attempts=1,
                               failure_history=["grasp_failure"]))
        acc.record(SolveResult(success=False, memory_hit=False, attempts=3,
                               failure_history=["goal_not_reached"]))
        s = acc.summary()
        self.assertEqual(s["solves"], 2)
        self.assertEqual(s["success_rate"], 0.5)
        self.assertEqual(s["failure_classes"]["grasp_failure"], 1)


if __name__ == "__main__":
    unittest.main()
