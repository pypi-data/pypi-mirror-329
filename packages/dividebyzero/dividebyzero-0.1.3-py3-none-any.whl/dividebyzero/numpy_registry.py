"""
Registry for numpy function compatibility.
"""

import numpy as np
from typing import Optional, Dict, Callable, Any
from functools import wraps
from numpy import dtype as np_dtype

_numpy_functions: Dict[str, Callable] = {}
_numpy_attributes: Dict[str, Any] = {}

def register_numpy_attribute(name: str, value: Any) -> None:
    """Register a numpy attribute (like dtypes, constants)."""
    if isinstance(value, np_dtype):
        # For dtype objects, store the actual type
        _numpy_attributes[name] = value.type
    else:
        _numpy_attributes[name] = value

def register_numpy_function(name: str, func: Callable) -> None:
    """Register a numpy function with its wrapped version."""
    _numpy_functions[name] = func

def get_numpy_attribute(name: str) -> Optional[Any]:
    """Get a registered numpy attribute if it exists."""
    return _numpy_attributes.get(name)

def get_numpy_function(name: str) -> Optional[Callable]:
    """Get the wrapped version of a numpy function if it exists."""
    return _numpy_functions.get(name)

def wrap_and_register_numpy_function(np_func: Callable) -> Callable:
    """Decorator to wrap and register a numpy function."""
    from .array import DimensionalArray
    
    @wraps(np_func)
    def wrapper(*args, **kwargs):
        # Handle dtype conversion for numpy types
        if 'dtype' in kwargs and isinstance(kwargs['dtype'], type) and issubclass(kwargs['dtype'], np.generic):
            kwargs['dtype'] = kwargs['dtype']
        
        # Convert dbz arrays to numpy arrays for input
        args = [(arg.array if isinstance(arg, DimensionalArray) else arg) for arg in args]
        kwargs = {k: (v.array if isinstance(v, DimensionalArray) else v) for k, v in kwargs.items()}
        
        # Call original numpy function
        result = np_func(*args, **kwargs)
        
        # Convert result back to dbz array
        if isinstance(result, np.ndarray):
            return DimensionalArray(result)
        elif isinstance(result, tuple):
            return tuple(DimensionalArray(r) if isinstance(r, np.ndarray) else r for r in result)
        return result
    
    register_numpy_function(np_func.__name__, wrapper)
    return wrapper 