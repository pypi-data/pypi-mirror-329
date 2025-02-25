import altair as alt
import polars as pl


def ir_spectrum_chart(df: pl.DataFrame) -> alt.Chart:
    chart = (
        alt.Chart(df)
        .mark_bar(opacity=0.5)
        .encode(
            x=alt.X("energy_cm:Q", title="Energy [1/cm]"),
            y=alt.Y("rel_intensity:Q", title="Rel. Intensity"),
            color=alt.value("blue"),
            tooltip=["Frequency [1/cm]", "Rel. Intensity"],
        )
    )

    return chart
