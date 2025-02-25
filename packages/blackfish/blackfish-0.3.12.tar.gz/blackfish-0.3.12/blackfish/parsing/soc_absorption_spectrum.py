from typing import Iterable

import polars as pl

from blackfish.parsing.utilities import ParsingError, find_table_starts


def soc_absorption_spectrum(lines: Iterable[str]) -> pl.DataFrame:
    """Parse SOC absorption spectrum from ORCA output file contents.

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
    # Determine major ORCA version
    for line in lines:
        if "Program Version" in line:
            orca_version = int(line.split()[2][0])
            break
    else:
        raise ParsingError("ORCA version not found in output file")

    TABLE_HEADER = (
        "SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS"
    )
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

    match orca_version:
        case 5:
            return orca5_soc_absorption_spectrum_parser(rows)
        case 6:
            return orca6_soc_absorption_spectrum_parser(rows)
        case _:
            raise ParsingError(f"Unsupported ORCA version {orca_version}")


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
        (pl.col("osc_strength") / pl.col("osc_strength").max()).alias("rel_intensity")
    )

    return df


def orca5_soc_absorption_spectrum_parser(rows: list[str]) -> pl.DataFrame:
    # ORCA 5 doesn't print the final state multiplicity..
    # Process table
    processed_rows = []
    for row in rows:
        row = row.replace("(", "").replace(")", "").replace(",", "")
        processed_row = row.split()[1:6]
        processed_rows.append(processed_row)

    df = pl.DataFrame(
        processed_rows,
        orient="row",
        schema={
            "state": pl.Int64,
            "energy_cm": pl.Float64,
            "wavelength_nm": pl.Float64,
            "osc_strength": pl.Float64,
            "d2": pl.Float64,
        },
    )

    df = df.with_columns(
        (pl.col("osc_strength") / pl.col("osc_strength").max()).alias("rel_intensity")
    )

    return df
