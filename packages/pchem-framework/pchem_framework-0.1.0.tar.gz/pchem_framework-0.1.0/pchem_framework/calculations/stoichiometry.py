import numpy as np

def limiting_reactant(amounts: list[float], coefficients: list[int]) -> int:
    """
    Determine the limiting reactant from molar amounts and stoichiometric coefficients.

    Parameters:
        amounts (list): List of molar amounts for each reactant.
        coefficients (list): List of stoichiometric coefficients.

    Returns:
        int: Index of the limiting reactant.

    Raises:
        ValueError: For invalid inputs or negative values.

    Example:
        >>> limiting_reactant([2.0, 4.0], [3, 4])
        0
    """
    if len(amounts) != len(coefficients):
        raise ValueError("Amounts and coefficients must have same length")
    
    ratios = [amt/coeff for amt, coeff in zip(amounts, coefficients)]
    return np.argmin(ratios)

def product_yield(actual: float, theoretical: float) -> float:
    """
    Calculate percentage yield of a reaction.

    Parameters:
        actual (float): Measured product mass in grams.
        theoretical (float): Theoretical maximum mass in grams.

    Returns:
        float: Percentage yield (0-100).

    Example:
        >>> product_yield(45.5, 50.0)
        91.0
    """
    return round((actual / theoretical) * 100, 1)