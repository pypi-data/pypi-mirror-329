# pchem_framework/data_handling/unit_conversion.py
from pint import UnitRegistry
from typing import Union

class UnitConverter:
    """
    Robust unit conversion system using Pint library.
    Maintains stateful unit registry for complex conversions.
    """
    _registry = UnitRegistry()
    _temperature_units = {'kelvin', 'celsius', 'fahrenheit'}

    @classmethod
    def convert_temperature(cls, value: float, from_unit: str, to_unit: str) -> float:
        """
        Fixed temperature conversion with Pint's built-in support
        """
        from_unit = from_unit.replace('°', 'deg')  # Pint syntax
        to_unit = to_unit.replace('°', 'deg')
        
        quantity = cls._registry.Quantity(value, from_unit)
        return quantity.to(to_unit).magnitude

    @classmethod
    def convert_pressure(cls, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert pressure between common chemistry units.

        Supported units: Pa, hPa, kPa, MPa, atm, mmHg, bar

        Example:
            >>> convert_pressure(1, 'atm', 'mmHg')
            760.0
            >>> convert_pressure(101325, 'Pa', 'atm')
            1.0
        """
        quantity = cls._registry.Quantity(value, from_unit)
        return quantity.to(to_unit).magnitude