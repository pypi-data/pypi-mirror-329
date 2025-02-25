from typing import Iterable

import polars as pl

from blackfish.parsing.utilities import find_table_starts


def socme(lines: Iterable[str]) -> pl.DataFrame:
    """
    Extract spin-orbit coupling matrix elements from ORCA output file contents.

    Args:
        lines (Iterable[str]): ORCA output file contents.

    Returns:
        pl.DataFrame: A DataFrame containing the SOC vectors between electronic states
            with columns 'triplet_root', 'singlet_root, 'x', 'y', 'z', and 'magnitude'.
            triplet_root - triplet root
            singlet_root - singlet root
            x,y,z - SOC vector components
            magnitude - sum of absolute values of vector components
    """
    TABLE_HEADER = "CALCULATED SOCME BETWEEN TRIPLETS AND SINGLETS"
    TABLE_HEADER_OFFSET = 5

    table_start_idx = next(find_table_starts(lines, TABLE_HEADER, TABLE_HEADER_OFFSET))

    # Collect table
    rows = []
    for row in list(lines)[table_start_idx:]:
        # Stop on empty line
        if not row.strip():
            break

        rows.append(row.replace("(", "").replace(")", "").replace(",", "").split())

    df = pl.DataFrame(
        rows,
        schema={
            "triplet_root": int,
            "singlet_root": int,
            "real_z": float,
            "imag_z": float,
            "real_x": float,
            "imag_x": float,
            "real_y": float,
            "imag_y": float,
        },
        orient="row",
    )

    # Compute individual magnitudes
    df = df.with_columns(
        ((pl.col("real_z").pow(2) + pl.col("imag_z").pow(2)).sqrt()).alias(
            "z_magnitude"
        ),
        ((pl.col("real_x").pow(2) + pl.col("imag_x").pow(2)).sqrt()).alias(
            "x_magnitude"
        ),
        ((pl.col("real_y").pow(2) + pl.col("imag_y").pow(2)).sqrt()).alias(
            "y_magnitude"
        ),
    )

    # Compute total magnitude
    df = df.with_columns(
        (pl.col("z_magnitude") + pl.col("x_magnitude") + pl.col("y_magnitude")).alias(
            "magnitude"
        )
    )

    # Return a cleaner DataFrame
    clean_df = df.select(
        [
            "triplet_root",
            "singlet_root",
            "magnitude",
        ]
    ).sort(by="magnitude", descending=True)

    return clean_df
