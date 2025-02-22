"""
FFT module for dividebyzero, providing numpy-compatible FFT functions.
"""

import numpy as np
from .array import DimensionalArray

def fft2(x):
    """2D FFT."""
    if isinstance(x, DimensionalArray):
        x = x.array
    return DimensionalArray(np.fft.fft2(x))

def ifft2(x):
    """Inverse 2D FFT."""
    if isinstance(x, DimensionalArray):
        x = x.array
    return DimensionalArray(np.fft.ifft2(x))

def fftshift(x):
    """Shift zero-frequency component to center of spectrum."""
    if isinstance(x, DimensionalArray):
        x = x.array
    return DimensionalArray(np.fft.fftshift(x))

def ifftshift(x):
    """Inverse shift zero-frequency component to center of spectrum."""
    if isinstance(x, DimensionalArray):
        x = x.array
    return DimensionalArray(np.fft.ifftshift(x))

def fftfreq(n, d=1.0):
    """Return the Discrete Fourier Transform sample frequencies."""
    return DimensionalArray(np.fft.fftfreq(n, d))

def rfft2(x):
    """2D Real FFT."""
    if isinstance(x, DimensionalArray):
        x = x.array
    return DimensionalArray(np.fft.rfft2(x))

def irfft2(x):
    """Inverse 2D Real FFT."""
    if isinstance(x, DimensionalArray):
        x = x.array
    return DimensionalArray(np.fft.irfft2(x))

def rfftfreq(n, d=1.0):
    """Return the Real FFT sample frequencies."""
    return DimensionalArray(np.fft.rfftfreq(n, d))

__all__ = [
    'fft2', 'ifft2', 'fftshift', 'ifftshift', 'fftfreq',
    'rfft2', 'irfft2', 'rfftfreq'
] 