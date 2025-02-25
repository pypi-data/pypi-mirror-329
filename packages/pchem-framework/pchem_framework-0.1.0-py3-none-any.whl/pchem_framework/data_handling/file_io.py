# pchem_framework/data_handling/file_io.py
import os
import pandas as pd
from typing import Union, Dict, Any
from pathlib import Path

def read_csv(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
    """
    Read chemical data from CSV files with robust validation and auto-detection.

    Parameters:
        file_path (str/Path): Path to CSV file
        **kwargs: Additional pandas.read_csv parameters

    Returns:
        pd.DataFrame: DataFrame containing chemical data

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: For invalid chemical data formats

    Example:
        >>> data = read_csv("spectra.csv")
        >>> print(data.head())
        
        Example valid CSV structure:
        wavelength,nm,absorbance
        400,0.12
        410,0.15
        ...
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    if Path(file_path).suffix.lower() != '.csv':
        raise ValueError("File extension must be .csv")

    try:
        df = pd.read_csv(file_path, **kwargs)
        if df.empty:
            raise ValueError("CSV file contains no data")
        return df
    except pd.errors.ParserError as e:
        raise ValueError(f"CSV parsing error: {str(e)}") from e

def write_json(data: Dict[str, Any], file_path: Union[str, Path], indent: int = 4):
    """
    Write chemical data to JSON file with proper formatting.

    Parameters:
        data (dict): Data to serialize (must be JSON-serializable)
        file_path (str/Path): Output file path
        indent (int): JSON indentation level

    Example:
        >>> data = {"compound": "NaOH", "concentration": 0.1, "units": "M"}
        >>> write_json(data, "solution.json")
    """
    import json
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=indent)