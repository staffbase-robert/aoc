import unittest
from day11 import rules
import random

class Test_move_tain(unittest.TestCase):
    def test_easy(self):
        self.assertTrue(rules[2](14))
        self.assertTrue(rules[2](10))
        self.assertTrue(rules[2](98))
        self.assertTrue(rules[2](420))

        self.assertFalse(rules[3](14))
        self.assertFalse(rules[3](10))
        self.assertFalse(rules[3](98))
        self.assertTrue(rules[3](420))

    def test_fuzz(self):
        for ti in rules:
            for _ in range(1000):
                i = random.randint(0,200000)
                want = i % ti == 0
                got = rules[ti](i)
                self.assertEqual(want, got, f"mismatch for {i} divided by {ti}, got {got}, want {want}")
if __name__ == '__main__':
    unittest.main()
