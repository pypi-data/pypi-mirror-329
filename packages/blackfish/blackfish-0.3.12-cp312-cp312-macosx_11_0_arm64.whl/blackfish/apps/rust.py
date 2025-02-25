# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "blackfish==0.3.8",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.11.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import blackfish as bf
    return (bf,)


@app.cell
def _(bf):
    # vars(bf)
    from pathlib import Path

    a = bf.parse_orca_output_py(Path("/Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out").read_text())
    return Path, a


@app.cell
def _(a):
    a   
    return


@app.cell
def _(a):
    a["casscf_states"].split("\n")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
