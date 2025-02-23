import unittest
from spssnumpy import Array

class TestArray(unittest.TestCase):
    def test_array_creation(self):
        arr = Array([[1, 2], [3, 4]])
        self.assertEqual(arr.shape, (2, 2))
        self.assertEqual(arr.data, [[1, 2], [3, 4]])

    def test_elementwise_addition(self):
        a = Array([[1, 2], [3, 4]])
        b = Array([[5, 6], [7, 8]])
        result = a + b
        self.assertEqual(result.data, [[6, 8], [10, 12]])

    def test_elementwise_subtraction(self):
        a = Array([[1, 2], [3, 4]])
        b = Array([[5, 6], [7, 8]])
        result = a - b
        self.assertEqual(result.data, [[-4, -4], [-4, -4]])

    def test_matrix_multiplication(self):
        a = Array([[1, 2], [3, 4]])
        b = Array([[5, 6], [7, 8]])
        result = a.dot(b)
        self.assertEqual(result.data, [[19, 22], [43, 50]])

    def test_transpose(self):
        a = Array([[1, 2], [3, 4]])
        result = a.transpose()
        self.assertEqual(result.data, [[1, 3], [2, 4]])

    def test_reshape(self):
        a = Array([[1, 2, 3], [4, 5, 6]])
        result = a.reshape((3, 2))
        self.assertEqual(result.data, [[1, 2], [3, 4], [5, 6]])

    def test_flatten(self):
        a = Array([[1, 2], [3, 4]])
        result = a.flatten()
        self.assertEqual(result.data, [1, 2, 3, 4])

    def test_zeros(self):
        result = Array.zeros((2, 3))
        self.assertEqual(result.data, [[0, 0, 0], [0, 0, 0]])

    def test_ones(self):
        result = Array.ones((2, 3))
        self.assertEqual(result.data, [[1, 1, 1], [1, 1, 1]])

    def test_sum(self):
        a = Array([[1, 2], [3, 4]])
        self.assertEqual(a.sum(), 10)

    def test_mean(self):
        a = Array([[1, 2], [3, 4]])
        self.assertEqual(a.mean(), 2.5)

if __name__ == "__main__":
    unittest.main()