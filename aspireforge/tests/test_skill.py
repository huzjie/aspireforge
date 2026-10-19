# -*- coding: utf-8 -*-
import unittest

from aspireforge.skill import MemorySkillLibrary, Skill, SkillProvenance, retrieve
from aspireforge.skill.retrieval import embed_task


class TestSkillLibrary(unittest.TestCase):
    def _skill(self, code, tags):
        from aspireforge.utils.hashing import skill_id_of
        return Skill(skill_id=skill_id_of(code), name="s", tags=tags, code=code,
                     embedding=embed_task(tags, "t"))

    def test_put_get(self):
        lib = MemorySkillLibrary()
        s = self._skill("robot.move_to(t)", ["move_to"])
        lib.put(s)
        self.assertEqual(lib.get(s.skill_id).code, s.code)
        self.assertEqual(len(lib), 1)

    def test_eviction(self):
        lib = MemorySkillLibrary(max_skills=2)
        for i in range(5):
            lib.put(self._skill("c%d" % i, ["t%d" % i]))
        self.assertEqual(len(lib), 2)

    def test_retrieval_by_tag(self):
        lib = MemorySkillLibrary()
        lib.put(self._skill("robot.grasp(t)", ["grasp", "kitchen"]))
        lib.put(self._skill("robot.move_to(t)", ["move_to", "warehouse"]))
        results = retrieve(lib, ["grasp"], "q", top_k=3)
        self.assertTrue(results)
        self.assertIn("grasp", results[0].skill.tags)


if __name__ == "__main__":
    unittest.main()
