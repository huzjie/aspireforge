# -*- coding: utf-8 -*-
import unittest

from aspireforge.config import Config
from aspireforge.distill.skill_distill import SkillDistiller
from aspireforge.robot.task import make_task
from aspireforge.robot.sim import Simulator
from aspireforge.utils.codegen import render_program


class TestDistill(unittest.TestCase):
    def test_distill(self):
        cfg = Config()
        d = SkillDistiller(cfg)
        task = make_task("d-0", cfg.robot.primitive_set)
        prog = render_program("d-0", task.required_primitives)
        sim = Simulator(cfg.robot.primitive_set)
        traj = sim.run(task, prog.code)
        self.assertTrue(traj.success)
        skill = d.distill(task, prog, traj)
        self.assertTrue(skill.provenance.verified)
        self.assertEqual(skill.provenance.source_task_id, "d-0")


if __name__ == "__main__":
    unittest.main()
