use polars::prelude::*;
use regex::Regex;

pub fn parse_loewdin_orbital_compositions(
    input: &str,
) -> Result<DataFrame, Box<dyn std::error::Error>> {
    let re_header = Regex::new(r"^\s*LOEWDIN ORBITAL-COMPOSITIONS\s*$")?;
    parse_orbital_compositions(input, re_header)
}

pub fn parse_loewdin_reduced_active_mos(
    input: &str,
) -> Result<DataFrame, Box<dyn std::error::Error>> {
    let re_header = Regex::new(r"^\s*LOEWDIN REDUCED ACTIVE MOs\s*$")?;
    parse_orbital_compositions(input, re_header)
}

fn parse_orbital_compositions(
    input: &str,
    re_header: Regex,
) -> Result<DataFrame, Box<dyn std::error::Error>> {
    let mut orbital_ids: Vec<i32> = Vec::new();
    let mut energies: Vec<f64> = Vec::new();
    let mut occupancies: Vec<f64> = Vec::new();
    let mut atom_indices: Vec<i32> = Vec::new();
    let mut elements: Vec<String> = Vec::new();
    let mut orbital_types: Vec<String> = Vec::new();
    let mut weights: Vec<f64> = Vec::new();

    let mut current_energies = Vec::new();
    let mut current_occupancies = Vec::new();
    let mut in_block = false;
    let mut empty_line_count = 0;

    let re_dashes = Regex::new(r"^-+\s*$")?;
    let re_float_line = Regex::new(r"^\s*((?:-?\d+\.\d+\s*)+)$")?;
    let re_orbital_line = Regex::new(r"^(\d+)\s+(\S+)\s+(\S+)\s+((?:-?\d+\.\d+\s*)+)$")?;

    for line in input.lines() {
        let line_trim = line.trim();

        // This is a complicated if statement,
        // but after the reduced active MO table, there is only one empty line.
        // To still catch this, we look for the start of the next header (----),
        // in_block to make sure we're not triggering on any (---), and
        // the emtpy_line_count to make sure we're not hitting the underscore of the header.
        // Well, at least it works.
        if line_trim.starts_with("----------------------------")
            && in_block
            && empty_line_count == 1
        {
            println!("{:?}", line);
            break;
        }

        if line_trim.is_empty() {
            // if line_trim.is_empty() {
            empty_line_count += 1;
            if in_block && empty_line_count >= 2 {
                break;
            }
            continue;
        }

        empty_line_count = 0;

        if re_header.is_match(line_trim) {
            in_block = true;
            continue;
        }

        if !in_block || re_dashes.is_match(line_trim) {
            continue;
        }

        if let Some(caps) = re_float_line.captures(line_trim) {
            let floats: Vec<f64> = caps[1]
                .split_whitespace()
                .filter_map(|s| s.parse::<f64>().ok())
                .collect();

            if current_energies.is_empty() {
                current_energies = floats;
            } else if current_occupancies.is_empty() {
                current_occupancies = floats;
            }
            continue;
        }

        if let Some(caps) = re_orbital_line.captures(line_trim) {
            let atom_index = caps[1].parse::<i32>()?;
            let element = caps[2].to_string();
            let orbital_type = caps[3].to_string();
            let contributions: Vec<f64> = caps[4]
                .split_whitespace()
                .filter_map(|s| s.parse::<f64>().ok())
                .collect();

            for (orbital_id, &contribution) in contributions.iter().enumerate() {
                if contribution > 0.0 {
                    orbital_ids.push(orbital_id as i32);
                    energies.push(current_energies[orbital_id]);
                    occupancies.push(current_occupancies[orbital_id]);
                    atom_indices.push(atom_index);
                    elements.push(element.clone());
                    orbital_types.push(orbital_type.clone());
                    weights.push(contribution);
                }
            }
        }
    }

    // Create DataFrame
    let df = DataFrame::new(vec![
        Column::new("orbital_id".into(), orbital_ids),
        Column::new("energy".into(), energies),
        Column::new("occupancy".into(), occupancies),
        Column::new("atom_index".into(), atom_indices),
        Column::new("element".into(), elements),
        Column::new("orbital_type".into(), orbital_types),
        Column::new("weight".into(), weights),
    ])?
    .sort(["orbital_id"], SortMultipleOptions::new())?;

    Ok(df)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let input = "
        ----------------------------
        LOEWDIN ORBITAL-COMPOSITIONS
        ----------------------------

                              0         1         2         3         4         5
                         -261.73681 -32.31296 -27.80151 -27.80141 -27.79974 -20.64726
                           2.00000   2.00000   2.00000   2.00000   2.00000   2.00000
                          --------  --------  --------  --------  --------  --------
         0 Fe s             100.0     100.0       0.0       0.0       0.0       0.0
         0 Fe pz              0.0       0.0       1.1       0.6      98.3       0.0
         0 Fe px              0.0       0.0       0.9      98.7       0.4       0.0
         0 Fe py              0.0       0.0      98.0       0.7       1.3       0.0
         4 O  s               0.0       0.0       0.0       0.0       0.0      99.9

                              6         7         8         9        10        11
                         -20.61622 -15.88874 -15.74442 -15.74253 -15.74097 -15.73729
                           2.00000   2.00000   2.00000   2.00000   2.00000   2.00000
                          --------  --------  --------  --------  --------  --------
         2 N  s               0.0      99.6       0.0       0.0       0.0       0.0
         2 N  pz              0.0       0.0       0.1       0.0       0.0       0.0
         3 N  s               0.0       0.0      99.8       0.0       0.0       0.0
         3 N  pz              0.0       0.1       0.0       0.0       0.0       0.0
         5 N  s               0.0       0.0       0.0       0.0      99.8       0.0
         7 N  s               0.0       0.0       0.0      99.8       0.0       0.0
         8 N  s               0.0       0.0       0.0       0.0       0.0      99.7
        44 O  s              99.9       0.0       0.0       0.0       0.0       0.0


        ";
        assert!(parse_loewdin_orbital_compositions(input).is_ok());
        assert_eq!(
            parse_loewdin_orbital_compositions(input).unwrap().shape().0,
            20
        );
    }

    #[test]
    fn it_works_two() {
        let input = "
            ----------------------------
            LOEWDIN REDUCED ACTIVE MOs
            ----------------------------

                                102       103       104       105       106       107
                              -0.49264  -0.39792  -0.45792  -0.45626  -0.45507  -0.44057
                               2.00000   1.00000   1.00000   1.00000   1.00000   1.00000
                              --------  --------  --------  --------  --------  --------
             0 Fe dz2             0.0      85.6       0.0       0.0       0.0       0.0
             0 Fe dxz             0.0       0.0      95.5       0.0       0.0       0.0
             0 Fe dyz             2.7       0.0       0.0      95.3       0.0       0.0
             0 Fe dx2y2           0.0       0.0       0.0       0.0      94.5       0.3
             0 Fe dxy             0.0       0.0       0.0       0.0       0.5      91.5
             1 N  py             49.2       0.0       0.0       1.8       0.0       0.0
             3 N  py             33.5       0.0       0.0       1.0       0.0       0.0

            ------------------------------------------------------------------------------
                                       ORCA POPULATION ANALYSIS
            ";
        assert!(parse_loewdin_reduced_active_mos(input).is_ok());
        assert_eq!(
            parse_loewdin_reduced_active_mos(input).unwrap().shape().0,
            12
        );
    }
}
