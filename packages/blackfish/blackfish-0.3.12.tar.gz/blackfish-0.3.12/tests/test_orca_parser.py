from pathlib import Path

import polars as pl
import pytest

from blackfish import OrcaParser

# Mock test data
MOCK_SUCCESSFUL_OUTPUT = """
                         *****************
                         * O   R   C   A *
                         *****************

           Program Version 5.0.3
FINAL SINGLE POINT ENERGY     -1528.908123456
TOTAL RUN TIME: 1 hour 23 minutes and 12 seconds
"""

MOCK_FAILED_OUTPUT = """
                         *****************
                         * O   R   C   A *
                         *****************

           Program Version 5.0.3
Error: SCF not converged!
"""

MOCK_IR_OUTPUT = """
-----------
IR SPECTRUM
-----------

 Mode   freq       eps      Int      T**2         TX        TY        TZ
       cm**-1   L/(mol*cm) km/mol    a.u.
----------------------------------------------------------------------------
  6:     12.42   0.000062    0.32  0.001569  ( 0.020681 -0.024061 -0.023714)
  7:     26.97   0.000089    0.45  0.001034  (-0.018061 -0.026532 -0.001852)

TOTAL RUN TIME: 1 hour 23 minutes and 12 seconds
"""


@pytest.fixture
def successful_parser():
    return OrcaParser(MOCK_SUCCESSFUL_OUTPUT.splitlines())


@pytest.fixture
def failed_parser():
    return OrcaParser(MOCK_FAILED_OUTPUT.splitlines())


class TestOrcaParserValidation:
    def test_successful_calculation(self, successful_parser):
        """Test that a successful calculation validates correctly"""
        successful_parser.validate()  # Should not raise an exception

    # Why tf does this _actually_ raise the ParsingError?!
    # def test_failed_calculation(self, failed_parser):
    #     """Test that a failed calculation raises ParsingError"""
    #     with pytest.raises(ParsingError):
    #         failed_parser.validate()

    def test_from_file(self, tmp_path):
        """Test file loading constructor"""
        test_file = tmp_path / "test.out"
        test_file.write_text(MOCK_SUCCESSFUL_OUTPUT)

        parser = OrcaParser.from_file(test_file)
        assert isinstance(parser, OrcaParser)
        parser.validate()  # Should not raise an exception


class TestOrcaParserEnergies:
    def test_fspe(self, successful_parser):
        """Test final single point energy parsing"""
        energy = successful_parser.get_energies().fspe()
        assert energy == pytest.approx(-1528.908123456)

        # Test unit conversion
        energy_ev = successful_parser.get_energies().fspe(unit="ev")
        assert energy_ev == pytest.approx(-41605.95, rel=1e-2)


class TestOrcaParserSpectrum:
    def test_ir_spectrum(self):
        """Test IR spectrum parsing"""
        parser = OrcaParser(MOCK_IR_OUTPUT.splitlines())
        df = parser.get_ir_spectrum()

        assert isinstance(df, pl.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == [
            "mode",
            "frequency_cm",
            "epsilon",
            "intensity",
            "t2",
            "tx",
            "ty",
            "tz",
            "rel_intensity",
        ]
        assert df["frequency_cm"][1] == pytest.approx(26.97)


def test_energy_conversion():
    """Test energy unit conversion utility"""
    assert OrcaParser.convert_energy(1.0, "hartree", "ev") == pytest.approx(27.211386)
    assert OrcaParser.convert_energy(27.211386, "ev", "hartree") == pytest.approx(1.0)


# Integration tests using actual ORCA output files
class TestOrcaParserIntegration:
    @pytest.fixture
    def test_files(self):
        # Return paths to actual test files
        return {
            "freq": Path("tests/data/ir_spectrum.txt"),
            "tddft": Path("tests/data/soc_absorption_spectrum.txt"),
            "roots": Path("tests/data/roots.txt"),
            "soc": Path("tests/data/soc_states.txt"),
        }

    def test_frequency_calculation(self, test_files):
        """Test parsing complete frequency calculation output"""
        parser = OrcaParser.from_file(test_files["freq"])

        ir_data = parser.get_ir_spectrum()
        assert isinstance(ir_data, pl.DataFrame)
        assert len(ir_data) > 0

        energies = parser.get_energies()
        assert energies.fspe() is not None
        assert energies.zero_point_energy() is not None

    def test_tddft_roots_calculation(self, test_files):
        """Test parsing complete TDDFT calculation output"""
        parser = OrcaParser.from_file(test_files["roots"])

        roots = parser.get_tddft_roots()
        assert isinstance(roots, pl.DataFrame)
        assert len(roots) > 0

    def test_soc_calculation(self, test_files):
        """Test parsing complete SOC calculation output"""
        parser = OrcaParser.from_file(test_files["soc"])

        soc_states = parser.get_soc_states()
        assert isinstance(soc_states, pl.DataFrame)
        assert len(soc_states) > 0
