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

    def _broadcast(self, other):
        """
        Broadcast two arrays to compatible shapes for element-wise operations.
        :param other: Another Array or scalar value.
        :return: Two NumPy arrays with compatible shapes.
        """
        if isinstance(other, Array):
            return np.broadcast_arrays(self.data, other.data)
        else:
            return self.data, np.full_like(self.data, other)

    def __getitem__(self, index):
        """
        Enable indexing and slicing to access elements of the array.
        :param index: The index or slice to retrieve.
        """
        result = self.data[index]
        if isinstance(result, np.ndarray):
            return Array(result)
        return result

    def __setitem__(self, index, value):
        """
        Enable assignment to modify elements of the array.
        :param index: The index to modify.
        :param value: The new value to assign.
        """
        self.data[index] = value

    def __add__(self, other):
        """
        Enable element-wise addition with another Array or a scalar.
        :param other: Another Array or a scalar value.
        """
        self_data, other_data = self._broadcast(other)
        return Array(self_data + other_data)

    def __sub__(self, other):
        """
        Enable element-wise subtraction with another Array or a scalar.
        :param other: Another Array or a scalar value.
        """
        self_data, other_data = self._broadcast(other)
        return Array(self_data - other_data)

    def __mul__(self, other):
        """
        Enable element-wise multiplication with another Array or a scalar.
        :param other: Another Array or a scalar value.
        """
        self_data, other_data = self._broadcast(other)
        return Array(self_data * other_data)

    def __truediv__(self, other):
        """
        Enable element-wise division with another Array or a scalar.
        :param other: Another Array or a scalar value.
        """
        self_data, other_data = self._broadcast(other)
        return Array(self_data / other_data)

    def sum(self, axis=None):
        """
        Compute the sum of elements along a specified axis.
        :param axis: The axis along which to compute the sum.
        """
        return self.data.sum(axis=axis)

    def mean(self, axis=None):
        """
        Compute the mean of elements along a specified axis.
        :param axis: The axis along which to compute the mean.
        """
        return self.data.mean(axis=axis)

    def min(self, axis=None):
        """
        Compute the minimum of elements along a specified axis.
        :param axis: The axis along which to compute the minimum.
        """
        return self.data.min(axis=axis)

    def max(self, axis=None):
        """
        Compute the maximum of elements along a specified axis.
        :param axis: The axis along which to compute the maximum.
        """
        return self.data.max(axis=axis)