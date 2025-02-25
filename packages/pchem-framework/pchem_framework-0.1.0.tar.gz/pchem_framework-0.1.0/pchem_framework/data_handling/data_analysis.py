# pchem_framework/data_handling/data_analysis.py
import pandas as pd
import numpy as np
from typing import Union, Tuple

def calculate_average(data: Union[pd.Series, list], precision: int = 3) -> float:
    """
    Calculate statistical average of chemical measurement data.

    Parameters:
        data (Series/list): Numerical chemical data
        precision (int): Decimal precision for result

    Returns:
        float: Arithmetic mean

    Example:
        >>> calculate_average([0.12, 0.15, 0.13])
        0.133
    """
    if not data:
        raise ValueError("Input data cannot be empty")
    
    series = pd.Series(data) if isinstance(data, list) else data
    return round(series.mean(), precision)

def perform_linear_regression(x_data: Union[list, pd.Series], 
                             y_data: Union[list, pd.Series]) -> Tuple[float, float, float]:
    """
    Perform linear regression on chemical calibration data.

    Returns:
        Tuple: (slope, intercept, r_squared)

    Example:
        >>> x = [1, 2, 3]
        >>> y = [2, 4, 6]
        >>> perform_linear_regression(x, y)
        (2.0, 0.0, 1.0)
    """
    x = pd.Series(x_data)
    y = pd.Series(y_data)
    
    if len(x) != len(y):
        raise ValueError("x and y data must have same length")
    
    slope, intercept = np.polyfit(x, y, 1)
    correlation = np.corrcoef(x, y)[0, 1]
    r_squared = correlation ** 2
    
    return round(slope, 4), round(intercept, 4), round(r_squared, 4)