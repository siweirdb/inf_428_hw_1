import math
import unittest

def time_to_cyclic(hour):
    radians = (hour / 24) * 2 * math.pi  # Convert hour to radians
    return math.sin(radians), math.cos(radians)

class TestTimeToCyclic(unittest.TestCase):

    def test_midnight(self):
        sin, cos = time_to_cyclic(0)
        self.assertAlmostEqual(sin, 0.0, places=1)
        self.assertAlmostEqual(cos, 1.0, places=1)

    def test_noon(self):
        sin, cos = time_to_cyclic(12)
        self.assertAlmostEqual(sin, 0.0, places=1)
        self.assertAlmostEqual(cos, -1.0, places=1)

    def test_evening(self):
        sin, cos = time_to_cyclic(18)
        self.assertAlmostEqual(sin, -1.0, places=1)
        self.assertAlmostEqual(cos, 0.0, places=1)

    def test_wraparound(self):
        t1 = time_to_cyclic(23)
        t2 = time_to_cyclic(1)
        diff = math.acos(t1[0] * t2[0] + t1[1] * t2[1])  # Angle between vectors
        self.assertAlmostEqual(diff, (2 / 24) * 2 * math.pi, places=2)

    def test_wraparound_afternoon(self):
        t1 = time_to_cyclic(22)
        t2 = time_to_cyclic(2)
        diff = math.acos(t1[0] * t2[0] + t1[1] * t2[1])
        self.assertAlmostEqual(diff, (4 / 24) * 2 * math.pi, places=2)

    def test_difference_morning(self):
        t1 = time_to_cyclic(6)
        t2 = time_to_cyclic(9)
        diff = math.acos(t1[0] * t2[0] + t1[1] * t2[1])
        self.assertAlmostEqual(diff, (3 / 24) * 2 * math.pi, places=2)

    def test_difference_evening(self):
        t1 = time_to_cyclic(17)
        t2 = time_to_cyclic(21)
        diff = math.acos(t1[0] * t2[0] + t1[1] * t2[1])
        self.assertAlmostEqual(diff, (4 / 24) * 2 * math.pi, places=2)

if __name__ == "__main__":
    unittest.main()
