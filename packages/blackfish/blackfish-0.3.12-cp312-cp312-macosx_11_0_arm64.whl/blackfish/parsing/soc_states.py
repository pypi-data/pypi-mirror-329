from typing import Iterable, Iterator

import polars as pl

from blackfish.parsing.utilities import ParsingError


def soc_states(lines: Iterable[str]) -> pl.DataFrame:
    """Parse spin-orbit coupling (SOC) states from ORCA output file contents.

    Extracts SOC state information including state energies and contributions from
    different spin components.

    Args:
        lines (Iterable[str]): ORCA output file contents.

    Returns:
        pl.DataFrame: DataFrame with columns:
            - state (int): SOC state number
            - spin (int): Spin component
            - root (int): Contributing root state
            - weight (float): State contribution weight
            - energy_cm (float): Energy in wavenumbers (cm⁻¹)

    Raises:
        ParsingError: If SOC matrix section is not found in input file.
    """
    # Find the start of SOC states section
    try:
        start_idx = (
            next(
                i
                for i, line in enumerate(lines)
                if "Eigenvectors of the SOC matrix:" in line.strip()
            )
            + 3
        )
    except StopIteration:
        raise ParsingError("SOC matrix section not found in input")

    # Parse states
    soc_states = []
    for state_lines in _iter_soc_states(list(lines)[start_idx:]):
        state_data = _parse_single_state(state_lines)

        # Flatten the data structure
        for root in state_data["roots"]:
            soc_states.append(
                {
                    "state": state_data["state"],
                    "energy_cm": state_data["energy_cm"],
                    **root,
                }
            )

    # Create and transform DataFrame
    df = pl.DataFrame(soc_states)
    return (
        df.group_by(["state", "spin"])
        .agg([pl.first("root"), pl.sum("weight"), pl.first("energy_cm")])
        .sort(["state", "weight"], descending=[False, True])
    )


def _parse_single_state(state_lines: list[str]) -> dict:
    """Parse a single spin-orbit coupling (SOC) state block into a dictionary.

    Takes a block of text lines representing a single SOC state and parses the state number,
    energy, and contributing root states with their weights and spin components.

    Args:
        state_lines (list[str]): Lines of text containing a single SOC state block,
            starting with "STATE n: energy" followed by root contribution lines.

    Returns:
        dict: Dictionary containing:
            - state (int): SOC state number
            - energy_cm (float): State energy in wavenumbers
            - roots (list[dict]): List of contributing roots, each containing:
                - weight (float): Contribution weight
                - real (float): Real component
                - imag (float): Imaginary component
                - root (int): Root state number
                - spin (int): Spin state
                - ms (int): Ms quantum number

    Example format:
        STATE 1: 0.000000
           1.000000    1.000000    0.000000     1    1    1
           0.000000    0.000000    0.000000     2    1    0
    """
    # Parse header line
    header = state_lines[0].strip()
    state_num = int(header[5 : header.index(":")])
    energy = float(header[header.index(":") + 1 :])

    # Parse root contributions
    roots = []
    for line in state_lines[1:]:
        parts = line.replace(":", "").strip().split()
        roots.append(
            {
                "weight": float(parts[0]),
                "real": float(parts[1]),
                "imag": float(parts[2]),
                "root": int(parts[3]),
                "spin": int(parts[4]),
                "ms": int(parts[5]),
            }
        )

    return {"state": state_num, "energy_cm": energy, "roots": roots}


def _iter_soc_states(lines: list[str]) -> Iterator[list[str]]:
    """Iterate over spin-orbit coupling (SOC) state blocks in the input text.

    Takes a list of text lines and yields blocks of lines corresponding to individual
    SOC states. Each block starts with "STATE n:" and continues until the next state
    or end of input.

    Args:
        lines (list[str]): List of text lines to parse, starting at the first SOC state.

    Yields:
        list[str]: Lines for a single SOC state block, including the state header line
            and all contribution lines until the next state.

    Example block:
        STATE 1: 0.000000
           1.000000    1.000000    0.000000     1    1    1
           0.000000    0.000000    0.000000     2    1    0
    """
    current_state = []

    for line in lines:
        line = line.strip()
        if not line:
            break

        if line.startswith("STATE"):
            if current_state:
                yield current_state
            current_state = [line]
        elif current_state:
            current_state.append(line)

    if current_state:  # Don't forget the last state
        yield current_state
