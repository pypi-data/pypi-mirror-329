from .matrix import Matrix

def determinant(matrix):
    """
    Calculate the determinant of a square matrix.
    :param matrix: A Matrix object representing a square matrix.
    :return: The determinant as a scalar value.
    """
    if not isinstance(matrix, Matrix):
        raise TypeError("Input must be a Matrix object.")
    
    # Ensure the matrix is square
    rows = len(matrix.data)
    cols = len(matrix.data[0])
    if rows != cols:
        raise ValueError("Matrix must be square to calculate determinant.")
    
    # Base case for 1x1 matrix
    if rows == 1:
        det = matrix.data[0][0]
        print(f"Determinant of 1x1 matrix {matrix.data}: {det}")
        return det
    
    # Base case for 2x2 matrix
    if rows == 2:
        det = matrix.data[0][0] * matrix.data[1][1] - matrix.data[0][1] * matrix.data[1][0]
        print(f"Determinant of 2x2 matrix {matrix.data}: {det}")
        return det
    
    # Recursive case for larger matrices
    det = 0
    for col in range(cols):
        # Create submatrix by removing the first row and current column
        submatrix_data = [
            [matrix.data[i][j] for j in range(cols) if j != col]
            for i in range(1, rows)
        ]
        
        # Skip empty submatrices (edge case handling)
        if not submatrix_data or not submatrix_data[0]:
            continue
        
        submatrix = Matrix(submatrix_data)
        print(f"Submatrix for col {col}: {submatrix.data}")
        
        # Calculate cofactor
        sub_det = determinant(submatrix)
        cofactor = (-1) ** col * matrix.data[0][col] * sub_det
        print(f"Cofactor for col {col}: {cofactor}")
        det += cofactor
    
    print(f"Determinant of matrix {matrix.data}: {det}")
    return det


def inverse(matrix):
    """
    Compute the inverse of a square matrix.
    :param matrix: A Matrix object representing a square matrix.
    :return: The inverse as a Matrix object.
    """
    if not isinstance(matrix, Matrix):
        raise TypeError("Input must be a Matrix object.")
    
    # Ensure the matrix is square
    rows = len(matrix.data)
    cols = len(matrix.data[0])
    if rows != cols:
        raise ValueError("Matrix must be square to compute inverse.")
    
    # Calculate determinant
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is singular and cannot be inverted.")
    
    # Compute adjugate (adjoint) matrix
    adjugate_data = []
    for i in range(rows):
        adjugate_row = []
        for j in range(cols):
            # Create submatrix by removing row i and column j
            submatrix_data = [
                [matrix.data[x][y] for y in range(cols) if y != j]
                for x in range(rows) if x != i
            ]
            
            # Handle edge cases where submatrix might be empty
            if not submatrix_data or not submatrix_data[0]:
                cofactor = 0
            else:
                submatrix = Matrix(submatrix_data)
                print(f"Submatrix for element ({i}, {j}): {submatrix.data}")
                
                sub_det = determinant(submatrix)
                cofactor = ((-1) ** (i + j)) * sub_det
                print(f"Cofactor for element ({i}, {j}): {cofactor}")
            
            adjugate_row.append(cofactor)
        adjugate_data.append(adjugate_row)
    
    print(f"Adjugate matrix before transpose: {adjugate_data}")
    
    # Transpose the adjugate matrix
    adjugate = Matrix(adjugate_data).transpose()
    print(f"Adjugate matrix after transpose: {adjugate.data}")
    
    # Divide each element by the determinant
    inverse_data = [[adjugate.data[i][j] / det for j in range(cols)] for i in range(rows)]
    print(f"Inverse matrix: {inverse_data}")
    return Matrix(inverse_data)