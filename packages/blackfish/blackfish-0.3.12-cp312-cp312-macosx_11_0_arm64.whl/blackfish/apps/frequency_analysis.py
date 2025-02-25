import marimo

__generated_with = "0.11.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    from pathlib import Path

    import marimo as mo
    import polars as pl
    import altair as alt

    import blackfish as bf
    return Path, alt, bf, mo, pl


@app.cell(hide_code=True)
def _(mo):
    file_button = mo.ui.file(
        label="Open ORCA frequency calculation file", filetypes=[".out"]
    )
    file_button
    return (file_button,)


@app.cell(hide_code=True)
def _(bf):
    from tempfile import NamedTemporaryFile


    def create_orca_parser(file_button) -> bf.OrcaParser:
        with NamedTemporaryFile() as tmp:
            tmp.write(file_button.value[0].contents)
            tmp.seek(0)
            return bf.OrcaParser.from_file(tmp.name)
    return NamedTemporaryFile, create_orca_parser


@app.cell(hide_code=True)
def _(alt, pl):
    def chart_ir_spectrum(df: pl.DataFrame) -> alt.Chart:
        chart = (
            alt.Chart(df)
            .mark_bar(size=3, cursor="pointer")
            .encode(
                x=alt.X(
                    "frequency_cm",
                    title="Frequency (1/cm)",
                    scale=alt.Scale(domain=[0, 3500]),
                ),
                y=alt.Y(
                    "intensity",
                    title="Intensity",
                    scale=alt.Scale(domain=[0, 4000]),
                ),
                tooltip=[
                    alt.Tooltip(title="Vib. Mode", field="mode"),
                    alt.Tooltip(
                        title="Frequency", field="frequency_cm", format="d"
                    ),
                ],
            )
        )

        return chart
    return (chart_ir_spectrum,)


@app.cell(hide_code=True)
def _(chart_ir_spectrum, create_orca_parser, file_button, mo):
    mo.stop(not file_button.value)

    parser = create_orca_parser(file_button)
    df = parser.get_ir_spectrum()
    _chart = chart_ir_spectrum(df)

    chart = mo.ui.altair_chart(_chart, chart_selection="point")
    return chart, df, parser


@app.cell
def _(chart):
    chart
    return


@app.cell
def _(chart):
    chart.value
    return


if __name__ == "__main__":
    app.run()
