/// Parse the "CAS-SCF states" section from ORCA output.
///
/// This function looks for lines like:
///     ROOT   0:  E=   -2198.4372074675 Eh
/// and collects the root numbers and energies into a DataFrame.
///
/// # Arguments
///
/// * `input` - A string slice containing the ORCA output.
///
/// # Returns
///
/// A `Result<DataFrame, PolarsError>` containing a DataFrame with columns "root" (i32)
/// and "energy_Eh" (f64).
///
/// # Example
///
/// ```
/// let output = r#"
/// ---------------------------------------------
/// CAS-SCF STATES FOR BLOCK  0 MULT= 6 NROOTS= 1
/// ---------------------------------------------
///
/// ROOT   0:  E=   -2198.4372074675 Eh
/// "#;
/// let df = parse_casscf_states(output).unwrap();
/// println!("{:?}", df);
/// ```
pub fn parse_casscf_states(input: &str) -> Result<DataFrame, PolarsError> {
    let re = Regex::new(r"ROOT\s+(\d+):\s+E=\s+([-\d\.]+)\s+Eh").unwrap();
    let mut roots = Vec::new();
    let mut energies = Vec::new();

    for cap in re.captures_iter(input) {
        roots.push(cap[1].parse::<i32>().unwrap());
        energies.push(cap[2].parse::<f64>().unwrap());
    }

    let s_roots = Column::new("root".into(), roots);
    let s_energy = Column::new("energy_Eh".into(), energies);
    DataFrame::new(vec![s_roots, s_energy])
}

/// Parse SA-CASSCF transition energies.
pub fn parse_sa_casscf_transition_energies(input: &str) -> Result<DataFrame, PolarsError> {
    // Matches lines like: "   1:    0    4   0.075424     2.052  16553.7"
    let re = Regex::new(r"^\s*(\d+):\s+(\d+)\s+(\d+)\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)").unwrap();
    let mut state = Vec::new();
    let mut root = Vec::new();
    let mut mult = Vec::new();
    let mut de_au = Vec::new();
    let mut de_ev = Vec::new();
    let mut de_cm = Vec::new();

    for cap in re.captures_iter(input) {
        state.push(cap[1].parse::<i32>().unwrap());
        root.push(cap[2].parse::<i32>().unwrap());
        mult.push(cap[3].parse::<i32>().unwrap());
        de_au.push(cap[4].parse::<f64>().unwrap());
        de_ev.push(cap[5].parse::<f64>().unwrap());
        de_cm.push(cap[6].parse::<f64>().unwrap());
    }
    let s_state = Column::new("state".into(), state);
    let s_root = Column::new("root".into(), root);
    let s_mult = Column::new("mult".into(), mult);
    let s_de_au = Column::new("de_au".into(), de_au);
    let s_de_ev = Column::new("de_ev".into(), de_ev);
    let s_de_cm = Column::new("de_cm".into(), de_cm);
    DataFrame::new(vec![s_state, s_root, s_mult, s_de_au, s_de_ev, s_de_cm])
}

// /// Parse ENERGY COMPONENTS.
// pub fn parse_energy_components(input: &str) -> Result<DataFrame, PolarsError> {
//     // Matches lines like: "One electron energy          :  -8114.090485189 Eh     -220795.6271 eV"
//     let re = Regex::new(r"(?m)^(One electron energy|Two electron energy|Nuclear repulsion energy)\s*:\s*([\-\d\.]+)\s+Eh\s+([\-\d\.]+)\s+eV").unwrap();
//     let mut component = Vec::new();
//     let mut energy_au = Vec::new();
//     let mut energy_ev = Vec::new();

//     for cap in re.captures_iter(input) {
//         component.push(cap[1].to_string());
//         energy_au.push(cap[2].parse::<f64>().unwrap());
//         energy_ev.push(cap[3].parse::<f64>().unwrap());
//     }
//     let s_comp = Column::new("component".into(), component);
//     let s_au = Column::new("energy_Eh".into(), energy_au);
//     let s_ev = Column::new("energy_eV".into(), energy_ev);
//     DataFrame::new(vec![s_comp, s_au, s_ev])
// }

// /// Parse Loewdin orbital compositions.
// pub fn parse_loewdin_orbital_compositions(input: &str) -> Result<DataFrame, PolarsError> {
//     // This example parser extracts rows starting with an index and element label.
//     let re = Regex::new(r"(?m)^(\d+\s+\w+\s+\w+)\s+((?:[\d\.]+\s+)+)").unwrap();
//     let mut label = Vec::new();
//     let mut values = Vec::new();
//     for cap in re.captures_iter(input) {
//         label.push(cap[1].trim().to_string());
//         // Split numbers and parse
//         let nums: Vec<f64> = cap[2]
//             .split_whitespace()
//             .filter_map(|s| s.parse::<f64>().ok())
//             .collect();
//         // For simplicity we join back as comma-separated string
//         values.push(format!("{:?}", nums));
//     }
//     let s_label = Column::new("label".into(), label);
//     let s_values = Column::new("values".into(), values);
//     DataFrame::new(vec![s_label, s_values])
// }

// /// Parse Loewdin reduced active MOs.
// pub fn parse_loewdin_reduced_active_mos(input: &str) -> Result<DataFrame, PolarsError> {
//     // Similar to orbital compositions parser.
//     let re = Regex::new(r"(?m)^(\d+\s+\w+\s+\w+)\s+((?:[\d\.\-]+\s+)+)").unwrap();
//     let mut label = Vec::new();
//     let mut values = Vec::new();
//     for cap in re.captures_iter(input) {
//         label.push(cap[1].trim().to_string());
//         let nums: Vec<f64> = cap[2]
//             .split_whitespace()
//             .filter_map(|s| s.parse::<f64>().ok())
//             .collect();
//         values.push(format!("{:?}", nums));
//     }
//     let s_label = Column::new("label".into(), label);
//     let s_values = Column::new("values".into(), values);
//     DataFrame::new(vec![s_label, s_values])
// }

/// Parse NEVPT2 transition energies.
pub fn parse_nevpt2_transition_energies(input: &str) -> Result<DataFrame, PolarsError> {
    // Similar to SA-CASSCF transition energies parser.
    let re =
        Regex::new(r"(?m)^\s*(\d+):\s+(\d+)\s+(\d+)\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)").unwrap();
    let mut state = Vec::new();
    let mut root = Vec::new();
    let mut mult = Vec::new();
    let mut de_au = Vec::new();
    let mut de_ev = Vec::new();
    let mut de_cm = Vec::new();
    for cap in re.captures_iter(input) {
        state.push(cap[1].parse::<i32>().unwrap());
        root.push(cap[2].parse::<i32>().unwrap());
        mult.push(cap[3].parse::<i32>().unwrap());
        de_au.push(cap[4].parse::<f64>().unwrap());
        de_ev.push(cap[5].parse::<f64>().unwrap());
        de_cm.push(cap[6].parse::<f64>().unwrap());
    }
    let s_state = Column::new("state".into(), state);
    let s_root = Column::new("root".into(), root);
    let s_mult = Column::new("mult".into(), mult);
    let s_de_au = Column::new("de_au".into(), de_au);
    let s_de_ev = Column::new("de_ev".into(), de_ev);
    let s_de_cm = Column::new("de_cm".into(), de_cm);
    DataFrame::new(vec![s_state, s_root, s_mult, s_de_au, s_de_ev, s_de_cm])
}

/// Parse SOC states.
pub fn parse_soc_states(input: &str) -> Result<DataFrame, PolarsError> {
    // Extract lines with "STATE" header and following vector rows.
    let re_state = Regex::new(r"(?m)^STATE\s+(\d+):\s+([\d\.]+)").unwrap();
    let mut state = Vec::new();
    let mut header_val = Vec::new();
    for cap in re_state.captures_iter(input) {
        state.push(cap[1].parse::<i32>().unwrap());
        header_val.push(cap[2].parse::<f64>().unwrap());
    }
    let s_state = Column::new("state".into(), state);
    let s_header = Column::new("header_val".into(), header_val);
    DataFrame::new(vec![s_state, s_header])
}

/// Parse SOC energy levels & populations.
pub fn parse_soc_energy_levels(input: &str) -> Result<DataFrame, PolarsError> {
    // Matches lines like:
    // "   0 :         0.000     0.0000         1.67e-01"
    let re =
        Regex::new(r"(?m)^\s*(\d+)\s*:\s*([\d\.\-]+)\s+([\d\.\-]+)\s+([\deE\+\-\.]+)").unwrap();
    let mut level = Vec::new();
    let mut energy_cm = Vec::new();
    let mut energy_ev = Vec::new();
    let mut population = Vec::new();
    for cap in re.captures_iter(input) {
        level.push(cap[1].parse::<i32>().unwrap());
        energy_cm.push(cap[2].parse::<f64>().unwrap());
        energy_ev.push(cap[3].parse::<f64>().unwrap());
        population.push(cap[4].parse::<f64>().unwrap());
    }
    let s_level = Column::new("level".into(), level);
    let s_cm = Column::new("energy_cm".into(), energy_cm);
    let s_ev = Column::new("energy_ev".into(), energy_ev);
    let s_pop = Column::new("population".into(), population);
    DataFrame::new(vec![s_level, s_cm, s_ev, s_pop])
}

// /// Parse SOC absorption spectrum.
// pub fn parse_soc_absorption_spectrum(input: &str) -> Result<DataFrame, PolarsError> {
//     // Matches lines with 9 columns (after the header separator)
//     let re = Regex::new(r"(?m)^\s*(\S+)\s+->\s+(\S+)\s+([\d\.Ee\+\-]+)\s+([\d\.Ee\+\-]+)\s+([\d\.Ee\+\-]+)\s+([\d\.Ee\+\-]+)\s+([\d\.Ee\+\-]+)\s+([\d\.Ee\+\-]+)\s+([\d\.Ee\+\-]+)").unwrap();
//     let mut trans_from = Vec::new();
//     let mut trans_to = Vec::new();
//     let mut energy_ev = Vec::new();
//     let mut energy_cm = Vec::new();
//     let mut wavelength = Vec::new();
//     let mut fosc = Vec::new();
//     let mut d2 = Vec::new();
//     let mut dx = Vec::new();
//     let mut dy = Vec::new();
//     let mut dz: Vec<f64> = Vec::new();
//     for cap in re.captures_iter(input) {
//         trans_from.push(cap[1].to_string());
//         trans_to.push(cap[2].to_string());
//         energy_ev.push(cap[3].parse::<f64>().unwrap());
//         energy_cm.push(cap[4].parse::<f64>().unwrap());
//         wavelength.push(cap[5].parse::<f64>().unwrap());
//         fosc.push(cap[6].parse::<f64>().unwrap());
//         d2.push(cap[7].parse::<f64>().unwrap());
//         dx.push(cap[8].parse::<f64>().unwrap());
//         dy.push(cap[9].parse::<f64>().unwrap());
//         // Assuming |DZ| is not printed separately; adjust as needed.
//     }
//     let s_from = Column::new("transition_from".into(), trans_from);
//     let s_to = Column::new("transition_to".into(), trans_to);
//     let s_e_ev = Column::new("energy_eV".into(), energy_ev);
//     let s_e_cm = Column::new("energy_cm".into(), energy_cm);
//     let s_wave = Column::new("wavelength_nm".into(), wavelength);
//     let s_fosc = Column::new("fosc".into(), fosc);
//     let s_d2 = Column::new("d2".into(), d2);
//     let s_dx = Column::new("dx".into(), dx);
//     let s_dy = Column::new("dy".into(), dy);
//     DataFrame::new(vec![
//         s_from, s_to, s_e_ev, s_e_cm, s_wave, s_fosc, s_d2, s_dx, s_dy,
//     ])
// }

/// Parse SOC energy levels with NEVPT2.
pub fn parse_soc_energy_levels_with_nevpt2(input: &str) -> Result<DataFrame, PolarsError> {
    // Matches lines like: "   0:            0.00        0.0000       8.10e-02"
    let re = Regex::new(r"(?m)^\s*(\d+):\s+([\d\.\-]+)\s+([\d\.\-]+)\s+([\deE\+\-]+)").unwrap();
    let mut level = Vec::new();
    let mut energy_cm = Vec::new();
    let mut energy_ev = Vec::new();
    let mut population = Vec::new();
    for cap in re.captures_iter(input) {
        level.push(cap[1].parse::<i32>().unwrap());
        energy_cm.push(cap[2].parse::<f64>().unwrap());
        energy_ev.push(cap[3].parse::<f64>().unwrap());
        population.push(cap[4].parse::<f64>().unwrap());
    }
    let s_level = Column::new("level".into(), level);
    let s_cm = Column::new("energy_cm".into(), energy_cm);
    let s_ev = Column::new("energy_ev".into(), energy_ev);
    let s_pop = Column::new("population".into(), population);
    DataFrame::new(vec![s_level, s_cm, s_ev, s_pop])
}

// /// Parse AILFT output.
// pub fn parse_ailft(input: &str) -> Result<DataFrame, PolarsError> {
//     // As an example, extract the ligand field one-electron matrix.
//     let re = Regex::new(r"(?m)^Orbital\s+Energy\s+\(eV\).*?\n((?:.*\n)+?)\n").unwrap();
//     if let Some(cap) = re.captures(input) {
//         // For simplicity, return the whole block as a single column.
//         let matrix_block = cap[1].trim().to_string();
//         let s_matrix = Column::new("ailft_matrix".into(), &[matrix_block]);
//         DataFrame::new(vec![s_matrix])
//     } else {
//         Err(PolarsError::NoData("AILFT matrix not found".into()))
//     }
// }

/// Extend the parsed struct with additional fields.
#[derive(Debug)]
pub struct OrcaParsed {
    pub active_space: DataFrame,
    pub casscf_states: DataFrame,
    pub sa_casscf_transitions: DataFrame,
    pub energy_components: DataFrame,
    pub loewdin_orbital_compositions: DataFrame,
    pub loewdin_reduced_active_mos: DataFrame,
    pub nevpt2_transitions: DataFrame,
    pub soc_states: DataFrame,
    pub soc_energy_levels: DataFrame,
    pub soc_absorption: DataFrame,
    pub soc_levels_nevpt2: DataFrame,
    pub ailft: DataFrame,
}

/// Parse the complete ORCA output.
pub fn parse_orca_output(content: &str) -> Result<OrcaParsed, PolarsError> {
    let active_space = parse_active_space(content)?;
    let casscf_states = parse_casscf_states(content)?;
    let sa_casscf_transitions = parse_sa_casscf_transition_energies(content)?;
    let energy_components = parse_energy_components(content)?;
    let loewdin_orbital_compositions = parse_loewdin_orbital_compositions(content)?;
    let loewdin_reduced_active_mos = parse_loewdin_reduced_active_mos(content)?;
    let nevpt2_transitions = parse_nevpt2_transition_energies(content)?;
    let soc_states = parse_soc_states(content)?;
    let soc_energy_levels = parse_soc_energy_levels(content)?;
    let soc_absorption = parse_soc_absorption_spectrum(content)?;
    let soc_levels_nevpt2 = parse_soc_energy_levels_with_nevpt2(content)?;
    let ailft = parse_ailft(content)?;

    Ok(OrcaParsed {
        active_space,
        casscf_states,
        sa_casscf_transitions,
        energy_components,
        loewdin_orbital_compositions,
        loewdin_reduced_active_mos,
        nevpt2_transitions,
        soc_states,
        soc_energy_levels,
        soc_absorption,
        soc_levels_nevpt2,
        ailft,
    })
}
