import unittest

from sweep import first_impact_orbit, parse_int_list


class SweepTests(unittest.TestCase):
    def test_first_impact_orbit(self):
        self.assertEqual(first_impact_orbit([0, 0, 2, 1]), 3)
        self.assertIsNone(first_impact_orbit([0, 0, 0]))

    def test_parse_int_list(self):
        self.assertEqual(parse_int_list("1, 2,3"), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
