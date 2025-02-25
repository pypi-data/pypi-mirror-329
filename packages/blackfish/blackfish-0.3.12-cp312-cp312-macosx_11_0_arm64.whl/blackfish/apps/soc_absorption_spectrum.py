import altair as alt
import polars as pl
from scipy.signal import find_peaks

from blackfish.apps.gaussian_broadening import apply_gaussian_filter


def soc_absorption_spectrum_chart(
    df: pl.DataFrame,
    fwhm: int = 2000,
    peaks: bool = True,
    peak_threshold: float = 0.3,
    color: str = "black",
) -> alt.LayerChart:
    bar = (
        alt.Chart(df)
        .mark_bar(opacity=0.7, size=4)
        .encode(
            x=alt.X("energy_cm:Q", title="Energy [1/cm]"),
            y=alt.Y("rel_intensity:Q", title="Rel. Intensity"),
            tooltip=["energy_cm", "rel_intensity"],
        )
        .properties(width=800, height=400)
    )

    simulated_df = apply_gaussian_filter(df, "energy_cm", "rel_intensity", fwhm, 10)

    simulated_layer = (
        alt.Chart(simulated_df)
        .mark_line()
        .encode(x="energy_cm:Q", y="rel_intensity:Q", color=alt.value(color))
    )
    chart = bar + simulated_layer

    if peaks:
        # Convert to numpy arrays for peak finding
        y = simulated_df["rel_intensity"].to_numpy()
        x = simulated_df["energy_cm"].to_numpy()

        # Find peaks with height threshold
        peak_indices, _ = find_peaks(y, prominence=peak_threshold)

        # Create DataFrame with peak data
        peak_data = pl.DataFrame(
            {"energy_cm": x[peak_indices], "rel_intensity": y[peak_indices]}
        )

        # Create peak markers
        peak_layer = (
            alt.Chart(peak_data)
            .mark_point(color="red", filled=True)
            .encode(
                x="energy_cm:Q",
                y="rel_intensity:Q",
                tooltip=["energy_cm", "rel_intensity"],
            )
        )
        chart += peak_layer

    return chart
