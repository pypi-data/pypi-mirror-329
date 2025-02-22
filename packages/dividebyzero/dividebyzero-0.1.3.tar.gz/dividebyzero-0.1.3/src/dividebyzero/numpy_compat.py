"""
Numpy compatibility layer for dividebyzero.
Allows dbz to act as a complete drop-in replacement for numpy.
"""

import numpy as np
from functools import wraps
import inspect
import sys
from .numpy_registry import wrap_and_register_numpy_function, register_numpy_attribute

# Register numpy functions and attributes
for name in dir(np):
    if name.startswith('_'):
        continue
        
    obj = getattr(np, name)
    
    # For callable functions (but not classes or modules)
    if callable(obj) and not inspect.isclass(obj) and not inspect.ismodule(obj):
        try:
            wrap_and_register_numpy_function(obj)
        except (AttributeError, TypeError):
            continue
    else:
        # For non-callable attributes (dtypes, constants, etc.)
        try:
            register_numpy_attribute(name, obj)
            # Also add to module namespace
            setattr(sys.modules[__name__], name, obj)
        except (AttributeError, TypeError):
            continue

# Export everything
__all__ = [name for name in dir(np) if not name.startswith('_')] 