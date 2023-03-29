import unittest
from vector import Vector

class TestVector(unittest.TestCase):
    def test_init(self):
        v = Vector(1, 2)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        
        with self.assertRaises(ValueError):
            v = Vector("1", "2")