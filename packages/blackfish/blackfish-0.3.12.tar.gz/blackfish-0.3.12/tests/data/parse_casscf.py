import marimo

__generated_with = "0.11.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from pathlib import Path
    return Path, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ```
        ---------------------------------------------
        CAS-SCF STATES FOR BLOCK  2 MULT= 2 NROOTS=40
        ---------------------------------------------

        ROOT   0:  E=   -4568.3569534307 Eh
              0.21319 [    25]: 22102
              0.20259 [     9]: 12112
              0.10954 [    11]: 12202
              0.07648 [     7]: 11221
              0.07030 [    12]: 12211
              0.05178 [    18]: 21112
              0.04644 [    10]: 12121
              0.04150 [    27]: 22120
              0.02622 [    19]: 21121
              0.02462 [    20]: 21202
              0.02427 [    26]: 22111
              0.02060 [     2]: 02212
              0.01271 [     6]: 11212
              0.01266 [    24]: 22021
              0.01197 [     5]: 11122
              0.00794 [    22]: 21220
              0.00771 [    28]: 22201
              0.00706 [     8]: 12022
              0.00594 [     0]: 01222
              0.00447 [     4]: 10222
              0.00421 [    14]: 20122
              0.00372 [    29]: 22210
              0.00349 [    13]: 12220
              0.00286 [    21]: 21211
        ROOT   1:  E=   -4568.3555163763 Eh  0.039 eV    315.4 cm**-1
              0.24971 [    26]: 22111
              0.12512 [    10]: 12121
              0.11652 [     9]: 12112
              0.11017 [     6]: 11212
              0.09782 [    12]: 12211
              0.07653 [    21]: 21211
              0.04441 [    18]: 21112
              0.02858 [    27]: 22120
              0.02629 [    19]: 21121
        ```
        """
    )
    return


@app.cell
def _(Path):
    file = (
        Path(
            "/Users/freddy/Documents/Projects/aom-ailft/test/Co-Br-Cl-F-NH3/CASSCF/CASSCF.out"
        )
        .read_text()
        .splitlines()
    )
    return (file,)


@app.cell
def _():
    import blackfish as bf
    return (bf,)


@app.cell
def _(bf, file):
    bf.OrcaParser(file).get_casscf_roots()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
