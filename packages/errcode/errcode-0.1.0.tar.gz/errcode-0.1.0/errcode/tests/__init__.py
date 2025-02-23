from errcode import max_size
import unittest

class TestMaxSize(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(max_size(arity=[], correct=0, detect=0), 1)
        self.assertEqual(max_size(arity=[], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[], correct=1, detect=1), 1)

    def test_one(self):
        self.assertEqual(max_size(arity=[2], correct=0, detect=0), 2)
        self.assertEqual(max_size(arity=[2], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[2], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[-2], correct=0, detect=0), 1)
        self.assertEqual(max_size(arity=[-2], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[-2], correct=1, detect=1), 1)

    def test_two(self):
        self.assertEqual(max_size(arity=[2, 3], correct=0, detect=0), 6)
        self.assertEqual(max_size(arity=[2, 3], correct=0, detect=1), 2)
        self.assertEqual(max_size(arity=[2, 3], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[2, -3], correct=0, detect=0), 2)
        self.assertEqual(max_size(arity=[2, -3], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[2, -3], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, 3], correct=0, detect=0), 3)
        self.assertEqual(max_size(arity=[-2, 3], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, 3], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, -3], correct=0, detect=0), 1)
        self.assertEqual(max_size(arity=[-2, -3], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, -3], correct=1, detect=1), 1)

    def test_three(self):
        self.assertEqual(max_size(arity=[2, 3, 4], correct=0, detect=0), 24)
        self.assertEqual(max_size(arity=[2, 3, 4], correct=0, detect=1), 6)
        self.assertEqual(max_size(arity=[2, 3, 4], correct=1, detect=1), 2)
        self.assertEqual(max_size(arity=[2, 3, 4], correct=1, detect=2), 1)
        self.assertEqual(max_size(arity=[2, 3, 4], correct=2, detect=2), 1)
        self.assertEqual(max_size(arity=[2, 3, -4], correct=0, detect=0), 6)
        self.assertEqual(max_size(arity=[2, 3, -4], correct=0, detect=1), 2)
        self.assertEqual(max_size(arity=[2, 3, -4], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[2, -3, 4], correct=0, detect=0), 8)
        self.assertEqual(max_size(arity=[2, -3, 4], correct=0, detect=1), 2)
        self.assertEqual(max_size(arity=[2, -3, 4], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[2, -3, -4], correct=0, detect=0), 2)
        self.assertEqual(max_size(arity=[2, -3, -4], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[2, -3, -4], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, 3, 4], correct=0, detect=0), 12)
        self.assertEqual(max_size(arity=[-2, 3, 4], correct=0, detect=1), 3)
        self.assertEqual(max_size(arity=[-2, 3, 4], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, 3, -4], correct=0, detect=0), 3)
        self.assertEqual(max_size(arity=[-2, 3, -4], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, 3, -4], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, -3, 4], correct=0, detect=0), 4)
        self.assertEqual(max_size(arity=[-2, -3, 4], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, -3, 4], correct=1, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, -3, -4], correct=0, detect=0), 1)
        self.assertEqual(max_size(arity=[-2, -3, -4], correct=0, detect=1), 1)
        self.assertEqual(max_size(arity=[-2, -3, -4], correct=1, detect=1), 1)

    def test_forward_qnd(self):
        self.assertEqual(max_size(arity=2, repeat=10, detect=3), 40)
        self.assertEqual(max_size(arity=2, repeat=11, correct=1), 144)
        self.assertEqual(max_size(arity=2, repeat=13, detect=5), 32)
        self.assertEqual(max_size(arity=2, repeat=14, correct=3), 16)

    def test_forward_twothree(self):
        self.assertEqual(max_size(arity=[2, 2, 3, 3, 3], correct=1), 9)
        self.assertEqual(max_size(arity=[2, 2, 2, 2, 3, 3, 3], correct=1), 28)


if __name__ == '__main__':
    unittest.main()