# Blackfish 🐋

## Installation

```bash
pip install blackfish
```

## Quick Start

```python
from blackfish import OrcaParser

# Load the ORCA output file
parser = OrcaParser("my_calculation.out")

# Data can then be parsed as polars DataFrames
ir_spectrum = parser.get_ir_spectrum()
nacme = parser.get_nacme()
tddft_roots = parser.get_tddft_roots()
tddft_soc_spectrum = parser.get_tddft_soc_spectrum()
soc_states = parser.get_soc_states()
socme = parser.get_socme()

# Energy values are stored in an Energies object.
# If a value can't be parsed, it returns None
energies = parser.get_energies()
energies.fspe                 # Hartree
energies.fspe(unit="kj/mol")  # kJ/mol
energies.gibbs_free_energy
energies.gibbs_minus_electronic_energy
energies.entropy
energies.enthalpy
energies.zero_point_energy

# or simply convert energies
energy_in_kjmol = OrcaParser.convert_energy(energy_in_kcalmol, from_unit="kcal/mol", to_unit="kj/mol")

# Available energy units
# - hartree
# - ev
# - 1/cm
# - kj/mol
# - kcal/mol
```

## Examples

### IR Spectrum Analysis

```python
# Get IR spectrum data
ir_spectrum = orca.get_ir_spectrum()

# View strongest vibrational modes
strongest_modes = ir_spectrum.filter(pl.col("rel_intensity") > 0.5)
print(strongest_modes)

# Get frequencies above 3000 1/cm
high_freq = ir_spectrum.filter(pl.col("frequency_cm") > 3000)
print(high_freq)
```

### Electronic State Analysis

```python
# Get excited state data
tddft_roots = orca.get_tddft_roots()

# Group transitions by multiplicity
by_mult = tddft_roots.group_by("mult").agg([
    pl.count(),
    pl.mean("energy_cm").alias("avg_energy")
])
```

### SOC States Analysis

```python
# Get SOC states
soc_states = orca.get_soc_states()

# Get contributions to specific SOC state
state1 = soc_states.filter(pl.col("state") == 1)

# Find states with large spin mixing
mixed_states = soc_states.filter(pl.col("weight") > 0.2)

# Summarize spin components per state
spin_summary = soc_states.group_by("state").agg([
    pl.n_unique("spin").alias("n_spin_components"),
    pl.max("weight").alias("max_contribution")
])
```

### NACME Analysis

```python
# Get non-adiabatic coupling elements
nacme = orca.get_nacme()

# Find atoms with strong coupling
strong_coupling = nacme.filter(pl.col("magnitude") > 0.1)

# Get coupling vectors for specific atoms
h_atoms = nacme.filter(pl.col("symbol") == "H")

# Sort atoms by coupling magnitude
sorted_coupling = nacme.sort("magnitude", descending=True)
```

### TDDFT SOC Spectrum Analysis

```python
# Get absorption spectrum
tddft_soc_spectrum = orca.get_tddft_soc_spectrum()

# Find intense transitions
intense = tddft_soc_spectrum.filter(pl.col("rel_intensity") > 0.5)

# Get visible region transitions
visible = tddft_soc_spectrum.filter(
    (pl.col("wavelength_nm") >= 380) &
    (pl.col("wavelength_nm") <= 700)
)

# Summarize by spin multiplicity
by_mult = tddft_soc_spectrum.group_by("mult").agg([
    pl.count(),
    pl.mean("energy_ev").alias("avg_energy"),
    pl.max("osc_strength").alias("max_intensity")
])
```

## Data Structure

Blackfish uses [Polars](https://pola.rs/) DataFrames for efficient data handling. Common DataFrame schemas include:

### IR Spectrum
- `mode`: Vibrational mode number
- `frequency_cm`: Frequency in cm⁻¹
- `intensity`: IR intensity
- `rel_intensity`: Normalized intensity
- `tx/ty/tz`: Transition dipole components

### Excited States (Roots)
- `root`: State number
- `mult`: Spin multiplicity
- `donor`: Donor orbital
- `acceptor`: Acceptor orbital
- `weight`: Configuration weight
- `energy_cm`: Energy in cm⁻¹

### SOC States
- `state`: SOC state number
- `spin`: Spin component
- `root`: Contributing root state
- `weight`: State contribution weight
- `energy_cm`: Energy in cm⁻¹

### NACME
- `id`: Atom index
- `symbol`: Atomic symbol
- `x/y/z`: Coupling vector components
- `magnitude`: Total coupling magnitude

### SOC Absorption Spectrum
- `state`: Final state number
- `mult`: State multiplicity
- `energy_ev`: Transition energy in eV
- `energy_cm`: Energy in cm⁻¹
- `wavelength_nm`: Wavelength in nm
- `osc_strength`: Oscillator strength
- `rel_intensity`: Normalized intensity

## License

This project is licensed under the Apache2.0 License - see the LICENSE file for details.
