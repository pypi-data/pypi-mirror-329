use std::error::Error;

use regex::Regex;

/// Parse the active space orbital range
///
/// # Arguments
///
/// * `input` - A string containing the ORCA output.
///
/// # Returns
///
/// A list of the active space orbital IDs
pub fn parse_active_space_range(input: &str) -> Result<Vec<u32>, Box<dyn Error>> {
    // Match a line like: "Active        87 -   91 (   5 orbitals)"
    let re = Regex::new(r"Active\s+(?<start>\d+)\s*-\s*(?<stop>\d+)\s*\(\s*\d+\s*orbitals\)")?;
    if let Some(caps) = re.captures(input) {
        let start: u32 = caps["start"].parse()?;
        let stop: u32 = caps["stop"].parse()?;
        Ok((start..=stop).collect())
    } else {
        Err("No match found".into())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let input = "
        Determined orbital ranges:
           Internal       0 -  102 ( 103 orbitals)
           Active       103 -  107 (   5 orbitals)
           External     108 -  521 ( 414 orbitals)
        ";
        let expectation: Vec<u32> = (103..=107).collect();
        assert!(parse_active_space_range(input).is_ok());
        assert_eq!(parse_active_space_range(input).unwrap(), expectation);
    }
}
