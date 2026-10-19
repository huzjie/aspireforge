# -*- coding: utf-8 -*-
import unittest

from aspireforge.config import Config
from aspireforge.distill.skill_distill import SkillDistiller
from aspireforge.robot.sim import Simulator
from aspireforge.robot.task import make_task
from aspireforge.utils.codegen import render_program
from aspireforge.utils.serialize import skill_from_json, skill_to_json, task_from_json, task_to_json


class TestSerialize(unittest.TestCase):
    def test_task_roundtrip(self):
        task = make_task("ser-0", Config().robot.primitive_set)
        self.assertEqual(task_from_json(task_to_json(task)).task_id, task.task_id)

    def test_skill_roundtrip(self):
        cfg = Config()
        task = make_task("ser-1", cfg.robot.primitive_set)
        prog = render_program("ser-1", task.required_primitives)
        sim = Simulator(cfg.robot.primitive_set)
        skill = SkillDistiller(cfg).distill(task, prog, sim.run(task, prog.code))
        self.assertEqual(skill_from_json(skill_to_json(skill)).skill_id, skill.skill_id)


if __name__ == "__main__":
    unittest.main()
