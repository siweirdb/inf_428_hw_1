def cyclic_time_difference(hour1: int, hour2: int):
    diff = abs(hour1 - hour2)
    return min(diff, 24 - diff)


import unittest


class TestCyclicTimeDifference(unittest.TestCase):

    def test_cyclic_time_difference(self):

        self.assertEqual(cyclic_time_difference(23, 1), 2)
        self.assertEqual(cyclic_time_difference(0, 12), 12)
        self.assertEqual(cyclic_time_difference(6, 18), 12)
        self.assertEqual(cyclic_time_difference(3, 15), 12)

        self.assertEqual(cyclic_time_difference(0, 0), 0)
        self.assertEqual(cyclic_time_difference(5, 5), 0)
        self.assertEqual(cyclic_time_difference(23, 23), 0)
        self.assertEqual(cyclic_time_difference(0, 23), 1)


if __name__ == "__main__":
    unittest.main()
