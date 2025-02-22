# Expose Array and Matrix from array.py and matrix.py
from .array import Array
from .matrix import Matrix

# Expose mathematical functions from math_functions.py
from .math_functions import sin, cos, tan, exp, log, sqrt

# Define what gets imported with "from scignumpy import *"
__all__ = ["Array", "Matrix", "sin", "cos", "tan", "exp", "log", "sqrt"]