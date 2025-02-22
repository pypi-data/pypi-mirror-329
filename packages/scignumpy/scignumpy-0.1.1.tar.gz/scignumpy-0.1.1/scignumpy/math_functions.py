import numpy as np
from .array import Array
from .matrix import Matrix

def sin(obj):
    """
    Apply the sine function element-wise to an Array or Matrix.
    :param obj: An Array or Matrix object.
    :return: A new Array or Matrix with sine values.
    """
    if isinstance(obj, Array):
        return Array(np.sin(obj.data))
    elif isinstance(obj, Matrix):
        return Matrix(np.sin(obj.data))
    else:
        raise TypeError("Input must be an Array or Matrix object.")

def cos(obj):
    """
    Apply the cosine function element-wise to an Array or Matrix.
    :param obj: An Array or Matrix object.
    :return: A new Array or Matrix with cosine values.
    """
    if isinstance(obj, Array):
        return Array(np.cos(obj.data))
    elif isinstance(obj, Matrix):
        return Matrix(np.cos(obj.data))
    else:
        raise TypeError("Input must be an Array or Matrix object.")

def tan(obj):
    """
    Apply the tangent function element-wise to an Array or Matrix.
    :param obj: An Array or Matrix object.
    :return: A new Array or Matrix with tangent values.
    """
    if isinstance(obj, Array):
        return Array(np.tan(obj.data))
    elif isinstance(obj, Matrix):
        return Matrix(np.tan(obj.data))
    else:
        raise TypeError("Input must be an Array or Matrix object.")

def exp(obj):
    """
    Apply the exponential function element-wise to an Array or Matrix.
    :param obj: An Array or Matrix object.
    :return: A new Array or Matrix with exponential values.
    """
    if isinstance(obj, Array):
        return Array(np.exp(obj.data))
    elif isinstance(obj, Matrix):
        return Matrix(np.exp(obj.data))
    else:
        raise TypeError("Input must be an Array or Matrix object.")

def log(obj):
    """
    Apply the natural logarithm function element-wise to an Array or Matrix.
    :param obj: An Array or Matrix object.
    :return: A new Array or Matrix with natural logarithm values.
    """
    if isinstance(obj, Array):
        return Array(np.log(obj.data))
    elif isinstance(obj, Matrix):
        return Matrix(np.log(obj.data))
    else:
        raise TypeError("Input must be an Array or Matrix object.")

def sqrt(obj):
    """
    Apply the square root function element-wise to an Array or Matrix.
    :param obj: An Array or Matrix object.
    :return: A new Array or Matrix with square root values.
    """
    if isinstance(obj, Array):
        return Array(np.sqrt(obj.data))
    elif isinstance(obj, Matrix):
        return Matrix(np.sqrt(obj.data))
    else:
        raise TypeError("Input must be an Array or Matrix object.")