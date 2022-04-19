import unittest
import sorting
from typing import List
from random import randint


def generate_test_data() -> List[int]:
    """Poor persons fuzzing"""

    tests = []

    for i in range(0, 10):
        test = []

        for j in range(0, 100):
            test.append(randint(0, 1_000_000))

        tests.append(test)

    return tests


class TestMergeSortAttributes(unittest.TestCase):

    def test_length(self):
        for test in generate_test_data():
            self.assertEqual(len(test), len(sorting.merge_sort(test)), "Input and output lengths do not match")

    def test_values_increment(self):
        for test in generate_test_data():
            test_sorted = sorting.merge_sort(test)
            for i in range(0, len(test_sorted)-1):
                self.assertTrue(test_sorted[i] <= test_sorted[i+1], "Number dont increment as they should")


if __name__ == '__main__':
    unittest.main()
