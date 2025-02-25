use polars::prelude::*;
use regex::Regex;
use std::error::Error;

/// Parses the spectral table preceded by its header into a Polars DataFrame.
///
/// The function looks for a header line containing
/// "SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS"
/// and then reads the table below it until an empty line is encountered.
///
/// # Arguments
///
/// * `input` - A string slice containing the full file contents.
///
/// # Returns
///
/// A Result with a DataFrame or an error.
///
/// # Example
///
/// ```rust
/// # use your_crate::parse_spectral_table;
/// let data = r#"SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
/// --------------------------------------------------------------------------------
///       Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|
///                           (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)
/// --------------------------------------------------------------------------------
///   0-6.0A  ->  1-6.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
///   5-6.0A  ->  7-4.0A    2.884592   23265.8   429.8   0.000000001   0.00000   0.00012   0.00016   0.00019
///
/// "#;
/// let df = parse_spectral_table(data).unwrap();
/// println!("{:?}", df);
/// ```

pub fn parse_soc_corr_abs_spectrum_casscf(input: &str) -> Result<DataFrame, Box<dyn Error>> {
    const CASSCF_HEADER: &str =
        "CASSCF (NEVPT2 diagonal energies) UV, CD spectra and dipole moments";
    parse_soc_corrected_absorption_spectrum(input, CASSCF_HEADER)
}

pub fn parse_soc_corr_abs_spectrum_qdpt(input: &str) -> Result<DataFrame, Box<dyn Error>> {
    const QDPT_HEADER: &str = "QDPT WITH NEVPT2 DIAGONAL ENERGIES";
    parse_soc_corrected_absorption_spectrum(input, QDPT_HEADER)
}

fn parse_soc_corrected_absorption_spectrum(
    input: &str,
    block_header: &str,
) -> Result<DataFrame, Box<dyn Error>> {
    // Define the header marker we require.
    const SOC_CORR_ABS_HEADER: &str =
        "SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS";

    // Regex for matching data rows.
    // This regex expects the first field to be a transition field (e.g. "0-6.0A  ->  1-6.0A")
    // followed by eight numeric fields.
    let re = Regex::new(
        r"(?x)
        ^\s*
        (?P<transition>\d+-[\d\.]+A\s*->\s*\d+-[\d\.]+A)\s+
        (?P<energy_ev>-?\d+\.\d+)\s+
        (?P<energy_cm>-?\d+\.\d+)\s+
        (?P<wavelength>-?\d+\.\d+)\s+
        (?P<fosc>-?\d+\.\d+)\s+
        (?P<d2>-?\d+\.\d+)\s+
        (?P<dx>-?\d+\.\d+)\s+
        (?P<dy>-?\d+\.\d+)\s+
        (?P<dz>-?\d+\.\d+)
        \s*$
    ",
    )?;

    let mut transitions = Vec::new();
    let mut energy_ev = Vec::new();
    let mut energy_cm = Vec::new();
    let mut wavelength = Vec::new();
    let mut fosc = Vec::new();
    let mut d2 = Vec::new();
    let mut dx = Vec::new();
    let mut dy = Vec::new();
    let mut dz = Vec::new();

    let mut lines = input.lines().peekable();
    let mut in_casscf = false;
    let mut table_started = false;

    // Look for the header and the subsequent table header lines.
    while let Some(line) = lines.next() {
        if !line.contains(block_header) && !in_casscf {
            continue;
        } else {
            in_casscf = true
        }

        if line.contains(SOC_CORR_ABS_HEADER) {
            // We found the required header.
            // Skip the next couple of lines (the dashed line and the column names)
            // until we reach the dashed line that follows the column names.
            for _ in 0..3 {
                lines.next();
            }
            table_started = true;
            break;
        }
    }

    if !table_started {
        return Err("Required header not found in the file.".into());
    }

    // Process rows until an empty line is reached.
    for line in lines {
        let line = line.trim();
        if line.is_empty() {
            break;
        }
        // Skip dashed lines if any.
        if line.chars().all(|c| c == '-' || c.is_whitespace()) {
            continue;
        }
        if let Some(caps) = re.captures(line) {
            transitions.push(caps["transition"].to_string());
            energy_ev.push(caps["energy_ev"].parse::<f64>()?);
            energy_cm.push(caps["energy_cm"].parse::<f64>()?);
            wavelength.push(caps["wavelength"].parse::<f64>()?);
            fosc.push(caps["fosc"].parse::<f64>()?);
            d2.push(caps["d2"].parse::<f64>()?);
            dx.push(caps["dx"].parse::<f64>()?);
            dy.push(caps["dy"].parse::<f64>()?);
            dz.push(caps["dz"].parse::<f64>()?);
        }
    }

    // Create Polars Series for each column.
    let s_transition = Column::new("transition".into(), transitions);
    let s_energy_ev = Column::new("energy_ev".into(), energy_ev);
    let s_energy_cm = Column::new("energy_cm".into(), energy_cm);
    let s_wavelength = Column::new("wavelength_nm".into(), wavelength);
    let s_fosc = Column::new("fosc_d2".into(), fosc);
    let s_d2 = Column::new("d2".into(), d2);
    let s_dx = Column::new("dx".into(), dx);
    let s_dy = Column::new("dy".into(), dy);
    let s_dz = Column::new("dz".into(), dz);

    // Build and return the DataFrame.
    let df = DataFrame::new(vec![
        s_transition,
        s_energy_ev,
        s_energy_cm,
        s_wavelength,
        s_fosc,
        s_d2,
        s_dx,
        s_dy,
        s_dz,
    ])?;

    Ok(df)
}
