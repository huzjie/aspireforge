# -*- coding: utf-8 -*-
import unittest

from aspireforge.config import Config
from aspireforge.data.synth import generate_task_suite


class TestData(unittest.TestCase):
    def test_suite(self):
        suite = generate_task_suite(Config(), n_seen=8, n_unseen=8)
        self.assertEqual(len(suite["seen"]), 8)
        self.assertEqual(len(suite["unseen"]), 8)
        # unseen task mirrors seen primitives
        self.assertEqual(suite["unseen"][0].required_primitives,
                         suite["seen"][0].required_primitives)


if __name__ == "__main__":
    unittest.main()
