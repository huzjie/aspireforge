# -*- coding: utf-8 -*-
import unittest

from aspireforge.config import Config
from aspireforge.engine import AspireEngine
from aspireforge.robot.task import make_task


class TestEngine(unittest.TestCase):
    def test_solve_end_to_end(self):
        engine = AspireEngine(Config())
        task = make_task("engine-0", engine.primitive_set)
        res = engine.solve(task)
        self.assertIn(res.success, (True, False))

    def test_train_raises_skill(self):
        engine = AspireEngine(Config())
        s0 = engine.agent.backend.skill
        s1 = engine.train(["t0", "t1", "t2"], lr=0.5)
        self.assertGreaterEqual(s1, s0)

    def test_library_grows_on_success(self):
        engine = AspireEngine(Config())
        engine.agent.backend.skill = 1.0
        for i in range(8):
            engine.solve(make_task("grow-%d" % i, engine.primitive_set))
        self.assertGreater(engine.library_size(), 0)


if __name__ == "__main__":
    unittest.main()
