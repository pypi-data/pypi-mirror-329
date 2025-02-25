import numpy as np

def strong_acid_ph(concentration: float) -> float:
    """
    Calculate pH of a strong acid solution.

    Parameters:
        concentration (float): Acid concentration in mol/L.

    Returns:
        float: pH value.

    Example:
        >>> strong_acid_ph(0.01)
        2.0
    """
    return round(-np.log10(concentration), 1)

def buffer_ph(acid_conc: float, base_conc: float, pka: float) -> float:
    """
    Calculate buffer pH using Henderson-Hasselbalch equation.

    Parameters:
        acid_conc (float): Concentration of weak acid.
        base_conc (float): Concentration of conjugate base.
        pka (float): Acid dissociation constant.

    Returns:
        float: pH value.

    Example:
        >>> buffer_ph(0.1, 0.2, 4.76)
        5.06
    """
    return round(pka + np.log10(base_conc/acid_conc), 2)