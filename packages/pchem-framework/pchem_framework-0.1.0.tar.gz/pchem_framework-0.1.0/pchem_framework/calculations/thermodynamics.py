def gibbs_free_energy(delta_h: float, delta_s: float, temp: float) -> float:
    """
    Calculate Gibbs free energy change (ΔG).

    Parameters:
        delta_h (float): Enthalpy change (J/mol).
        delta_s (float): Entropy change (J/(mol·K)).
        temp (float): Temperature (K).

    Returns:
        float: ΔG in J/mol.

    Example:
        >>> gibbs_free_energy(-80000, -200, 298)
        -20400.0
    """
    return delta_h - temp * delta_s