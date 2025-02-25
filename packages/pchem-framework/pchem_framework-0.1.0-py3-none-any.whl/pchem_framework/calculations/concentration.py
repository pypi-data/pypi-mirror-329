import numpy as np

def molarity_to_molality(molarity: float, density: float, molar_mass: float) -> float:
    """
    Convert molarity (M) to molality (m).

    Parameters:
        molarity (float): Molar concentration (mol/L).
        density (float): Solution density (g/mL).
        molar_mass (float): Solute molar mass (g/mol).

    Returns:
        float: Molality in mol/kg.

    Example:
        >>> molarity_to_molality(2.0, 1.083, 58.44)
        2.4
    """
    denominator = (density * 1000) - (molarity * molar_mass)
    return round((molarity * 1000) / denominator, 1)

def ppm_to_molarity(ppm: float, molar_mass: float, density: float) -> float:
    """
    Convert ppm concentration to molarity.
    
    Formula: M = (ppm * density) / (molar_mass * 1000)
    """
    return (ppm * density) / (molar_mass * 1000)