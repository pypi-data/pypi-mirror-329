import re

def calculate_molar_mass(formula: str, atomic_weights: dict[str, float]) -> float:
    """
    Calculate the molar mass of a chemical compound from its formula.

    Parameters:
        formula (str): Chemical formula (e.g., 'H2O', 'C6H12O6').
        atomic_weights (dict): Dictionary mapping element symbols to their atomic weights (g/mol).

    Returns:
        float: Molar mass in grams per mole (g/mol).

    Raises:
        ValueError: If formula contains invalid characters or undefined elements.

    Example:
        >>> atomic_data = {'H': 1.008, 'O': 16.00, 'C': 12.01}
        >>> calculate_molar_mass('H2O', atomic_data)
        18.016
        >>> calculate_molar_mass('C6H12O6', atomic_data)
        180.156
    """
    pattern = re.compile(r"([A-Z][a-z]*)(\d*)")
    total = 0.0
    
    for element, count_str in pattern.findall(formula):
        if element not in atomic_weights:
            raise ValueError(f"Atomic weight for {element} not provided")
        count = int(count_str) if count_str else 1
        total += atomic_weights[element] * count
        
    return round(total, 3)