# -*- coding: utf-8 -*-
import unittest

from aspireforge.integrations.langchain import make_skill_tool
from aspireforge.integrations.llamaindex import SkillRetriever


class TestIntegrations(unittest.TestCase):
    def test_langchain_tool(self):
        tool = make_skill_tool()
        out = tool("demo-0")
        self.assertIn("success", out)

    def test_llamaindex_retriever(self):
        r = SkillRetriever()
        results = r.retrieve("move_to grasp")
        self.assertIsInstance(results, list)


if __name__ == "__main__":
    unittest.main()
