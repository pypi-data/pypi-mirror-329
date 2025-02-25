import numpy as np

def half_life(k: float) -> float:
    """
    Calculate half-life for first-order reactions.

    Parameters:
        k (float): Rate constant (1/s).

    Returns:
        float: Half-life in seconds.

    Example:
        >>> half_life(0.005)
        138.6
    """
    return round(np.log(2) / k, 1)