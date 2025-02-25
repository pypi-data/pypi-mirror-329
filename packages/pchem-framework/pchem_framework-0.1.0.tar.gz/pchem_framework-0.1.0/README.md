# Practical Chemistry Framework (pchem-framework) 🔬🧪

[![PyPI Version](https://img.shields.io/pypi/v/pchem-framework)](https://pypi.org/project/pchem-framework/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pchem-framework)](https://pypi.org/project/pchem-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/pchem-framework/badge/?version=latest)](https://pchem-framework.readthedocs.io/)

An open-source Python framework for practical chemistry calculations, data analysis, and visualization. Designed for students, educators, and researchers.

![Titration Curve Example](https://via.placeholder.com/800x400.png?text=Titration+Curve+Example)

## Table of Contents
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Functionality](#core-functionality)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Key Features 🚀

### Chemical Calculations
- **Stoichiometry**: Limiting reactant analysis, yield calculations
- **Solution Chemistry**: Molarity <-> molality conversions, dilution calculations
- **Acid-Base Chemistry**: pH calculations for strong/weak acids/bases, buffers
- **Thermodynamics**: Enthalpy, entropy, and Gibbs free energy calculations

### Data Handling & Visualization
- **File I/O**: CSV, JSON, and text file support with pandas integration
- **Unit Conversion**: Robust dimensional analysis with Pint library
- **Data Analysis**: Statistical functions and linear regression
- **Plotting**: Publication-ready graphs for kinetics and titration curves

## Installation ⚙️

```bash
# Stable version
pip install pchem-framework

# Development version
pip install git+https://github.com/somkietacode/pchem-framework.git
```

**Requirements:** Python 3.8+ with NumPy, Pandas, Matplotlib, and Pint

## Quick Start 🏁

### Basic Calculations
```python
from pchem_framework.calculations import molar_mass, ph

# Calculate molar mass of H2SO4
atomic_weights = {'H': 1.008, 'S': 32.07, 'O': 16.00}
print(molar_mass.calculate_molar_mass('H2SO4', atomic_weights))  # Output: 98.086 g/mol

# Calculate buffer pH (Henderson-Hasselbalch)
print(ph.buffer_ph(0.1, 0.2, 4.76))  # Output: 5.06
```

### Data Analysis Workflow
```python
from pchem_framework.data_handling import file_io, plotting

# Load experimental data
kinetic_data = file_io.read_csv("kinetic_data.csv")

# Generate concentration-time plot
fig = plotting.plot_concentration_vs_time(
    kinetic_data['time'], 
    kinetic_data['concentration'],
    title="First-Order Reaction Kinetics"
)
fig.savefig("kinetics_plot.png")
```

## Core Functionality 📚

### Calculations Module
```python
from pchem_framework.calculations import (
    molar_mass,       # Formula parsing and MW calculations
    stoichiometry,    # Reaction balancing and yield predictions
    concentration,    # Solution preparation calculations
    ph,               # Acid-base equilibrium calculations
    kinetics,         # Reaction rate analysis
    thermodynamics    # Energy calculations
)
```

### Data Handling Module
```python
from pchem_framework.data_handling import (
    file_io,          # Unified data import/export
    unit_conversion,  # Dimensional analysis
    data_analysis,    # Statistical methods
    plotting          # Scientific visualization
)
```

## Documentation 📖

Explore detailed guides and tutorials in our documentation:

- [Full API Reference](https://pchem-framework.readthedocs.io/)
- [Example Notebooks](notebooks/)
  - Basic Stoichiometry Calculations
  - Advanced Buffer Solutions Analysis
  - Kinetic Data Processing Tutorial

## Contributing 🤝

We welcome contributions! Please see our:
- [Contribution Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Roadmap](ROADMAP.md)

To report bugs or request features:
- [Open an Issue](https://github.com/your-username/pchem-framework/issues)

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support ☕

If you find this project useful, please consider:
- [Starring the Repository](https://github.com/your-username/pchem-framework)
- Citing us in your publications:
  ```bibtex
  @software{pchem_framework,
    title={Practical Chemistry Framework},
    author={Your Name},
    year={2024},
    publisher={GitHub},
    journal={GitHub repository},
    howpublished={\url{https://github.com/your-username/pchem-framework}}
  }
  ```
