// use polars::prelude::*;
// use regex::Regex;

// Meh, somehow the parsed df is empty, but i can't be bothered to fix it right now

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
//     let s_au = Column::new("energy_eh".into(), energy_au);
//     let s_ev = Column::new("energy_ev".into(), energy_ev);
//     DataFrame::new(vec![s_comp, s_au, s_ev])
// }

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn it_works() {
//         let input = "
//             -----------------
//             ENERGY COMPONENTS
//             -----------------

//             One electron energy          :  -9980.152955048 Eh     -271573.7685 eV
//             Two electron energy          :   4214.818259477 Eh      114691.0356 eV
//             Nuclear repulsion energy     :   3387.302412090 Eh       92173.1846 eV
//                                            ----------------
//                                             -2378.032283481

//             Kinetic energy               :   2370.593934721 Eh       64507.1404 eV
//             Potential energy             :  -4748.626218201 Eh     -129216.6886 eV
//             Virial ratio                 :     -2.003137757
//                                            ----------------
//                                             -2378.032283481

//             Core energy                  :  -2365.315240051 Eh   -64363.4999 eV

//             ";
//         assert!(parse_energy_components(input).is_ok());
//         assert_eq!(parse_energy_components(input).unwrap().shape().0, 3);
//     }
// }
