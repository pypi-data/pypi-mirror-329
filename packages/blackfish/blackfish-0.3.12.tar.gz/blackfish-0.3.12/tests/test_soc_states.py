from pathlib import Path

import polars as pl
import pytest

from blackfish.parsing.soc_states import (
    _iter_soc_states,
    _parse_single_state,
    soc_states,
)

ROOT = Path(__file__).parent


@pytest.fixture
def sample_soc_output():
    return (ROOT / "data/soc_states.txt").read_text().splitlines()


@pytest.fixture
def sample_state_block():
    return [
        "STATE 1: 0.000000",
        "1.000000    1.000000    0.000000     1    1    1",
        "0.000000    0.000000    0.000000     2    1    0",
    ]


def test_soc_states_returns_dataframe(sample_soc_output):
    """Test that soc_states function returns a polars DataFrame"""
    result = soc_states(sample_soc_output)
    assert isinstance(result, pl.DataFrame)


def test_soc_states_correct_columns(sample_soc_output):
    """Test that the returned DataFrame has the expected columns"""
    result = soc_states(sample_soc_output)
    expected_columns = {"state", "spin", "root", "weight", "energy_cm"}
    assert set(result.columns) == expected_columns


def test_soc_states_data_types(sample_soc_output):
    """Test that the columns have the correct data types"""
    result = soc_states(sample_soc_output)
    assert result["state"].dtype == pl.Int64
    assert result["spin"].dtype == pl.Int64
    assert result["root"].dtype == pl.Int64
    assert result["weight"].dtype == pl.Float64
    assert result["energy_cm"].dtype == pl.Float64


def test_soc_states_non_empty(sample_soc_output):
    """Test that the DataFrame is not empty"""
    result = soc_states(sample_soc_output)
    assert len(result) > 0


def test_soc_states_weights_sum(sample_soc_output):
    """Test that weights sum to approximately 1.0 for each state"""
    result = soc_states(sample_soc_output)
    for state in result["state"].unique():
        state_weights = result.filter(pl.col("state") == state)["weight"]
        assert sum(state_weights) == pytest.approx(1.0, abs=5e-2)


# Tests for _parse_single_state helper function
def test_parse_single_state(sample_state_block):
    """Test parsing of a single state block"""
    result = _parse_single_state(sample_state_block)

    assert result["state"] == 1
    assert result["energy_cm"] == 0.0
    assert len(result["roots"]) == 2

    # Check first root
    assert result["roots"][0]["weight"] == 1.0
    assert result["roots"][0]["real"] == 1.0
    assert result["roots"][0]["imag"] == 0.0
    assert result["roots"][0]["root"] == 1
    assert result["roots"][0]["spin"] == 1
    assert result["roots"][0]["ms"] == 1


def test_parse_single_state_invalid_format():
    """Test parsing of invalid state block format"""
    invalid_block = ["STATE invalid: 0.0", "bad data"]
    with pytest.raises(ValueError):
        _parse_single_state(invalid_block)


# Tests for _iter_soc_states helper function
def test_iter_soc_states():
    """Test iteration over state blocks"""
    input_lines = [
        "STATE 1: 0.0",
        "1.0 1.0 0.0 1 1 1",
        "STATE 2: 100.0",
        "0.5 0.5 0.0 1 1 1",
        "0.5 0.5 0.0 2 1 0",
        "",
    ]

    states = list(_iter_soc_states(input_lines))
    print(states)
    assert len(states) == 2
    assert states[0][0] == "STATE 1: 0.0"
    assert states[1][0] == "STATE 2: 100.0"


def test_iter_soc_states_empty_input():
    """Test iteration with empty input"""
    states = list(_iter_soc_states([]))
    assert len(states) == 0


def test_soc_states_sorting(sample_soc_output):
    """Test that states are properly sorted"""
    result = soc_states(sample_soc_output)
    # Check that states are sorted by state number
    assert list(result["state"]) == sorted(result["state"])
    # Within each state, check that weights are sorted in descending order
    for state in result["state"].unique():
        state_weights = result.filter(pl.col("state") == state)["weight"]
        assert list(state_weights) == sorted(state_weights, reverse=True)


def test_soc_states_energy_values(sample_soc_output):
    """Test that energy values are consistent within each state"""
    result = soc_states(sample_soc_output)
    for state in result["state"].unique():
        state_energies = result.filter(pl.col("state") == state)["energy_cm"]
        # All energies for the same state should be identical
        assert len(set(state_energies)) == 1


def test_soc_states_valid_spins(sample_soc_output):
    """Test that spin values are valid"""
    result = soc_states(sample_soc_output)
    # Spin values should be positive integers
    assert all(isinstance(x, int) and x >= 0 for x in result["spin"])
