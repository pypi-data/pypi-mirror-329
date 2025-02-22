"""
Dividebyzero: A framework for handling singularities in numerical computations.
"""

import numpy as np
from .array import DimensionalArray
from .registry import ErrorRegistry, ErrorData
from .exceptions import DimensionalError, ReconstructionError
from . import numpy_compat  # This will register all numpy functions
from .numpy_registry import _numpy_functions, _numpy_attributes
from . import quantum
from . import linalg
from . import random
from . import fft  # Add FFT module
from .linalg import logm
import logging

# Create a module-level registry
_REGISTRY = ErrorRegistry()

# Add mathematical constants
pi = np.pi
e = np.e
inf = np.inf
nan = np.nan

# Add newaxis attribute
newaxis = None

# Add commonly used functions
zeros = lambda *args, **kwargs: array(np.zeros(*args, **kwargs))
ones = lambda *args, **kwargs: array(np.ones(*args, **kwargs))
eye = lambda *args, **kwargs: array(np.eye(*args, **kwargs))
zeros_like = lambda *args, **kwargs: array(np.zeros_like(*args, **kwargs))
ones_like = lambda *args, **kwargs: array(np.ones_like(*args, **kwargs))

# Add commonly used mathematical functions
abs = lambda x: array(np.abs(x.array if isinstance(x, DimensionalArray) else x))
sin = lambda x: array(np.sin(x.array if isinstance(x, DimensionalArray) else x))
cos = lambda x: array(np.cos(x.array if isinstance(x, DimensionalArray) else x))
tan = lambda x: array(np.tan(x.array if isinstance(x, DimensionalArray) else x))
exp = lambda x: array(np.exp(x.array if isinstance(x, DimensionalArray) else x))
log = lambda x: array(np.log(x.array if isinstance(x, DimensionalArray) else x))
sqrt = lambda x: array(np.sqrt(x.array if isinstance(x, DimensionalArray) else x))
linspace = lambda *args, **kwargs: array(np.linspace(*args, **kwargs))
arange = lambda *args, **kwargs: array(np.arange(*args, **kwargs))

# Add complex number functions
conj = lambda x: array(np.conj(x.array if isinstance(x, DimensionalArray) else x))
angle = lambda x: array(np.angle(x.array if isinstance(x, DimensionalArray) else x))
real = lambda x: array(np.real(x.array if isinstance(x, DimensionalArray) else x))
imag = lambda x: array(np.imag(x.array if isinstance(x, DimensionalArray) else x))

# Add array manipulation functions
sum = lambda x, *args, **kwargs: array(np.sum(x.array if isinstance(x, DimensionalArray) else x, *args, **kwargs))
where = lambda cond, x, y: array(np.where(
    cond.array if isinstance(cond, DimensionalArray) else cond,
    x.array if isinstance(x, DimensionalArray) else x,
    y.array if isinstance(y, DimensionalArray) else y
))
isnan = lambda x: array(np.isnan(x.array if isinstance(x, DimensionalArray) else x))
einsum = lambda subscripts, *operands: array(np.einsum(subscripts, *(
    x.array if isinstance(x, DimensionalArray) else x for x in operands
)))

# Add NumPy dtype aliases
float32 = np.float32
float64 = np.float64
int32 = np.int32
int64 = np.int64
uint8 = np.uint8
uint16 = np.uint16
uint32 = np.uint32
uint64 = np.uint64
complex64 = np.complex64
complex128 = np.complex128
bool_ = np.bool_

def get_registry():
    """Get the global error registry."""
    return _REGISTRY

def array(array_like, dtype=None):
    """Create a DimensionalArray."""
    return DimensionalArray(array_like, error_registry=_REGISTRY, dtype=dtype)

# Add all registered numpy functions to the module namespace
globals().update(_numpy_functions)
globals().update(_numpy_attributes)

# Build __all__ list
base_exports = [
    'array', 'zeros', 'ones', 'eye', 'zeros_like', 'ones_like',
    'DimensionalArray', 'ErrorRegistry', 'ErrorData',
    'DimensionalError', 'ReconstructionError',
    'get_registry', 'quantum', 'linalg', 'random', 'fft',  # Add fft to exports
    'pi', 'e', 'inf', 'nan', 'newaxis',
    'sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'logm',
    'linspace', 'arange', 'abs',
    'conj', 'angle', 'real', 'imag',  # Add complex functions
    'sum', 'where', 'isnan', 'einsum',
    'float32', 'float64', 'int32', 'int64',
    'uint8', 'uint16', 'uint32', 'uint64',
    'complex64', 'complex128', 'bool_', 'asnumpy'
]

__all__ = base_exports + [
    name for name in (_numpy_functions.keys() | _numpy_attributes.keys())
    if name not in base_exports
]

def set_log_level(level):
    """
    Set the logging level for the entire dividebyzero library.
    
    Args:
        level: The logging level to set. Can be a string ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
               or a corresponding integer value.
    """
    logger = logging.getLogger('dividebyzero')
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

# Set default logging level to WARNING
set_log_level(logging.WARNING)

def asnumpy(x):
    """Convert array to numpy array."""
    if isinstance(x, DimensionalArray):
        return x.array
    return np.asarray(x)