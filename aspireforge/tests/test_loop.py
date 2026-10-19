# -*- coding: utf-8 -*-
import unittest

from aspireforge.config import Config
from aspireforge.reflect.loop import SelfRepairLoop
from aspireforge.robot.task import make_task
from aspireforge.skill import MemorySkillLibrary


class TestSelfRepairLoop(unittest.TestCase):
    def test_loop_runs(self):
        cfg = Config()
        lib = MemorySkillLibrary()
        loop = SelfRepairLoop(cfg, library=lib)
        task = make_task("loop-0", cfg.robot.primitive_set)
        result = loop.run(task)
        self.assertGreaterEqual(result.attempts, 1)
        if result.success:
            self.assertTrue(result.distilled_skills)


if __name__ == "__main__":
    unittest.main()
