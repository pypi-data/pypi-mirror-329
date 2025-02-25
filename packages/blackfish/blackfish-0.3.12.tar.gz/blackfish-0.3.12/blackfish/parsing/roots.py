from typing import Iterable, Iterator

import polars as pl

from blackfish.parsing.utilities import ParsingError


def roots(lines: Iterable[str]) -> pl.DataFrame:
    """Parse excited state roots data from ORCA quantum chemistry output file contents.

    Args:
        lines (Iterable[str]): ORCA output file contents.

    Returns:
        pl.DataFrame: A Polars DataFrame containing parsed roots data with columns:
            - root: Root number
            - mult: Multiplicity
            - donor: Donor orbital
            - acceptor: Acceptor orbital
            - weight: Contribution weight
            - energy_cm: Energy in cm⁻¹

    Raises:
        ParsingError: If the specified file does not exist, is not a file, or no roots are found in it.

    The function looks for TD-DFT/TDA or TD-DFT excited states sections in the output file,
    extracts roots data including state numbers, energies, and orbital transitions, and
    returns them in a tabular format.
    """

    lines = list(lines)

    # Find the start of root section(s) with different header offsets
    start_indices = []
    for i, line in enumerate(lines):
        if "TD-DFT/TDA EXCITED STATES" in line or "TD-DFT EXCITED STATES" in line:
            while not lines[i].startswith("STATE"):
                i += 1
            start_indices.append(i)

    # Parse roots
    roots = []
    for start_idx in start_indices:
        for root_lines in _iter_roots(lines[start_idx:]):
            root_data = _parse_single_root(root_lines)
            roots.append(root_data)

    # Flatten the data structure
    flattened_roots = []
    for root in roots:
        for orb_contrib in root["orbital_transitions"]:
            flattened_roots.append(
                {
                    "root": root["root"],
                    "mult": root["mult"],
                    "donor": orb_contrib["donor"],
                    "acceptor": orb_contrib["acceptor"],
                    "weight": orb_contrib["weight"],
                    "energy_cm": root["energy_cm"],
                }
            )

    # Create and transform DataFrame
    df = pl.DataFrame(flattened_roots)

    if len(df) == 0:
        raise ParsingError("No roots found")

    return df.sort(by=["root", "weight"], descending=[False, True])


def _parse_single_root(root_lines: list[str]) -> dict:
    """Parse a single excited state root block into component data.

    Args:
        root_lines (list[str]): List of lines containing a single root block from ORCA output.
            First line should contain state header, subsequent lines have orbital transitions.

    Returns:
        dict: Parsed root data with keys:
            - root (int): State number
            - energy_ev (float): Energy in electron volts
            - energy_cm (float): Energy in wavenumbers (cm⁻¹)
            - spin_projection (float): Spin projection value
            - mult (int): Multiplicity
            - orbital_transitions (list): List of dicts containing:
                - donor (str): Donor orbital
                - acceptor (str): Acceptor orbital
                - weight (float): Transition weight
    """
    # Parse header line
    header = root_lines[0].strip()
    state_num = int(header[5 : header.index(":")])
    parts = header.strip().split()
    energy_ev = float(parts[5])
    energy_cm = float(parts[7])
    spin_projection = float(parts[11])
    mult = int(parts[13])

    # Parse root contributions
    orbital_transitions = []
    for line in root_lines[1:]:
        parts = line.replace("->", "").replace(":", "").replace(")", "").strip().split()
        orbital_transitions.append(
            {
                "donor": str(parts[0]),
                "acceptor": str(parts[1]),
                "weight": float(parts[2]),
            }
        )

    return {
        "root": state_num,
        "energy_ev": energy_ev,
        "energy_cm": energy_cm,
        "spin_projection": spin_projection,
        "mult": mult,
        "orbital_transitions": orbital_transitions,
    }


def _iter_roots(lines: list[str]) -> Iterator[list[str]]:
    """Iterate over excited state root blocks in ORCA output text lines.

    Args:
        lines (list[str]): List of text lines from ORCA output file starting
            with a STATE header line.

    Yields:
        list[str]: List of lines comprising a single excited state root block,
            including the header line and orbital transition lines.

    Each root block starts with "STATE" and contains one or more orbital transition
    lines. Blocks are delimited by empty lines and subsequent STATE headers.
    """
    current_state = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("STATE"):
                continue
            else:
                break

        if line.startswith("STATE"):
            if current_state:
                yield current_state
            current_state = [line]
        elif current_state:
            current_state.append(line)

    if current_state:  # Don't forget the last state
        yield current_state
