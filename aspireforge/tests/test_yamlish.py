# -*- coding: utf-8 -*-
import unittest

from aspireforge.utils.yamlish import parse


class TestYamlish(unittest.TestCase):
    def test_scalars(self):
        d = parse("a: 1\nb: hello\nc: true\nd: 2.5")
        self.assertEqual(d["a"], 1)
        self.assertEqual(d["b"], "hello")
        self.assertEqual(d["c"], True)
        self.assertEqual(d["d"], 2.5)

    def test_nested(self):
        d = parse("coder:\n  model: mock\n  temperature: 0.0")
        self.assertEqual(d["coder"]["model"], "mock")

    def test_block_list(self):
        d = parse("primitive_set:\n  - move_to\n  - grasp\n  - place")
        self.assertEqual(d["primitive_set"], ["move_to", "grasp", "place"])

    def test_inline_list(self):
        d = parse("failure_classes: [collision, timing_error]")
        self.assertEqual(d["failure_classes"], ["collision", "timing_error"])

    def test_comment(self):
        d = parse("model: mock  # the backend")
        self.assertEqual(d["model"], "mock")


if __name__ == "__main__":
    unittest.main()
