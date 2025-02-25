# pchem_framework/data_handling/plotting.py
import matplotlib.pyplot as plt
from typing import List, Union
import numpy as np

def plot_concentration_vs_time(time_data: Union[List[float], np.ndarray],
                              conc_data: Union[List[float], np.ndarray],
                              title: str = "Concentration vs Time",
                              **kwargs) -> plt.Figure:
    """
    Generate professional concentration-time plots for kinetic studies.

    Parameters:
        time_data: Time values (x-axis)
        conc_data: Concentration values (y-axis)
        title: Plot title
        **kwargs: Matplotlib style parameters

    Returns:
        plt.Figure: Configured figure object

    Example:
        >>> fig = plot_concentration_vs_time([0, 1, 2], [1.0, 0.5, 0.25])
        >>> fig.savefig("kinetics.png")
    """
    fig, ax = plt.subplots(figsize=kwargs.get('figsize', (8, 6)))
    
    ax.plot(time_data, conc_data, 
           marker=kwargs.get('marker', 'o'),
           linestyle=kwargs.get('linestyle', '-'),
           color=kwargs.get('color', '#1f77b4'))
    
    ax.set(xlabel='Time (s)', ylabel='Concentration (M)',
          title=title)
    ax.grid(True, alpha=0.3)
    
    return fig

def plot_titration_curve(volume_added: Union[List[float], np.ndarray],
                        pH: Union[List[float], np.ndarray],
                        equivalence_point: float = None) -> plt.Figure:
    """
    Generate publication-quality titration curve plots.

    Parameters:
        volume_added: Titrant volume (x-axis)
        pH: Solution pH (y-axis)
        equivalence_point: Optional equivalence point marker

    Example:
        >>> vol = [0, 10, 20, 30]
        >>> pH = [1, 2, 7, 12]
        >>> fig = plot_titration_curve(vol, pH, equivalence_point=20)
    """
    if len(volume_added) != len(pH):
        raise ValueError("Volume and pH arrays must have equal length")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(volume_added, pH, 'b-', marker='o', markersize=8)
    
    if equivalence_point:
        ax.axvline(equivalence_point, color='r', linestyle='--', 
                  label='Equivalence Point')
    
    ax.set(xlabel='Volume Added (mL)', ylabel='pH',
          title='Titration Curve')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig