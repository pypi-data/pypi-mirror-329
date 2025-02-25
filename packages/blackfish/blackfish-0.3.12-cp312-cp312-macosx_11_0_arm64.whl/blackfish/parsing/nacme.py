from typing import Iterable

import polars as pl

from blackfish.parsing.utilities import find_table_starts


def nacme(lines: Iterable[str]) -> pl.DataFrame:
    """
    Extract non-adiabatic coupling matrix elements from ORCA output file contents.

    Args:
        lines (Iterable[str]): ORCA output file contents.

    Returns:
        pl.DataFrame: A DataFrame containing the NAC vectors between electronic states
            with columns 'id', 'symbol', 'x', 'y', 'z', and 'magnitude'.
            id - atom index
            symbol - atomic symbol
            x,y,z - NAC vector components
            magnitude - sum of absolute values of vector components
    """
    TABLE_HEADER = "CARTESIAN NON-ADIABATIC COUPLINGS"
    TABLE_HEADER_OFFSET = 5

    table_start_idx = next(find_table_starts(lines, TABLE_HEADER, TABLE_HEADER_OFFSET))

    # Collect table
    rows = []
    for row in list(lines)[table_start_idx:]:
        # Stop on empty line
        if not row.strip():
            break

        rows.append(row.split())

    df = pl.DataFrame(
        rows,
        schema={"id": int, "symbol": str, "_": str, "x": float, "y": float, "z": float},
        orient="row",
    ).drop("_")

    # Compute magnitude
    df = df.with_columns(
        (pl.col("x").abs() + pl.col("y").abs() + pl.col("z").abs()).alias("magnitude")
    )

    return df
