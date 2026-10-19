# -*- coding: utf-8 -*-
import unittest

from aspireforge.config import Config, default_config, load_config


class TestConfig(unittest.TestCase):
    def test_default(self):
        cfg = default_config()
        self.assertEqual(cfg.coder.model, "mock")
        self.assertGreater(cfg.skill.max_skills, 0)

    def test_from_dict(self):
        cfg = Config.from_dict({"coder": {"model": "openai"}, "skill_library_size": 99})
        self.assertEqual(cfg.coder.model, "openai")
        self.assertEqual(cfg.skill_library_size, 99)

    def test_load_default_yaml(self):
        cfg = load_config()
        self.assertIsInstance(cfg, Config)
        self.assertGreaterEqual(len(cfg.robot.primitive_set), 4)


if __name__ == "__main__":
    unittest.main()
