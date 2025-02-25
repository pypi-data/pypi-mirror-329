# damakye_matrixsolver/utils.py

def input_matrix_and_vector():
    """Prompts the user to input an n x n matrix and vector b."""
    n = int(input("Enter the size of the matrix (n x n): "))
    
    A = []
    print(f"Enter the {n}x{n} matrix row by row (space-separated values):")
    for i in range(n):
        row = list(map(float, input(f"Enter row {i+1}: ").split()))
        if len(row) != n:
            raise ValueError(f"Row {i+1} must have {n} elements.")
        A.append(row)
    
    b = list(map(float, input(f"Enter the vector b (space-separated values): ").split()))
    if len(b) != n:
        raise ValueError(f"Vector b must have {n} elements.")
    
    return A, b

def choose_method():
    """Prompts the user to choose their preferred solving method and returns the corresponding method."""
    print("Choose the preferred method to solve the system of linear equations:")
    print("1. NumPy (default)")
    print("2. Gaussian Elimination")
    print("3. Row Reduction")
    print("4. LU Decomposition")
    print("5. Gauss-Jordan Elimination")
    
    choice = input("Enter the number corresponding to your choice: ")
    
    method_map = {
        "1": "numpy",
        "2": "gaussian",
        "3": "row_reduction",
        "4": "lu",
        "5": "gauss_jordan"
    }
    
    return method_map.get(choice, "numpy")  # Default to NumPy if invalid input
