from pathlib import Path

import polars as pl
import pytest

from blackfish.parsing.roots import _iter_roots, _parse_single_root, roots

# Get the project root directory
ROOT = Path(__file__).parent


def test_roots():
    # Test the main roots function
    test_file_output = (ROOT / "data/roots.txt").read_text().splitlines()
    df = roots(test_file_output)

    # Basic DataFrame checks
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()

    # Check expected columns
    expected_columns = ["root", "mult", "donor", "acceptor", "weight", "energy_cm"]
    assert all(col in df.columns for col in expected_columns)

    # Check sorting
    assert df["root"].is_sorted()

    # Check data types
    assert df["root"].dtype == pl.Int64
    assert df["mult"].dtype == pl.Int64
    assert df["donor"].dtype == pl.Utf8
    assert df["acceptor"].dtype == pl.Utf8
    assert df["weight"].dtype == pl.Float64
    assert df["energy_cm"].dtype == pl.Float64


def test_parse_single_root():
    # Test sample root block
    test_root_lines = [
        "STATE  1:  E=      0.021089 au     2.345 eV   18915.8 cm**-1  <S**2> =  0.000  Mult 1",
        "      124a ->  125a  :     0.707",
        "      123a ->  126a  :     0.293",
    ]

    result = _parse_single_root(test_root_lines)

    # Check parsed data
    assert result["root"] == 1
    assert result["energy_ev"] == pytest.approx(2.345)
    assert result["energy_cm"] == pytest.approx(18915.8)
    assert result["spin_projection"] == pytest.approx(0.000)
    assert result["mult"] == 1

    # Check orbital transitions
    transitions = result["orbital_transitions"]
    assert len(transitions) == 2
    assert transitions[0]["donor"] == "124a"
    assert transitions[0]["acceptor"] == "125a"
    assert transitions[0]["weight"] == pytest.approx(0.707)


def test_iter_roots():
    # Test root block iterator
    test_lines = [
        "STATE  1:  E=   2.345 eV   18915.8 cm**-1  <S**2> =  0.000  Mult=1",
        "      124a ->  125a  :     0.707",
        "",
        "STATE  2:  E=   3.456 eV   27875.9 cm**-1  <S**2> =  0.000  Mult=1",
        "      123a ->  125a  :     0.656",
        "",
        "",
    ]

    root_blocks = list(_iter_roots(test_lines))

    # Check number of root blocks
    assert len(root_blocks) == 2

    # Check first root block
    assert len(root_blocks[0]) == 2
    assert root_blocks[0][0].startswith("STATE  1:")

    # Check second root block
    assert len(root_blocks[1]) == 2
    assert root_blocks[1][0].startswith("STATE  2:")
