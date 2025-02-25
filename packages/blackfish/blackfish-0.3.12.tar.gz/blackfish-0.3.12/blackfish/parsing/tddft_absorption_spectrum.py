from typing import Iterable

import polars as pl

from blackfish.parsing.utilities import ParsingError, find_table_starts


def tddft_absorption_spectrum(lines: Iterable[str]) -> pl.DataFrame:
    """Parse TDDFT absorption spectrum from ORCA output file contents.

    Args:
        lines (Iterable[str]): ORCA output file contents.

    Returns:
        pl.DataFrame: DataFrame containing parsed spectrum with columns:
            - state (int64): Final state number
            - mult (float64): Final state multiplicity
            - energy_ev (float64): Transition energy in eV
            - energy_cm (float64): Transition energy in cm^-1
            - wavelength_nm (float64): Transition wavelength in nm
            - osc_strength (float64): Oscillator strength
            - d2 (float64): Total transition dipole moment squared
            - dx (float64): x component of transition dipole moment
            - dy (float64): y component of transition dipole moment
            - dz (float64): z component of transition dipole moment
            - rel_intensity (float64): Relative intensity normalized to strongest peak
    """
    TABLE_HEADER = "ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS"
    TABLE_HEADER_OFFSET = 5

    table_start_idx = next(find_table_starts(lines, TABLE_HEADER, TABLE_HEADER_OFFSET))

    # Collect table
    rows = []
    for row in list(lines)[table_start_idx:]:
        # Stop on empty line
        if not row.strip():
            break

        rows.append(row)

    if not rows:
        raise ParsingError("No data found in SOC absorption spectrum table")

    return orca6_soc_absorption_spectrum_parser(rows)


def orca6_soc_absorption_spectrum_parser(rows: list[str]) -> pl.DataFrame:
    # Process table
    processed_rows = []
    for row in rows:
        row = row.replace("A", "").replace("B", "").replace("->", "")
        to_state, to_spin = row.split()[1].split("-")
        processed_row = [to_state, to_spin] + row.split()[2:]
        processed_rows.append(processed_row)

    df = pl.DataFrame(
        processed_rows,
        orient="row",
        schema={
            "state": pl.Int64,
            "mult": pl.Float64,
            "energy_ev": pl.Float64,
            "energy_cm": pl.Float64,
            "wavelength_nm": pl.Float64,
            "osc_strength": pl.Float64,
            "d2": pl.Float64,
            "dx": pl.Float64,
            "dy": pl.Float64,
            "dz": pl.Float64,
        },
    )

    df = df.with_columns(
        (
            pl.when(pl.col("osc_strength").max() == 0)
            .then(pl.lit(0))
            .otherwise((pl.col("osc_strength") / pl.col("osc_strength").max()))
        ).alias("rel_intensity")
    )

    return df
