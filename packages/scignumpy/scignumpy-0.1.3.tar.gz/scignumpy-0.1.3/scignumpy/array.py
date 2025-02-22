# scignumpy/array.py

import numpy as np

class Array:
    def __init__(self, data):
        """
        Initialize an Array object with the given data.
        :param data: A list or nested list representing the array.
        """
        if isinstance(data, list):
            self.data = np.array(data, dtype=float)  # Use NumPy for contiguous memory
        elif isinstance(data, np.ndarray):
            self.data = data
        else:
            raise TypeError("Input must be a list or NumPy array.")

    def __repr__(self):
        """
        Return a string representation of the array.
        """
        return f"Array({self.data.tolist()})"

    @property
    def T(self):
        """
        Transpose the Array (swap rows and columns).
        """
        return Array(self.data.T)

    # Existing methods (__add__, __sub__, etc.) remain unchanged...