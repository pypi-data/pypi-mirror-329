from damakye_matrixsolver.methods import numpy_solver, gauss_jordan, gaussian_elimination, row_reduction, lu_decomposition

def solve_matrix(A, b, method="numpy"):
    """
    Solves the system of linear equations Ax = b using the selected method.
    
    Parameters:
    A (numpy.ndarray): The coefficient matrix.
    b (numpy.ndarray): The vector of constants.
    method (str): The method to use for solving the system ('numpy', 'gaussian', 'row_reduction', 'lu', 'gauss_jordan').
    
    Returns:
    numpy.ndarray: The solution vector x, or a message if the matrix is singular or not invertible.
    """
    if method == "numpy":
        return numpy_solver(A, b)
    elif method == "gauss_jordan":
        return gauss_jordan(A, b)
    elif method == "gaussian_elimination":
        return gaussian_elimination(A, b)
    elif method == "row_reduction":
        return row_reduction(A, b)
    elif method == "lu_decomposition":
        return lu_decomposition(A, b)
    else:
        raise ValueError("Invalid method selected. Please choose a valid method.")

def get_matrix_input():
    """Prompt the user to input the matrix and vector."""
    
    # Get the dimension of the matrix
    n = int(input("Enter the number of rows (and columns) for the square matrix (n x n): "))
    
    # Initialize matrix A and vector b
    A = []
    b = []
    
    # Get the matrix A values row by row
    print(f"Enter the matrix {n}x{n}:")
    for i in range(n):
        row = list(map(float, input(f"Enter row {i + 1} (space separated values): ").split()))
        A.append(row)
    
    # Get the vector b
    print(f"Enter the vector b (space separated values):")
    b = list(map(float, input().split()))
    
    return A, b

# Main function to integrate input, method selection, and solving
def main():
    # Get matrix and vector input
    A, b = get_matrix_input()

    # Ask the user to select a method
    print("Select a method to solve the matrix:")
    print("1. NumPy Solver")
    print("2. Gauss-Jordan Elimination")
    print("3. Gaussian Elimination")
    print("4. Row Reduction")
    print("5. LU Decomposition")
    
    method_choice = input("Enter the number corresponding to your choice: ")

    # Map the user's choice to the corresponding method string
    if method_choice == '1':
        method = 'numpy'
    elif method_choice == '2':
        method = 'gauss_jordan'
    elif method_choice == '3':
        method = 'gaussian_elimination'
    elif method_choice == '4':
        method = 'row_reduction'
    elif method_choice == '5':
        method = 'lu_decomposition'
    else:
        print("Invalid choice, using default method (NumPy solver).")
        method = 'numpy'

    # Solve the matrix with the selected method
    solution = solve_matrix(A, b, method)
    
    # Print the solution
    print("Solution:", solution)

if __name__ == "__main__":
    main()
