# -*- coding: utf-8 -*-
import unittest

from aspireforge.utils.hashing import md5_hex, skill_id_of
from aspireforge.utils.stable import stable_bool, stable_float, stable_ints, stable_vector, cosine


class TestHashing(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(skill_id_of("x"), skill_id_of("x"))
        self.assertNotEqual(skill_id_of("x"), skill_id_of("y"))

    def test_md5(self):
        self.assertEqual(md5_hex(b""), "d41d8cd98f00b204e9800998ecf8427e")


class TestStable(unittest.TestCase):
    def test_determinism(self):
        self.assertEqual(stable_float("k"), stable_float("k"))
        self.assertEqual(stable_ints("k", 5, 0, 9), stable_ints("k", 5, 0, 9))
        self.assertEqual(stable_vector("k", 4), stable_vector("k", 4))

    def test_bool_probability(self):
        self.assertTrue(stable_bool("always", p=1.0))
        self.assertFalse(stable_bool("never", p=0.0))

    def test_cosine(self):
        self.assertAlmostEqual(cosine([1, 0], [1, 0]), 1.0, places=6)
        self.assertAlmostEqual(cosine([1, 0], [0, 1]), 0.0, places=6)
        self.assertAlmostEqual(cosine([0, 0], [1, 1]), 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
