import numpy as np
from scipy.linalg import lu

def numpy_solver(A, b):
    """Solves the system using NumPy's linear algebra solver."""
    A = np.array(A)
    b = np.array(b)
    try:
        return np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return "The matrix is singular or not invertible."


def gauss_jordan(A, b):
    """Solves the system of linear equations Ax = b using the Gauss-Jordan method (RREF)."""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    
    # Create augmented matrix [A | b]
    augmented_matrix = np.hstack([A, b.reshape(-1, 1)])
    
    # Perform Gaussian elimination
    for i in range(n):
        # Make the diagonal element 1
        augmented_matrix[i] /= augmented_matrix[i, i]
        
        # Eliminate the column above and below the pivot (Gauss-Jordan)
        for j in range(n):
            if i != j:
                factor = augmented_matrix[j, i]
                augmented_matrix[j] -= factor * augmented_matrix[i]
    
    # The solution is in the last column of the augmented matrix
    return augmented_matrix[:, -1]


def gaussian_elimination(A, b):
    """Solves the system of linear equations Ax = b using Gaussian elimination."""
    n = len(A)
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    
    # Forward elimination
    for i in range(n):
        # Pivot: find the row with the largest absolute value in the current column
        max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        for j in range(i + 1, n):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(i, n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Back substitution
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = augmented_matrix[i][-1] / augmented_matrix[i][i]
        for j in range(i - 1, -1, -1):
            augmented_matrix[j][-1] -= augmented_matrix[j][i] * solution[i]
    
    return solution


def row_reduction(A, b):
    """Solves the system of linear equations Ax = b using Row Reduction (Gaussian elimination with back substitution)."""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    
    # Create augmented matrix [A | b]
    augmented_matrix = np.hstack([A, b.reshape(-1, 1)])
    
    # Forward elimination
    for i in range(n):
        # Pivot: Find max element in column
        max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Make the diagonal element 1 by scaling the row
        augmented_matrix[i] /= augmented_matrix[i, i]
        
        # Eliminate the column below the pivot element
        for j in range(i + 1, n):
            factor = augmented_matrix[j, i]
            augmented_matrix[j] -= factor * augmented_matrix[i]
    
    # Back substitution
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = augmented_matrix[i, -1]  # The solution is in the last column
        for j in range(i - 1, -1, -1):
            augmented_matrix[j, -1] -= augmented_matrix[j, i] * solution[i]
    
    return solution


def lu_decomposition(A, b):
    """Solves the system of linear equations Ax = b using LU decomposition."""
    A = np.array(A)
    b = np.array(b)
    
    # Perform LU decomposition using scipy's lu function
    P, L, U = lu(A)
    
    # Solve Ly = b using forward substitution
    y = np.linalg.solve(L, b)
    
    # Solve Ux = y using back substitution
    x = np.linalg.solve(U, y)
    
    return x
