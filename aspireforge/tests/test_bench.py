# -*- coding: utf-8 -*-
import unittest

from aspireforge.config import Config
from aspireforge.train_bench import summarize
from aspireforge.train_bench.bench import run_repair_effect, run_skill_effect, run_zero_shot


class TestBench(unittest.TestCase):
    def test_summarize(self):
        s = summarize(Config())
        self.assertIn("skill_effect", s)

    def test_skill_effect_monotonic(self):
        d = run_skill_effect(Config())
        vals = [d[k] for k in sorted(d)]
        self.assertTrue(all(b >= a for a, b in zip(vals, vals[1:])))

    def test_zero_shot_warm_beats_cold(self):
        d = run_zero_shot(Config())
        self.assertGreaterEqual(d["warm_zero_shot"], d["cold_zero_shot"])

    def test_repair_lifts(self):
        d = run_repair_effect(Config())
        self.assertGreaterEqual(d["repair"], d["naive"])


if __name__ == "__main__":
    unittest.main()
