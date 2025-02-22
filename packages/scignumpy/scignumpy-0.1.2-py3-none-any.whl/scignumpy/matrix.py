import numpy as np  # Add this line
from .array import Array

class Matrix(Array):
    def __init__(self, data):
        """
        Initialize a Matrix object with the given 2D data.
        :param data: A nested list representing the matrix.
        """
        super().__init__(data)
        if self.data.ndim != 2:
            raise ValueError("Matrix data must be 2D.")

    def transpose(self):
        """
        Return the transpose of the matrix.
        """
        return Matrix(self.data.T)

    def dot(self, other):
        """
        Perform matrix multiplication with another Matrix.
        :param other: Another Matrix object.
        """
        if not isinstance(other, Matrix):
            raise TypeError("Matrix multiplication requires another Matrix.")
        return Matrix(np.dot(self.data, other.data))

    def determinant(self):
        """
        Calculate the determinant of a square matrix.
        """
        if self.data.shape[0] != self.data.shape[1]:
            raise ValueError("Matrix must be square to calculate determinant.")
        return np.linalg.det(self.data)

    def inverse(self):
        """
        Compute the inverse of a square matrix.
        """
        if self.data.shape[0] != self.data.shape[1]:
            raise ValueError("Matrix must be square to compute inverse.")
        return Matrix(np.linalg.inv(self.data))