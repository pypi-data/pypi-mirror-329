"""Random number generation with DimensionalArray support."""

import numpy as np
from .array import DimensionalArray
from typing import Optional, Tuple, Union, Any

def rand(*args) -> DimensionalArray:
    """Random values in a given shape.
    
    Create an array of the given shape and populate it with random
    samples from a uniform distribution over [0, 1).
    """
    return DimensionalArray(np.random.rand(*args))

def randn(*args) -> DimensionalArray:
    """Return a sample (or samples) from the "standard normal" distribution."""
    return DimensionalArray(np.random.randn(*args))

def randint(low: int, high: Optional[int] = None, size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Return random integers from low (inclusive) to high (exclusive)."""
    return DimensionalArray(np.random.randint(low, high, size))

def random(size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Return random floats in the half-open interval [0.0, 1.0)."""
    return DimensionalArray(np.random.random(size))

def normal(loc: float = 0.0, scale: float = 1.0, size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Draw random samples from a normal (Gaussian) distribution."""
    return DimensionalArray(np.random.normal(loc, scale, size))

def uniform(low: float = 0.0, high: float = 1.0, size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Draw samples from a uniform distribution."""
    return DimensionalArray(np.random.uniform(low, high, size))

def multivariate_normal(mean, cov, size: Optional[int] = None) -> DimensionalArray:
    """Draw random samples from a multivariate normal distribution.
    
    Parameters
    ----------
    mean : array_like
        Mean of the distribution (1-D array-like)
    cov : array_like
        Covariance matrix of the distribution (2-D array-like)
    size : int, optional
        Number of samples to draw (default: 1)
        
    Returns
    -------
    DimensionalArray
        Drawn samples from the multivariate normal distribution.
    """
    if isinstance(mean, DimensionalArray):
        mean = mean.array
    if isinstance(cov, DimensionalArray):
        cov = cov.array
    return DimensionalArray(np.random.multivariate_normal(mean, cov, size))

def poisson(lam: Union[float, DimensionalArray], size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Draw samples from a Poisson distribution.
    
    Parameters
    ----------
    lam : float or array_like
        Expected number of events occurring in a fixed-time interval
    size : int or tuple of ints, optional
        Output shape. If size is None and lam is a scalar, a single sample is returned.
        
    Returns
    -------
    DimensionalArray
        Drawn samples from the Poisson distribution.
    """
    if isinstance(lam, DimensionalArray):
        lam = lam.array
    return DimensionalArray(np.random.poisson(lam, size))

def exponential(scale: float = 1.0, size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Draw samples from an exponential distribution."""
    return DimensionalArray(np.random.exponential(scale, size))

def gamma(shape: float, scale: float = 1.0, size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Draw samples from a Gamma distribution."""
    return DimensionalArray(np.random.gamma(shape, scale, size))

def beta(a: float, b: float, size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Draw samples from a Beta distribution."""
    return DimensionalArray(np.random.beta(a, b, size))

def binomial(n: int, p: float, size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Draw samples from a binomial distribution."""
    return DimensionalArray(np.random.binomial(n, p, size))

def chisquare(df: float, size: Optional[Union[int, Tuple[int, ...]]] = None) -> DimensionalArray:
    """Draw samples from a chi-square distribution."""
    return DimensionalArray(np.random.chisquare(df, size))

def choice(a: Any, size: Optional[Union[int, Tuple[int, ...]]] = None, replace: bool = True, p: Optional[Union[list, np.ndarray, DimensionalArray]] = None) -> DimensionalArray:
    """Generate a random sample from a given 1-D array."""
    if isinstance(a, DimensionalArray):
        a = a.array
    if isinstance(p, DimensionalArray):
        p = p.array
    return DimensionalArray(np.random.choice(a, size, replace, p))

def permutation(x: Union[int, np.ndarray, DimensionalArray]) -> DimensionalArray:
    """Randomly permute a sequence, or return a permuted range."""
    if isinstance(x, DimensionalArray):
        x = x.array
    return DimensionalArray(np.random.permutation(x))

def shuffle(x: Union[np.ndarray, DimensionalArray]) -> None:
    """Modify a sequence in-place by shuffling its contents."""
    if isinstance(x, DimensionalArray):
        np.random.shuffle(x.array)
    else:
        np.random.shuffle(x)

# Add seed function for reproducibility
def seed(seed: Optional[int] = None) -> None:
    """Seed the random number generator."""
    np.random.seed(seed)

def get_state() -> Any:
    """Return the current state of the random number generator."""
    return np.random.get_state()

def set_state(state: Any) -> None:
    """Set the state of the random number generator."""
    np.random.set_state(state) 