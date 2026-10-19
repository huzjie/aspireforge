# -*- coding: utf-8 -*-
import unittest

from aspireforge.config import Config
from aspireforge.model.mock import MockBackend
from aspireforge.robot.task import make_task
from aspireforge.oracle import program_correct


PRIMS = ["move_to", "grasp", "place", "push", "rotate", "open", "close", "wait"]


class TestMockBackend(unittest.TestCase):
    def test_skill_monotonic(self):
        cfg = Config()
        b = MockBackend(cfg)
        self.assertEqual(b.skill, 0.5)
        prev = b.skill
        for _ in range(10):
            b.train_step(lr=0.5)
            self.assertGreaterEqual(b.skill, prev)
            prev = b.skill
        self.assertGreater(b.skill, 0.99)

    def test_trained_generation_is_correct(self):
        cfg = Config()
        b = MockBackend(cfg)
        for _ in range(20):
            b.train_step(lr=0.5)
        for i in range(20):
            task = make_task("gen-%d" % i, PRIMS)
            prog = b.generate_program(task, [], "")
            self.assertTrue(program_correct(task.task_id, prog.code, PRIMS))


if __name__ == "__main__":
    unittest.main()
