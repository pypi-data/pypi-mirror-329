from typing import Iterable

# Define conversion factors to Hartree
# 1 unit = factor * Hartree
CONVERSION_TO_HARTREE = {
    "hartree": 1.0,
    "ev": 1.0 / 27.211386245988,  # 1 eV ≈ 0.0367493 Hartree
    "1/cm": 1.0 / 219474.6313705,  # 1 cm^-1 ≈ 4.5563353e-6 Hartree
    "kcal/mol": 1.0 / 627.509474,  # 1 kcal/mol ≈ 0.0015936 Hartree
    "kj/mol": 1.0 / 2625.499638,  # 1 kJ/mol ≈ 0.0003809 Hartree
}


# List of supported units for easy reference
SUPPORTED_UNITS = list(CONVERSION_TO_HARTREE.keys())


def convert_energy(value, from_unit, to_unit):
    """
    Convert energy from one unit to another.

    Parameters:
        value (float): The numerical value of the energy to convert.
        from_unit (str): The unit of the input energy. Supported units:
                         'hartree', 'eV', 'cm-1', 'kcal/mol'
        to_unit (str): The unit to convert the energy into. Supported units:
                       'hartree', 'eV', 'cm-1', 'kcal/mol'

    Returns:
        float: The converted energy value in the desired unit.

    Raises:
        ValueError: If either from_unit or to_unit is not supported.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit not in CONVERSION_TO_HARTREE:
        raise ValueError(
            f"Unsupported 'from_unit': {from_unit}. Supported units: {SUPPORTED_UNITS}"
        )

    if to_unit not in CONVERSION_TO_HARTREE:
        raise ValueError(
            f"Unsupported 'to_unit': {to_unit}. Supported units: {SUPPORTED_UNITS}"
        )

    # Convert the input value to Hartree
    value_in_hartree = value * CONVERSION_TO_HARTREE[from_unit]

    # Convert from Hartree to the desired unit
    converted_value = value_in_hartree / CONVERSION_TO_HARTREE[to_unit]

    return converted_value


class Energies:
    def __init__(self, lines: Iterable[str]) -> None:
        self.lines = list(lines)

    def fspe(self, unit: str = "hartree") -> float | None:
        """Get final single point energy in specified units"""
        for line in reversed(self.lines):
            if "FINAL SINGLE POINT ENERGY" in line:
                value = float(line.split()[-1])
                return convert_energy(value, from_unit="hartree", to_unit=unit)

    def gibbs_free_energy(self, unit: str = "hartree") -> float | None:
        """Get Gibbs free energy in specified units"""
        for line in reversed(self.lines):
            if "Final Gibbs free energy" in line:
                value = float(line.split()[-2])
                return convert_energy(value, from_unit="hartree", to_unit=unit)

    def gibbs_minus_electronic_energy(self, unit: str = "hartree") -> float | None:
        """Get Gibbs minus electronic energy in specified units"""
        for line in reversed(self.lines):
            if "G-E(el)" in line:
                value = float(line.split()[-4])
                return convert_energy(value, from_unit="hartree", to_unit=unit)

    def entropy(self, unit: str = "hartree") -> float | None:
        """Get entropy in specified units"""
        for line in reversed(self.lines):
            if "Final entropy term" in line:
                value = float(line.split()[-4])
                return convert_energy(value, from_unit="hartree", to_unit=unit)

    def enthalpy(self, unit: str = "hartree") -> float | None:
        """Get enthalpy in specified units"""
        for line in reversed(self.lines):
            if "Total Enthalpy" in line:
                value = float(line.split()[-2])
                return convert_energy(value, from_unit="hartree", to_unit=unit)

    def zero_point_energy(self, unit: str = "hartree") -> float | None:
        """Get zero point energy in specified units"""
        for line in reversed(self.lines):
            if "Zero point energy" in line:
                value = float(line.split()[-4])
                return convert_energy(value, from_unit="hartree", to_unit=unit)
