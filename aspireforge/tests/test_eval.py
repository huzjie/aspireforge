# -*- coding: utf-8 -*-
import unittest

from aspireforge.eval.metrics import success_rate, memory_hit_rate, mean_attempts
from aspireforge.engine import SolveResult


class TestEval(unittest.TestCase):
    def test_success_rate(self):
        rs = [SolveResult(success=True), SolveResult(success=False)]
        self.assertEqual(success_rate(rs), 0.5)

    def test_memory_hit(self):
        rs = [SolveResult(memory_hit=True), SolveResult(memory_hit=False)]
        self.assertEqual(memory_hit_rate(rs), 0.5)

    def test_attempts(self):
        rs = [SolveResult(attempts=2), SolveResult(attempts=4)]
        self.assertEqual(mean_attempts(rs), 3.0)


if __name__ == "__main__":
    unittest.main()
