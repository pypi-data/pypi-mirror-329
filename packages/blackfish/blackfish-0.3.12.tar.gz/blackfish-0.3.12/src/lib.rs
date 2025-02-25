pub mod parsers;
pub use parsers::casscf::*;

use pyo3::prelude::*;

fn read(file: &str) -> String {
    std::fs::read_to_string(file).expect("Unable to read file")
}

/// Ab initio LFT one electron eigenfunctions of CASSCF wavefunction
#[pyfunction]
fn one_electron_eigenfunctions(path: &str) -> PyResult<pyo3_polars::PyDataFrame> {
    let df = pyo3_polars::PyDataFrame(
        parse_lf_one_electron_eigenfunctions_casscf(read(path).as_str()).unwrap(),
    );
    Ok(df)
}

/// Ab initio LFT one electron eigenfunctions of NEVPT2 wavefunction
#[pyfunction]
fn nevpt2_one_electron_eigenfunctions(path: &str) -> PyResult<pyo3_polars::PyDataFrame> {
    let df = pyo3_polars::PyDataFrame(
        parse_lf_one_electron_eigenfunctions_nevpt2(read(path).as_str()).unwrap(),
    );
    Ok(df)
}

/// Spin-orbit corrected absorption spectrum of the CASSCF wavefunction
#[pyfunction]
fn soc_corrected_absorption_spectrum(path: &str) -> PyResult<pyo3_polars::PyDataFrame> {
    let df =
        pyo3_polars::PyDataFrame(parse_soc_corr_abs_spectrum_casscf(read(path).as_str()).unwrap());
    Ok(df)
}

/// Spin-orbit corrected absorption spectrum of the QDPT wavefunction
#[pyfunction]
fn qdpt_soc_corrected_absorption_spectrum(path: &str) -> PyResult<pyo3_polars::PyDataFrame> {
    let df =
        pyo3_polars::PyDataFrame(parse_soc_corr_abs_spectrum_qdpt(read(path).as_str()).unwrap());
    Ok(df)
}

/// Lödwin reduced active MOs
#[pyfunction]
fn loewdin_reduced_active_mos(path: &str) -> PyResult<pyo3_polars::PyDataFrame> {
    let df =
        pyo3_polars::PyDataFrame(parse_loewdin_reduced_active_mos(read(path).as_str()).unwrap());
    Ok(df)
}

/// Löwdin orbital compositions
#[pyfunction]
fn loewdin_orbital_compositions(path: &str) -> PyResult<pyo3_polars::PyDataFrame> {
    let df =
        pyo3_polars::PyDataFrame(parse_loewdin_orbital_compositions(read(path).as_str()).unwrap());
    Ok(df)
}

/// List of active space orbital IDs
#[pyfunction]
fn active_space_orbitals(path: &str) -> PyResult<Vec<u32>> {
    let active_space = parse_active_space_range(read(path).as_str()).unwrap();
    Ok(active_space)
}

#[pymodule]
fn blackfish(m: &Bound<'_, PyModule>) -> PyResult<()> {
    let ailft = PyModule::new(m.py(), "ailft")?;
    ailft.add_function(wrap_pyfunction!(one_electron_eigenfunctions, m)?)?;
    ailft.add_function(wrap_pyfunction!(nevpt2_one_electron_eigenfunctions, m)?)?;
    ailft.add_function(wrap_pyfunction!(active_space_orbitals, m)?)?;
    m.add_submodule(&ailft)?;

    let casscf = PyModule::new(m.py(), "casscf")?;
    casscf.add_function(wrap_pyfunction!(soc_corrected_absorption_spectrum, m)?)?;
    casscf.add_function(wrap_pyfunction!(qdpt_soc_corrected_absorption_spectrum, m)?)?;
    casscf.add_function(wrap_pyfunction!(active_space_orbitals, m)?)?;
    m.add_submodule(&casscf)?;

    m.add_function(wrap_pyfunction!(loewdin_reduced_active_mos, m)?)?;
    m.add_function(wrap_pyfunction!(loewdin_orbital_compositions, m)?)?;

    Ok(())
}
