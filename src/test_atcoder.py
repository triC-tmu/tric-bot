import unittest

from atcoder import get_problems_difficulty


class TestAtCoder(unittest.TestCase):
    def test_get_problems_difficulty(self):
        problem_list = ["abc138_a", "abc138_b", "abc138_c", "abc138_d", "pakencamp_2018_day2_a"]
        expected_output = {
            "abc138_a": 18,
            "abc138_b": 59,
            "abc138_c": 116,
            "abc138_d": 920,
            "pakencamp_2018_day2_a": None
        }
        self.assertEqual(get_problems_difficulty(problem_list), expected_output)


if __name__ == "__main__":
    unittest.main()
