from dataclasses import dataclass
from typing import Iterable

import polars as pl

from blackfish.parsing.utilities import ParsingError, find_table_starts


def casscf_roots(lines: Iterable[str]) -> pl.DataFrame:
    """Parse CASSCF roots from ORCA output file contents.

    Args:
        lines (Iterable[str]): ORCA output file contents.

    Returns:
        pl.DataFrame: DataFrame containing parsed states with columns:
            - root (int64): Root
            - energy_eh (float64): Root energy in Hartree
            - weight (float64): Weight of the CSF to the root
            - csf (int64): Configuration State Function ID
            - configuration (str): The CSF electron configuration of the active space
    """
    TABLE_HEADER = "CAS-SCF STATES FOR BLOCK"
    TABLE_HEADER_OFFSET = 0  # used to be 3

    roots_list = []
    for table_start_idx in find_table_starts(lines, TABLE_HEADER, TABLE_HEADER_OFFSET):
        mult = lines[table_start_idx].split()[-2]
        # Collect table
        rows = []
        for row in list(lines)[table_start_idx + 3 :]:
            # Stop on empty line
            if not row.strip():
                break

            rows.append(row)

        if not rows:
            raise ParsingError("No data found in SOC absorption spectrum table")

        these_roots = casscf_root_parser(rows).with_columns(
            pl.lit(int(mult)).alias("mult")
        )
        roots_list.append(these_roots)

    # Combine all DataFrames at once
    roots = pl.concat(roots_list, how="vertical")
    return roots


@dataclass
class RootContrib:
    contrib: float
    csf: int
    config: str


@dataclass
class Root:
    id: int
    energy_eh: float
    contribs: list[RootContrib]


def casscf_root_parser(lines: list[str]) -> pl.DataFrame:
    # Process table

    def iter_roots(lines):
        current_state = []

        for line in lines:
            line = line.strip()
            if not line:
                break

            if line.startswith("ROOT"):
                if current_state:
                    yield current_state
                current_state = [line]
            elif current_state:
                current_state.append(line)

        if current_state:  # Don't forget the last state
            yield current_state

    roots = []
    for _root in iter_roots(lines):
        root = Root(id=0, energy_eh=0, contribs=[])
        for line in _root:
            line = line.replace(":", "").replace("[", "").replace("]", "")
            if not line.strip():
                roots.append(root)
                break
            if line.startswith("ROOT"):
                roots.append(root)
                _, id, _, energy_eh, *_ = line.split()
                root.id = int(id)
                root.energy_eh = float(energy_eh)
                continue
            contrib, csf, config = line.split()
            root.contribs.append(RootContrib(float(contrib), int(csf), config))

    def to_df(roots):
        roots = [
            {
                "root": r.id,
                "energy_eh": r.energy_eh,
                "weight": c.contrib,
                "csf": c.csf,
                "configuration": c.config,
            }
            for r in roots
            for c in r.contribs
        ]
        df = pl.DataFrame(roots, strict=False, orient="row")
        return df

    return to_df(roots)
