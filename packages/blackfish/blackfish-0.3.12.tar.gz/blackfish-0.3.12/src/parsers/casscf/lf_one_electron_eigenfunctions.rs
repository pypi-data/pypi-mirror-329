use polars::prelude::*;
use regex::Regex;

// -----------------------------------------
// The ligand field one electron eigenfunctions:
// -----------------------------------------
// Orbital    Energy (eV)  Energy(cm-1)      dz2        dxz        dyz        dx2-y2     dxy
//     1          0.000        0.0        -0.000950  -0.017354  -0.098628  -0.796596   0.596159
//     2          0.450     3629.1        -0.035351   0.998473  -0.037986  -0.018815  -0.002417
//     3          0.494     3985.4        -0.085951   0.033457   0.990765  -0.072105   0.068400
//     4          1.566    12630.1         0.064974   0.015257  -0.006488   0.598075   0.798630
//     5          2.198    17725.0        -0.993549  -0.037406  -0.084688   0.046781   0.045826
// Ligand field orbitals were stored in 02_ailft.nevpt2.lft.gbw

pub fn parse_lf_one_electron_eigenfunctions_nevpt2(
    input: &str,
) -> Result<DataFrame, Box<dyn std::error::Error>> {
    const BLOCK_HEADER: &str = "AILFT MATRIX ELEMENTS (NEVPT2)";
    parse_lf_one_electron_eigenfunctions(input, BLOCK_HEADER)
}

pub fn parse_lf_one_electron_eigenfunctions_casscf(
    input: &str,
) -> Result<DataFrame, Box<dyn std::error::Error>> {
    const BLOCK_HEADER: &str = "AILFT MATRIX ELEMENTS (CASSCF)";
    parse_lf_one_electron_eigenfunctions(input, BLOCK_HEADER)
}

pub fn parse_lf_one_electron_eigenfunctions(
    input: &str,
    block_header: &str,
) -> Result<DataFrame, Box<dyn std::error::Error>> {
    // Define the header marker we require.
    const HEADER: &str = "The ligand field one electron eigenfunctions";

    // Regex for matching data rows.
    // followed by eight numeric fields.
    let re = Regex::new(
        r"^\s*(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)",
    )?;

    let mut orbital = Vec::new();
    let mut energy_ev = Vec::new();
    let mut energy_cm = Vec::new();
    let mut dz2 = Vec::new();
    let mut dxz = Vec::new();
    let mut dyz = Vec::new();
    let mut dx2y2 = Vec::new();
    let mut dxy = Vec::new();

    let mut lines = input.lines().peekable();
    let mut in_block = false;
    let mut table_started = false;

    // Look for the header and the subsequent table header lines.
    while let Some(line) = lines.next() {
        if !line.contains(block_header) && !in_block {
            continue;
        } else {
            in_block = true
        }

        if line.contains(HEADER) {
            // We found the required header.
            // Skip the next couple of lines (the dashed line and the column names)
            // until we reach the dashed line that follows the column names.
            for _ in 0..2 {
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
        if line.contains("Ligand field orbitals") || line.is_empty() {
            break;
        }
        // Skip dashed lines if any.
        if line.chars().all(|c| c == '-' || c.is_whitespace()) {
            continue;
        }
        if let Some(caps) = re.captures(line) {
            orbital.push(caps.get(1).unwrap().as_str().parse::<i64>()?);
            energy_ev.push(caps.get(2).unwrap().as_str().parse::<f64>()?);
            energy_cm.push(caps.get(3).unwrap().as_str().parse::<f64>()?);
            dz2.push(caps.get(4).unwrap().as_str().parse::<f64>()?);
            dxz.push(caps.get(5).unwrap().as_str().parse::<f64>()?);
            dyz.push(caps.get(6).unwrap().as_str().parse::<f64>()?);
            dx2y2.push(caps.get(7).unwrap().as_str().parse::<f64>()?);
            dxy.push(caps.get(8).unwrap().as_str().parse::<f64>()?);
        }
    }

    // Create Polars Series for each column.
    let s_transition = Column::new("orbital".into(), orbital);
    let s_energy_ev = Column::new("energy_ev".into(), energy_ev);
    let s_energy_cm = Column::new("energy_cm".into(), energy_cm);
    let s_dz2 = Column::new("dz2".into(), dz2);
    let s_dxz = Column::new("dxz".into(), dxz);
    let s_dyz = Column::new("dyz".into(), dyz);
    let s_dx2y2 = Column::new("dx2y2".into(), dx2y2);
    let s_dxy = Column::new("dxy".into(), dxy);

    // Build and return the DataFrame.
    let df = DataFrame::new(vec![
        s_transition,
        s_energy_ev,
        s_energy_cm,
        s_dz2,
        s_dxz,
        s_dyz,
        s_dx2y2,
        s_dxy,
    ])?;

    Ok(df)
}
