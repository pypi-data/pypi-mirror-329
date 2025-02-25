from pathlib import Path
from typing import Iterable

import polars as pl

from blackfish.parsing import (
    Energies,
    ParsingError,
    casscf_roots,
    ir_spectrum,
    nacme,
    roots,
    soc_absorption_spectrum,
    soc_states,
    socme,
    tddft_absorption_spectrum,
)
from blackfish.parsing.energies import convert_energy


class OrcaParser:
    def __init__(self, lines: Iterable[str]):
        self.lines = list(lines)
        self.validate()

    @classmethod
    def from_file(cls, file: str) -> "OrcaParser":
        return cls(Path(file).read_text().splitlines())

    @staticmethod
    def convert_energy(value: float, from_unit: str, to_unit: str) -> float:
        return convert_energy(value, from_unit, to_unit)

    def validate(self) -> None:
        """Perform some health checks"""

        def check(keyword: str) -> bool:
            """Check file for keyword"""
            lines = reversed(self.lines)
            for line in lines:
                if keyword in line:
                    return True
            return False

        if check("TOTAL RUN TIME") is False:
            raise ParsingError("Calculation did not finish successfully")

        if check("Geometry convergence"):
            # It's some sort of geometry optimization
            if check("HURRAY") is False:
                raise ParsingError("Geometry optimization did not converge")

    def get_ir_spectrum(self) -> pl.DataFrame:
        return ir_spectrum(self.lines)

    def get_nacme(self) -> pl.DataFrame:
        "Non-adiabatic coupling matrix elements"
        return nacme(self.lines)

    def get_tddft_roots(self) -> pl.DataFrame:
        return roots(self.lines)

    def get_tddft_soc_spectrum(self) -> pl.DataFrame:
        return soc_absorption_spectrum(self.lines)

    def get_tddft_spectrum(self) -> pl.DataFrame:
        return tddft_absorption_spectrum(self.lines)

    def get_soc_states(self) -> pl.DataFrame:
        return soc_states(self.lines)

    def get_energies(self) -> Energies:
        return Energies(self.lines)

    def get_socme(self) -> pl.DataFrame:
        """Spin-orbit coupling matrix elements"""
        return socme(self.lines)

    def get_casscf_roots(self) -> pl.DataFrame:
        """CASSCF roots"""
        return casscf_roots(self.lines)
