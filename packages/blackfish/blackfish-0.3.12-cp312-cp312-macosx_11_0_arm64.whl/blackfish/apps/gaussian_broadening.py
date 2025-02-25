import numpy as np
import polars as pl
from scipy.signal import convolve


# Step 1: Define the broadening function (Gaussian in this case)
def gaussian(x, fwhm):
    """Gaussian function used for spectral broadening.

    Args:
        x: The wavelength or frequency values relative to the center.
        fwhm: The full width at half maximum (FWHM) of the Gaussian.

    Returns:
        Array of Gaussian function values.
    """
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))  # Convert FWHM to standard deviation

    if sigma == 0:
        return np.zeros_like(x)

    return np.exp(-(x**2) / (2 * sigma**2))


def apply_gaussian_filter(df, energy_col, intensity_col, fwhm, interpolation_factor=5):
    """Apply spectral broadening to a Polars DataFrame with spectral data.

    Args:
        df: The input Polars DataFrame containing spectral data.
        energy_col: The column name containing energy or frequency values.
        intensity_col: The column name containing intensity values.
        fwhm: Full width at half maximum (FWHM) for the broadening.
        interpolation_factor: Factor by which to increase the number of data points for smoothing.

    Returns:
        A new Polars DataFrame with the broadened and smoothed spectrum.
    """
    # Extract data from the Polars DataFrame
    energies = df[energy_col].to_numpy()
    intensities = df[intensity_col].to_numpy()

    # Step 1: Interpolate the data to add more points (smoothing)
    new_energies = np.linspace(
        energies.min(), energies.max(), len(energies) * interpolation_factor
    )

    # Step 2: Create an array of zeros for the new intensities (zero padding)
    new_intensities = np.zeros_like(new_energies)

    # Step 3: Map original intensities to the nearest points on the new energy grid
    interpolated_indices = np.searchsorted(new_energies, energies)
    for i, idx in enumerate(interpolated_indices):
        if idx < len(new_energies):
            new_intensities[idx] = intensities[
                i
            ]  # Map original intensities to new grid

    # Step 4: Create a energy grid relative to the center of the spectrum
    delta_energies = new_energies - np.mean(new_energies)

    # Step 5: Create the Gaussian kernel for broadening
    gaussian_kernel = gaussian(delta_energies, fwhm)

    # Step 6: Convolve the interpolated intensity with the Gaussian broadening kernel
    broadened_intensities = convolve(new_intensities, gaussian_kernel, mode="same")

    # Step 7: Normalize the result to maintain the total intensity
    # broadened_intensities /= np.max(broadened_intensities)

    # Step 8: Create a new Polars DataFrame with broadened spectrum
    broadened_df = pl.DataFrame(
        {energy_col: new_energies, intensity_col: broadened_intensities}
    )

    return broadened_df
