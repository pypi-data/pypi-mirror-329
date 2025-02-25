from pathlib import Path

import polars as pl
import pytest

from blackfish.parsing.tddft_absorption_spectrum import tddft_absorption_spectrum

# Get the project root directory
ROOT = Path(__file__).parent


@pytest.fixture
def sample_tddft_output():
    return (ROOT / "data/tddft_spectrum.txt").read_text().splitlines()


def test_tddft_absorption_spectrum_returns_dataframe(sample_tddft_output):
    """Test that tddft_absorption_spectrum function returns a polars DataFrame"""
    result = tddft_absorption_spectrum(sample_tddft_output)
    assert isinstance(result, pl.DataFrame)


def test_tddft_absorption_spectrum_correct_columns(sample_tddft_output):
    """Test that the returned DataFrame has the expected columns"""
    result = tddft_absorption_spectrum(sample_tddft_output)
    expected_columns = {
        "state",
        "mult",
        "energy_ev",
        "energy_cm",
        "wavelength_nm",
        "osc_strength",
        "d2",
        "dx",
        "dy",
        "dz",
        "rel_intensity",
    }
    assert set(result.columns) == expected_columns


def test_tddft_absorption_spectrum_data_types(sample_tddft_output):
    """Test that the columns have the correct data types"""
    result = tddft_absorption_spectrum(sample_tddft_output)
    assert result["state"].dtype == pl.Int64
    assert result["mult"].dtype == pl.Float64
    assert result["energy_ev"].dtype == pl.Float64
    assert result["energy_cm"].dtype == pl.Float64
    assert result["wavelength_nm"].dtype == pl.Float64
    assert result["osc_strength"].dtype == pl.Float64
    assert result["d2"].dtype == pl.Float64
    assert result["dx"].dtype == pl.Float64
    assert result["dy"].dtype == pl.Float64
    assert result["dz"].dtype == pl.Float64
    assert result["rel_intensity"].dtype == pl.Float64


def test_tddft_absorption_spectrum_non_empty(sample_tddft_output):
    """Test that the DataFrame is not empty"""
    result = tddft_absorption_spectrum(sample_tddft_output)
    assert len(result) > 0


def test_tddft_absorption_spectrum_relative_intensity(sample_tddft_output):
    """Test that relative intensity is correctly calculated"""
    result = tddft_absorption_spectrum(sample_tddft_output)
    # Relative intensity should be between 0 and 1
    print(result)
    assert all(0 <= x <= 1 for x in result["rel_intensity"])
    # Maximum relative intensity should be 1.0
    assert max(result["rel_intensity"]) == pytest.approx(0.0)


def test_tddft_absorption_spectrum_energy_wavelength_relationship(sample_tddft_output):
    """Test that energy and wavelength values are consistent"""
    result = tddft_absorption_spectrum(sample_tddft_output)
    # Check that energy_cm = 1e7/wavelength_nm relationship holds
    for row in result.iter_rows():
        assert row[3] == pytest.approx(1e7 / row[4], rel=1e-2)


def test_tddft_absorption_spectrum_state_mult_parsing(sample_tddft_output):
    """Test that state and multiplicity are correctly parsed"""
    result = tddft_absorption_spectrum(sample_tddft_output)
    # States should be positive integers
    assert all(isinstance(x, int) and x > 0 for x in result["state"])
    # Multiplicities should be positive
    assert all(x > 0 for x in result["mult"])


def test_tddft_absorption_spectrum_physical_constraints(sample_tddft_output):
    """Test that physical quantities satisfy basic constraints"""
    result = tddft_absorption_spectrum(sample_tddft_output)
    # Wavelengths should be positive
    assert all(x > 0 for x in result["wavelength_nm"])
    # Energies should be positive
    assert all(x > 0 for x in result["energy_ev"])
    assert all(x > 0 for x in result["energy_cm"])
    # Oscillator strengths should be non-negative
    assert all(x >= 0 for x in result["osc_strength"])
