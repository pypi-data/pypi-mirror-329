# tests/test_solver.py

import unittest
import numpy as np
from matrix_solver import solve_matrix

class TestMatrixSolverMethods(unittest.TestCase):

    def test_numpy_solver(self):
        A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        b = [8, -11, -3]
        result = solve_matrix(A, b, method="numpy")
        expected = np.array([2.0, 3.0, -1.0])
        np.testing.assert_almost_equal(result, expected)

    def test_gauss_jordan(self):
        A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        b = [8, -11, -3]
        result = solve_matrix(A, b, method="gauss_jordan")
        expected = np.array([2.0, 3.0, -1.0])
        np.testing.assert_almost_equal(result, expected)

# Add tests for other methods (Gaussian, Row Reduction, LU Decomposition)
