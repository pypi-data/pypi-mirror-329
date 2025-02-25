# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.11.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import blackfish
    return blackfish, mo


@app.cell
def _(mo):
    from pathlib import Path

    file_radio = mo.ui.radio(
        options={
            str(p): p
            for p in Path(
                "/Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations"
            ).rglob("02_ailft.out")
        },
    )
    file_radio
    return Path, file_radio


@app.cell
def _(blackfish, file_radio, mo):
    mo.stop(not file_radio.value)

    df = blackfish.parse_ailft_one_electron_eigenfunctions(
        file_radio.value.read_text()
    )
    return (df,)


@app.cell
def _(mo):
    mo.md(
        r"""
        I want to look at the orbitals.

        Do plot the AILFT orbitals, I need to implement a new mode in `orcaplot`.

        Its like `active-space`, but with the `.lft.gbw` file.

        Maybe I can just add a flag to `active-space`.
        """
    )
    return


@app.cell
def _(df):
    type(df)
    return


@app.cell
def _(mo):
    mo.md(r"""Huh, funny that it's a `polars` dataframe, even though I didn't import the package.""")
    return


@app.cell
def _(df):
    print(df)
    return


@app.cell
def _(pl):
    import altair as alt


    def plot_mo_schema(df: pl.DataFrame):
        chart = (
            alt.Chart(df)
            .mark_point(shape="stroke", strokeWidth=4, size=2500)
            .encode(
                y=alt.Y("energy_cm", scale=alt.Scale(domain=[0, 25_000])),
                tooltip=["orbital", "dz2", "dxz", "dyz", "dx2y2", "dxy"],
            )
            .properties(width=240)
        )
        return chart
    return alt, plot_mo_schema


@app.cell
def _(df, plot_mo_schema):
    plot_mo_schema(df)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Without `ds` mixing
        -------------------

        ```bash
        freddy@fscherz aomadillo % uv run aomadillo_solve.py --nods -g "[1,1,2,2,2,2]" --fixmap "[x,x,x,x,x,x,0,x,0,x,0,x,0]" "[1,4,7,8,9,10]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam/new/m2/casscf/02_ailft/02_ailft.out
        #File                                                                                                                        Cost        E   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam/new/m2/casscf/02_ailft/02_ailft.out   2649289  -904097     7753     1447     7753     1447     6308        0     6292        0     6308        0     6291        0


        freddy@fscherz aomadillo % uv run aomadillo_solve.py --nods -g "[1,2,3,3,3,3]" --fixmap "[x,x,x,x,x,x,0,x,0,x,0,x,0]" "[1,4,5,6,7,8]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/casscf/02_ailft/02_ailft.out
        #File                                                                                                                           Cost        E   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/casscf/02_ailft/02_ailft.out   1422531  -910605     4956      773    10754     2142     5817        0     6310        0     6189        0     6389        0


        freddy@fscherz aomadillo % uv run aomadillo_solve.py --nods -g "[1,2,3,3,3,3]" --fixmap "[x,x,x,x,x,x,0,x,0,x,0,x,0]" "[1,4,5,6,7,8]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out
        #File                                                                                                                              Cost        E   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out    363316  -927380     8403     1813     4759     1769     4164        0     3754        0     3935        0     3690        0
        ```



        With `ds` mixing
        ----------------

        ```bash
        freddy@fscherz aomadillo % uv run aomadillo_solve.py -g "[1,1,2,2,2,2]" --fixmap "[x,x,x,x,x,x,x,x,0,x,x,0,x,x,0,x,x,0,x]" "[1,4,7,8,9,10]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam/new/m2/casscf/02_ailft/02_ailft.out
        #File                                                                                                                        Cost        E   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam/new/m2/casscf/02_ailft/02_ailft.out   1431874  -903342     8038     1257     7713     8038     1257     7713     5901        0     5592     6164        0     4617     5901        0     5592     6164        0     4616
        freddy@fscherz aomadillo % uv run aomadillo_solve.py -g "[1,2,3,3,3,3]" --fixmap "[x,x,x,x,x,x,x,x,0,x,x,0,x,x,0,x,x,0,x]" "[1,4,5,6,7,8]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/casscf/02_ailft/02_ailft.out
        #File                                                                                                                           Cost        E   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/casscf/02_ailft/02_ailft.out    865295  -910319     4602     2861    10000    11303      108        0     6046        0     4320     6106        0     3195     6249        0     4058     6164        0     3215
        freddy@fscherz aomadillo % uv run aomadillo_solve.py -g "[1,2,3,3,3,3]" --fixmap "[x,x,x,x,x,x,x,x,0,x,x,0,x,x,0,x,x,0,x]" "[1,4,5,6,7,8]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out
        #File                                                                                                                              Cost        E   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out    245682  -927204    10143     1288        0     3350     2325     8738     4113        0     3479     3658        0     3406     3934        0     3457     3623        0     3248
        ```

        With `ds` mixing and free `e_pi`
        --------------------------------

        ```bash
        freddy@fscherz aomadillo % uv run aomadillo_solve.py -g "[1,1,2,2,2,2]" "[1,4,7,8,9,10]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam/new/m2/casscf/02_ailft/02_ailft.out
        #File                                                                                                                        Cost        E   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam/new/m2/casscf/02_ailft/02_ailft.out    759218  -892179     6907    -1520     5029     6907    -1520     5029     2000    -2969     1158     2687    -2887      806     2000    -2969     1158     2687    -2887      805
        freddy@fscherz aomadillo % uv run aomadillo_solve.py -g "[1,2,3,3,3,3]" "[1,4,5,6,7,8]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/casscf/02_ailft/02_ailft.out
        #File                                                                                                                           Cost        E   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/casscf/02_ailft/02_ailft.out    476835  -901156     9568     3714    10000     -216    -5324        0     2936    -2542     2759     3335    -2006     1667     2994    -2680     2756     3390    -2094     1692
        freddy@fscherz aomadillo % uv run aomadillo_solve.py -g "[1,2,3,3,3,3]" "[1,4,5,6,7,8]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out
        #File                                                                                                                              Cost        E   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds   esigma      epi      eds
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out    215686  -921848     4513    -1336    10000     5019     2055     2359     2288    -1402     6200     1933     -998     5889     2155    -1298     6201     1773    -1524     5835
        ```

        Without `ds` mixing and free `e_pi`
        -----------------------------------

        ```bash
        freddy@fscherz aomadillo % uv run aomadillo_solve.py --nods -g "[1,1,2,2,2,2]" "[1,4,7,8,9,10]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam/new/m2/casscf/02_ailft/02_ailft.out
        #File                                                                                                                        Cost        E   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam/new/m2/casscf/02_ailft/02_ailft.out   1597299  -891857     3646    -1593     3646    -1593     2291    -3193     2256    -2988     2291    -3193     2256    -2988
        freddy@fscherz aomadillo % uv run aomadillo_solve.py --nods -g "[1,2,3,3,3,3]" "[1,4,5,6,7,8]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/casscf/02_ailft/02_ailft.out
        #File                                                                                                                           Cost        E   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/casscf/02_ailft/02_ailft.out    747807  -901746     6375     1378     3428    -2850     2928    -2360     3399    -1832     3208    -2814     3469    -1947
        freddy@fscherz aomadillo % uv run aomadillo_solve.py --nods -g "[1,2,3,3,3,3]" "[1,4,5,6,7,8]" /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out
        #File                                                                                                                              Cost        E   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi   esigma      epi
        /Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_me-cyclam-ac/new/m6/casscf/02_ailft/02_ailft.out    241019  -920709     3856    -1400     4913     1686     1915    -1803     1557    -1277     1740    -1660     1420    -1987
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(Path, pl):
    # Dump of plotly molecular visualization code

    import numpy as np
    import plotly.graph_objects as go

    ELEMENTS = {
        "H": {"covalent_radius": 0.31, "color": "white", "size": 5},
        "He": {"covalent_radius": 0.28, "color": "cyan", "size": 5},
        "Li": {"covalent_radius": 1.28, "color": "purple", "size": 8},
        "Be": {"covalent_radius": 0.96, "color": "darkgreen", "size": 8},
        "B": {"covalent_radius": 0.84, "color": "pink", "size": 8},
        "C": {"covalent_radius": 0.76, "color": "rgb(48,48,48)", "size": 10},
        "N": {"covalent_radius": 0.71, "color": "#002FA7", "size": 10},
        "O": {"covalent_radius": 0.66, "color": "red", "size": 10},
        "F": {"covalent_radius": 0.57, "color": "lightgreen", "size": 8},
        "Ne": {"covalent_radius": 0.58, "color": "cyan", "size": 5},
        "Na": {"covalent_radius": 1.66, "color": "blue", "size": 8},
        "Mg": {"covalent_radius": 1.41, "color": "lightgreen", "size": 10},
        "Al": {"covalent_radius": 1.21, "color": "gray", "size": 10},
        "Si": {"covalent_radius": 1.11, "color": "lightgray", "size": 10},
        "P": {"covalent_radius": 1.07, "color": "orange", "size": 12},
        "S": {"covalent_radius": 1.05, "color": "yellow", "size": 10},
        "Cl": {"covalent_radius": 1.02, "color": "green", "size": 10},
        "Ar": {"covalent_radius": 1.06, "color": "cyan", "size": 5},
        "K": {"covalent_radius": 2.03, "color": "violet", "size": 12},
        "Ca": {"covalent_radius": 1.76, "color": "lightblue", "size": 12},
        "Sc": {"covalent_radius": 1.70, "color": "gray", "size": 12},
        "Ti": {"covalent_radius": 1.60, "color": "gray", "size": 12},
        "V": {"covalent_radius": 1.53, "color": "gray", "size": 12},
        "Cr": {"covalent_radius": 1.39, "color": "gray", "size": 12},
        "Mn": {"covalent_radius": 1.39, "color": "gray", "size": 12},
        "Fe": {"covalent_radius": 1.32, "color": "darkorange", "size": 12},
        "Co": {"covalent_radius": 1.26, "color": "crimson", "size": 15},
        "Ni": {"covalent_radius": 1.24, "color": "bluegray", "size": 12},
        "Cu": {"covalent_radius": 1.32, "color": "brown", "size": 12},
        "Zn": {"covalent_radius": 1.22, "color": "lightblue", "size": 12},
        "Ga": {"covalent_radius": 1.22, "color": "lightblue", "size": 12},
        "Ge": {"covalent_radius": 1.20, "color": "lightgray", "size": 12},
        "As": {"covalent_radius": 1.19, "color": "bluegray", "size": 12},
        "Se": {"covalent_radius": 1.20, "color": "yellow", "size": 12},
        "Br": {"covalent_radius": 1.20, "color": "darkred", "size": 12},
        "Kr": {"covalent_radius": 1.16, "color": "cyan", "size": 5},
        "Rb": {"covalent_radius": 2.20, "color": "violet", "size": 14},
        "Sr": {"covalent_radius": 1.95, "color": "lightblue", "size": 14},
        "Y": {"covalent_radius": 1.90, "color": "gray", "size": 14},
        "Zr": {"covalent_radius": 1.75, "color": "gray", "size": 14},
        "Nb": {"covalent_radius": 1.64, "color": "gray", "size": 14},
        "Mo": {"covalent_radius": 1.54, "color": "gray", "size": 14},
        "Tc": {"covalent_radius": 1.47, "color": "gray", "size": 14},
        "Ru": {"covalent_radius": 1.46, "color": "gray", "size": 14},
        "Rh": {"covalent_radius": 1.42, "color": "gray", "size": 14},
        "Pd": {"covalent_radius": 1.39, "color": "seagreen", "size": 14},
        "Pt": {"covalent_radius": 1.36, "color": "white", "size": 14},
        "Ag": {"covalent_radius": 1.45, "color": "gray", "size": 14},
        "Cd": {"covalent_radius": 1.44, "color": "lightblue", "size": 14},
        "In": {"covalent_radius": 1.42, "color": "gray", "size": 14},
        "Sn": {"covalent_radius": 1.39, "color": "lightgray", "size": 14},
        "Sb": {"covalent_radius": 1.39, "color": "bluegray", "size": 14},
        "Te": {"covalent_radius": 1.38, "color": "yellow", "size": 14},
        "I": {"covalent_radius": 1.39, "color": "purple", "size": 14},
        "Xe": {"covalent_radius": 1.40, "color": "cyan", "size": 5},
        "Cs": {"covalent_radius": 2.44, "color": "violet", "size": 16},
        "Ba": {"covalent_radius": 2.15, "color": "lightblue", "size": 16},
        "La": {"covalent_radius": 2.07, "color": "gray", "size": 16},
        "Ce": {"covalent_radius": 2.04, "color": "gray", "size": 16},
        "Pr": {"covalent_radius": 2.03, "color": "gray", "size": 16},
        "Nd": {"covalent_radius": 2.01, "color": "gray", "size": 16},
        "Pm": {"covalent_radius": 1.99, "color": "gray", "size": 16},
        "Sm": {"covalent_radius": 1.98, "color": "gray", "size": 16},
        "Eu": {"covalent_radius": 1.98, "color": "gray", "size": 16},
        "Gd": {"covalent_radius": 1.96, "color": "gray", "size": 16},
        "Tb": {"covalent_radius": 1.94, "color": "gray", "size": 16},
        "Dy": {"covalent_radius": 1.92, "color": "gray", "size": 16},
        "Ho": {"covalent_radius": 1.92, "color": "gray", "size": 16},
        "Er": {"covalent_radius": 1.89, "color": "gray", "size": 16},
        "Tm": {"covalent_radius": 1.90, "color": "gray", "size": 16},
        "Yb": {"covalent_radius": 1.87, "color": "gray", "size": 16},
        "Lu": {"covalent_radius": 1.87, "color": "gray", "size": 16},
    }


    class MoleculeVisualizer:
        """
        Visualizes a molecular structure from an XYZ file.

        It uses an XYZ file input to build a DataFrame of atomic coordinates,
        detects bonds based on covalent radii from a provided elements dictionary,
        and plots atoms as spheres and bonds as cylinders.
        """

        def __init__(self, df: pl.DataFrame, width=640, height=640, title=None):
            """
            Args:
                df: Polars DataFrame with columns ["Symbol", "X", "Y", "Z"].
                width: Plot width (pixels).
                height: Plot height (pixels).
                title: Plot title.
            """
            self.df = df
            self.elements = ELEMENTS
            self.width = width
            self.height = height
            self.title = title

        @staticmethod
        def parse_xyz_string(string: str) -> pl.DataFrame:
            """
            Parse an XYZ-formatted string into a Polars DataFrame.
            The first line is the number of atoms, the second is a comment, and then
            each subsequent line has: Symbol X Y Z.
            """
            lines = string.splitlines()
            num_atoms = int(lines[0].strip())
            atoms = []
            for line in lines[2 : 2 + num_atoms]:
                parts = line.split()
                symbol = parts[0]
                x, y, z = map(float, parts[1:4])
                atoms.append({"Symbol": symbol, "X": x, "Y": y, "Z": z})
            return pl.DataFrame(atoms)

        @classmethod
        def from_xyz_string(cls, string: str, width=640, height=320, title=None):
            """
            Create a StructureVisualizer instance directly from an XYZ-formatted string.

            Args:
                string: XYZ-formatted string.
                width: Plot width.
                height: Plot height.
                title: Plot title.
            """
            df = cls.parse_xyz_string(string)
            return cls(df, width, height, title)

        @classmethod
        def from_xyz_file(cls, file: Path, width=640, height=640, title=None):
            """
            Create a StructureVisualizer instance directly from an XYZ file.

            Args:
                file: Path to the XYZ file.
                width: Plot width.
                height: Plot height.
                title: Plot title.
            """
            text = file.read_text()
            df = cls.parse_xyz_string(text)
            return cls(df, width, height, title)

        def detect_bonds(self, tolerance=1.2) -> list[tuple]:
            """
            Detect bonds based on covalent radii (using a tolerance factor).
            Returns a list of tuples of atom indices that are bonded.
            """
            bonds = []
            num_atoms = len(self.df)
            symbols = self.df["Symbol"].to_list()
            xs = self.df["X"].to_list()
            ys = self.df["Y"].to_list()
            zs = self.df["Z"].to_list()

            for i in range(num_atoms):
                elem1 = symbols[i]
                if elem1 not in self.elements:
                    continue
                radius1 = self.elements[elem1]["covalent_radius"]
                x1, y1, z1 = xs[i], ys[i], zs[i]
                for j in range(i + 1, num_atoms):
                    elem2 = symbols[j]
                    if elem2 not in self.elements:
                        continue
                    radius2 = self.elements[elem2]["covalent_radius"]
                    cutoff = (radius1 + radius2) * tolerance

                    dx = x1 - xs[j]
                    dy = y1 - ys[j]
                    dz = z1 - zs[j]
                    distance = np.sqrt(dx * dx + dy * dy + dz * dz)

                    if distance <= cutoff:
                        bonds.append((i, j))
            return bonds

        def create_sphere(self, center, radius=1.0, n_steps=12):
            """
            Create mesh data for a sphere centered at `center`.
            Returns (x, y, z, i, j, k) for a Plotly Mesh3d trace.
            """
            cx, cy, cz = center
            theta_vals = np.linspace(0, np.pi, n_steps + 1)
            phi_vals = np.linspace(0, 2 * np.pi, n_steps, endpoint=False)
            theta_grid, phi_grid = np.meshgrid(theta_vals, phi_vals, indexing="ij")

            x_2d = cx + radius * np.sin(theta_grid) * np.cos(phi_grid)
            y_2d = cy + radius * np.sin(theta_grid) * np.sin(phi_grid)
            z_2d = cz + radius * np.cos(theta_grid)

            x_all = x_2d.ravel()
            y_all = y_2d.ravel()
            z_all = z_2d.ravel()

            i_list, j_list, k_list = [], [], []

            def idx(t, p):
                return t * n_steps + (p % n_steps)

            for t in range(n_steps):
                for p in range(n_steps):
                    i0 = idx(t, p)
                    i1 = idx(t, p + 1)
                    i2 = idx(t + 1, p)
                    i3 = idx(t + 1, p + 1)
                    # First triangle
                    i_list.append(i0)
                    j_list.append(i1)
                    k_list.append(i2)
                    # Second triangle
                    i_list.append(i1)
                    j_list.append(i3)
                    k_list.append(i2)

            return x_all, y_all, z_all, i_list, j_list, k_list

        def create_cylinder(
            self, start_point, end_point, radius=0.05, n_segments=48, add_caps=True
        ):
            """
            Create mesh data for a cylinder from start_point to end_point.
            Returns (x, y, z, i, j, k) for a Plotly Mesh3d trace.
            """
            p0 = np.array(start_point, dtype=float)
            p1 = np.array(end_point, dtype=float)
            d = p1 - p0
            length = np.linalg.norm(d)
            if length < 1e-12:
                # Degenerate case: return a point.
                return [p0[0]], [p0[1]], [p0[2]], [], [], []

            d /= length
            if abs(d[0]) < 1e-4 and abs(d[1]) < 1e-4:
                up = np.array([0, 1, 0], dtype=float)
            else:
                up = np.array([0, 0, 1], dtype=float)

            v = np.cross(d, up)
            v /= np.linalg.norm(v)
            w = np.cross(d, v)

            angles = np.linspace(0, 2 * np.pi, n_segments, endpoint=False)
            circle_bottom = (
                p0[:, None]
                + radius * np.cos(angles)[None, :] * v[:, None]
                + radius * np.sin(angles)[None, :] * w[:, None]
            )
            circle_top = (
                p1[:, None]
                + radius * np.cos(angles)[None, :] * v[:, None]
                + radius * np.sin(angles)[None, :] * w[:, None]
            )

            x = np.hstack([circle_bottom[0, :], circle_top[0, :]])
            y = np.hstack([circle_bottom[1, :], circle_top[1, :]])
            z = np.hstack([circle_bottom[2, :], circle_top[2, :]])

            i_list, j_list, k_list = [], [], []
            for seg in range(n_segments):
                seg_next = (seg + 1) % n_segments
                b0 = seg
                b1 = seg_next
                t0 = seg + n_segments
                t1 = seg_next + n_segments

                # Two triangles per segment
                i_list.extend([b0, b1])
                j_list.extend([b1, t0])
                k_list.extend([t0, b0])
                i_list.extend([b1])
                j_list.extend([t1])
                k_list.extend([t0])

            if add_caps:
                bottom_center_idx = len(x)
                top_center_idx = len(x) + 1
                x = np.append(x, [p0[0], p1[0]])
                y = np.append(y, [p0[1], p1[1]])
                z = np.append(z, [p0[2], p1[2]])

                # Bottom cap
                for seg in range(n_segments):
                    seg_next = (seg + 1) % n_segments
                    i_list.append(bottom_center_idx)
                    j_list.append(seg_next)
                    k_list.append(seg)
                # Top cap
                for seg in range(n_segments):
                    seg_next = (seg + 1) % n_segments
                    i_list.append(top_center_idx)
                    j_list.append(seg + n_segments)
                    k_list.append(seg_next + n_segments)

            return x, y, z, i_list, j_list, k_list

        def plot_bonds_as_cylinders(
            self,
            bonds,
            bond_color="gray",
            bond_radius=0.06,
            n_segments=32,
            add_caps=True,
        ):
            """
            Build a Plotly Figure by adding cylinder meshes for each bond.
            """
            fig = go.Figure()
            for bond in bonds:
                i_atom, j_atom = bond
                x1, y1, z1 = (
                    self.df["X"][i_atom],
                    self.df["Y"][i_atom],
                    self.df["Z"][i_atom],
                )
                x2, y2, z2 = (
                    self.df["X"][j_atom],
                    self.df["Y"][j_atom],
                    self.df["Z"][j_atom],
                )

                x_cyl, y_cyl, z_cyl, i_cyl, j_cyl, k_cyl = self.create_cylinder(
                    start_point=(x1, y1, z1),
                    end_point=(x2, y2, z2),
                    radius=bond_radius,
                    n_segments=n_segments,
                    add_caps=add_caps,
                )

                fig.add_trace(
                    go.Mesh3d(
                        x=x_cyl,
                        y=y_cyl,
                        z=z_cyl,
                        i=i_cyl,
                        j=j_cyl,
                        k=k_cyl,
                        color=bond_color,
                        opacity=1.0,
                        lighting=dict(
                            ambient=0.85,
                            diffuse=0.2,
                            specular=0.6,
                            roughness=0.5,
                            fresnel=0.5,
                        ),
                        flatshading=False,
                        name=f"bond_{i_atom}_{j_atom}",
                        hoverinfo="skip",
                    )
                )
            fig.update_layout(scene=dict(aspectmode="data"))
            return fig

        def plot(self):
            """
            Build a complete Plotly Figure with bonds (as cylinders) and atoms (as spheres).
            """
            bonds = self.detect_bonds()

            # Decorate the DataFrame with color and size info based on the elements dictionary.
            df = self.df.with_columns(
                pl.col("Symbol")
                .map_elements(
                    lambda s: self.elements[s]["color"], return_dtype=pl.Utf8
                )
                .alias("Color"),
                pl.col("Symbol")
                .map_elements(
                    lambda s: self.elements[s]["size"], return_dtype=pl.Float64
                )
                .alias("Size"),
            )

            # Start with bonds.
            fig = self.plot_bonds_as_cylinders(
                bonds,
                bond_color="gray",
                bond_radius=0.1,
                n_segments=24,
                add_caps=True,
            )

            # Plot each atom as a sphere.
            for idx in range(len(df)):
                x_atom = df["X"][idx]
                y_atom = df["Y"][idx]
                z_atom = df["Z"][idx]
                # Set sphere radius based on element type.
                radius_atom = ELEMENTS.get(df["Symbol"][idx], {}).get(
                    "covalent_radius", 0.5
                )
                radius_atom /= 2
                color_atom = ELEMENTS.get(df["Symbol"][idx], {}).get(
                    "color", "grey"
                )
                x_sphere, y_sphere, z_sphere, i_sphere, j_sphere, k_sphere = (
                    self.create_sphere(
                        center=(x_atom, y_atom, z_atom),
                        radius=radius_atom,
                        n_steps=32,
                    )
                )

                fig.add_trace(
                    go.Mesh3d(
                        x=x_sphere,
                        y=y_sphere,
                        z=z_sphere,
                        i=i_sphere,
                        j=j_sphere,
                        k=k_sphere,
                        color=color_atom,
                        opacity=1.0,
                        lighting=dict(
                            ambient=0.85,
                            diffuse=0.2,
                            specular=0.6,
                            roughness=0.5,
                            fresnel=0.5,
                        ),
                        name=f"Atom {idx}: {df['Symbol'][idx]}",
                        hoverinfo="skip",
                    )
                )

            fig.update_layout(
                width=self.width,
                height=self.height,
                title=self.title,
                scene=dict(
                    aspectmode="data",
                    xaxis_visible=False,
                    yaxis_visible=False,
                    zaxis_visible=False,
                    bgcolor="whitesmoke",
                    dragmode="orbit",  # Ensures orbital rotation mode is active
                ),
                scene_camera=dict(
                    up=dict(x=0, y=0, z=2),
                    eye=dict(x=0, y=2.5, z=0),
                    center=dict(x=0, y=0, z=0),
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(dict(yanchor="top", y=0.99, xanchor="left", x=0.01)),
            )
            return fig


    from collections import namedtuple

    # import numpy as np
    # import plotly.graph_objects as go
    from scipy.ndimage import zoom
    from skimage import measure

    CubeData = namedtuple("CubeData", ["origin", "basis_vectors", "grid", "data"])


    class CubeFileRenderer:
        def __init__(self, filepath):
            self.filepath = filepath
            self.cube_data = self.read_cube_file(filepath)

        def read_cube_file(self, filepath):
            with open(filepath, "r") as file:
                lines = file.readlines()

            _comments = lines[:2]

            n_atoms, *origin = lines[2].split()
            n_atoms = int(n_atoms)

            # Cube files encode the unit (Bohrs or Angstroms) in the sign
            # of the number of atoms...
            # If n_atoms is negative, the units are in Angstroms
            #
            # Apparently this depends on the type of density.....
            # the diffdens cubes are _positive_ and bohrs,
            # while for MOs the cubes are _negative_ and in bohrs ._.
            unit = "bohr"
            if n_atoms < 0:
                n_atoms = -n_atoms
                unit = "angstrom"

            # scale = 0.529177 if unit == "bohr" else 1.0
            scale = 0.529177

            # print(f"Number of atoms: {n_atoms}")
            # print(f"Unit: {unit}")

            origin = np.array([float(coord) * scale for coord in origin])
            # print(f"Origin: {origin}")

            BasisVector = namedtuple("BasisVector", ["n_voxels", "x", "y", "z"])
            basis_vectors = {
                "x": BasisVector(
                    int(lines[3].split()[0]),
                    *[float(coord) * scale for coord in lines[3].split()[1:]],
                ),
                "y": BasisVector(
                    int(lines[4].split()[0]),
                    *[float(coord) * scale for coord in lines[4].split()[1:]],
                ),
                "z": BasisVector(
                    int(lines[5].split()[0]),
                    *[float(coord) * scale for coord in lines[5].split()[1:]],
                ),
            }

            if (
                not basis_vectors["x"].n_voxels
                == basis_vectors["y"].n_voxels
                == basis_vectors["z"].n_voxels
            ):
                raise ValueError("Number of voxels in each direction must be equal")

            grid_resolution = basis_vectors["x"].n_voxels

            # print(
            #     f"Grid: {basis_vectors['x'].n_voxels}, {basis_vectors['y'].n_voxels}, {basis_vectors['z'].n_voxels}"
            # )

            Atom = namedtuple("Atom", ["element", "charge", "x", "y", "z"])

            atoms = []
            for line in lines[6 : 6 + n_atoms]:
                element, charge, *coords = line.split()
                atoms.append(Atom(element, charge, *coords))
            # print(f"Atoms: {atoms}")

            # charge, mult = lines[6 + n_atoms].split()
            # print(f"Charge: {charge}")
            # print(f"Multiplicity: {mult}")

            # Remove freakin MO additional line after atoms
            if len(lines[6 + n_atoms].split()) == 2:
                n_atoms += 1

            grid_values = []
            for line in lines[6 + n_atoms :]:
                grid_values.extend(map(float, line.split()))

            grid_data = np.array(grid_values).reshape(
                basis_vectors["x"].n_voxels,
                basis_vectors["y"].n_voxels,
                basis_vectors["z"].n_voxels,
            )
            # print(f"Grid data shape: {grid_data.shape}")

            self.data = CubeData(origin, basis_vectors, grid_resolution, grid_data)

        def render_isosurface(
            self, isovalue=0.01, interpolation_factor: int = 1, opaque: bool = False
        ):
            data = self.data

            refined_data = zoom(input=data.data, zoom=interpolation_factor, order=3)

            # Calculate spacing for the grid
            spacing = (
                data.basis_vectors["x"].x * interpolation_factor,
                data.basis_vectors["y"].y * interpolation_factor,
                data.basis_vectors["z"].z * interpolation_factor,
            )

            # Extract vertices and faces using marching cubes
            vertices_pos, faces_pos, _, _ = measure.marching_cubes(
                refined_data, level=isovalue, spacing=spacing
            )
            vertices_neg, faces_neg, _, _ = measure.marching_cubes(
                refined_data, level=-isovalue, spacing=spacing
            )

            # Adjust vertices positions by origin offset
            vertices_pos += data.origin
            vertices_neg += data.origin

            fig = go.Figure()

            # Add positive isosurface
            fig.add_trace(
                go.Mesh3d(
                    x=vertices_pos[:, 0],
                    y=vertices_pos[:, 1],
                    z=vertices_pos[:, 2],
                    i=faces_pos[:, 0],
                    j=faces_pos[:, 1],
                    k=faces_pos[:, 2],
                    color="#004D40",
                    opacity=1 if opaque else 0.5,
                    # name="Density gain",
                    # showlegend=True,
                    hoverinfo="skip",
                    lighting=dict(
                        ambient=0.5,
                        diffuse=0.7,
                        specular=0.2,
                        roughness=0.2,
                        fresnel=0.1,
                    ),
                )
            )

            # Add negative isosurface
            fig.add_trace(
                go.Mesh3d(
                    x=vertices_neg[:, 0],
                    y=vertices_neg[:, 1],
                    z=vertices_neg[:, 2],
                    i=faces_neg[:, 0],
                    j=faces_neg[:, 1],
                    k=faces_neg[:, 2],
                    color="#1E88E5",
                    opacity=1 if opaque else 0.5,
                    # name="Density loss",
                    # showlegend=True,
                    hoverinfo="skip",
                    lighting=dict(
                        ambient=0.5,
                        diffuse=0.7,
                        specular=0.2,
                        roughness=0.2,
                        fresnel=0.1,
                    ),
                )
            )

            fig.update_layout(
                # title="Isosurface Visualization",
                scene=dict(
                    xaxis=dict(
                        showbackground=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                        title="",
                    ),
                    yaxis=dict(
                        showbackground=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                        title="",
                    ),
                    zaxis=dict(
                        showbackground=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                        title="",
                    ),
                ),
                legend=dict(dict(yanchor="top", y=0.99, xanchor="left", x=0.01)),
            )

            return fig


    # if __name__ == "__main__":
    #     cube = CubeFileRenderer(
    #         "/Users/freddy/Documents/Projects/chemical_reactivity_marimo/test/cubes/ch4.mo0a.cube"
    #     )
    #     fig = cube.render_isosurface(isovalue=0.00005, interpolation_factor=3)
    #     fig.show()

    """
    Module for molecular structure representation and manipulation.
    Provides classes and utilities for working with atoms, molecules, and coordinate systems.
    """

    from dataclasses import dataclass
    from typing import Self

    # import numpy as np
    # import plotly.graph_objects as go
    from numpy.typing import NDArray
    from rdkit import Chem
    from rdkit.Chem import AllChem


    @dataclass
    class Atom:
        """
        Represents an atom with its element type and 3D coordinates.

        Attributes:
        -----------
        element : str
            Chemical element symbol (e.g., 'H', 'C', 'O')
        coords : NDArray[np.float64]
            3D coordinates of the atom in Angstroms
        """

        element: str
        coords: NDArray[np.float64]

        def to_str(self) -> str:
            """
            Convert atom to string representation in XYZ format.

            Returns:
            --------
            str
                Formatted string with element and coordinates (e.g., "H 0.0000 0.0000 0.0000")
            """
            return f"{self.element} {self.coords[0]:.4f} {self.coords[1]:.4f} {self.coords[2]:.4f}"

        @classmethod
        def from_str(cls, line: str) -> "Atom":
            """
            Create an Atom instance from a string representation.

            Parameters:
            -----------
            line : str
                String containing element and coordinates (e.g., "H 0.0 0.0 0.0")

            Returns:
            --------
            Atom
                New Atom instance with parsed element and coordinates
            """
            element, *coords = line.split()
            return cls(element, coords=np.array([float(coord) for coord in coords]))


    def convert_smiles_to_xyz(smiles: str) -> str:
        """
        Convert a SMILES string to XYZ format using RDKit.

        Parameters:
        -----------
        smiles : str
            SMILES representation of molecule

        Returns:
        --------
        str
            XYZ format string containing atomic coordinates
        """
        # Convert SMILES string to a molecule object
        mol = Chem.MolFromSmiles(smiles)

        # Generate 3D conformer
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, useRandomCoords=False)  # type: ignore

        atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
        conf = mol.GetConformer()
        coords = [conf.GetAtomPosition(i) for i in range(mol.GetNumAtoms())]

        xyz_str = f"{len(atoms)}\nGenerated from SMILES: {smiles}\n"
        xyz_str += "\n".join(
            f"{atoms[i]} {coords[i].x:.4f} {coords[i].y:.4f} {coords[i].z:.4f}"
            for i in range(len(atoms))
        )

        return xyz_str


    class Molecule:
        """
        Represents a molecular structure with atoms and properties.

        Attributes:
        -----------
        atoms : list[Atom]
            List of atoms in the molecule
        charge : int
            Total molecular charge
        mult : int
            Spin multiplicity
        """

        def __init__(
            self, atoms: list[Atom], charge: int = 0, mult: int = 1
        ) -> None:
            """
            Initialize a Molecule instance.

            Parameters:
            -----------
            atoms : list[Atom]
                List of atoms comprising the molecule
            charge : int, optional
                Molecular charge. Defaults to 0
            mult : int, optional
                Spin multiplicity. Defaults to 1 (singlet)
            """
            self.atoms = atoms
            self.charge = charge
            self.mult = mult

        def __str__(self) -> str:
            """
            String representation of molecule in XYZ format.

            Returns:
            --------
            str
                XYZ format string of the molecule
            """
            return self.to_xyz()

        @property
        def spin(self) -> float:
            """
            Calculate the spin of the molecule.

            Returns:
            --------
            float
                Spin multiplicity
            """
            return (self.mult - 1) / 2

        @classmethod
        def from_xyz(cls, xyz: str) -> "Molecule":
            """
            Create a Molecule instance from XYZ format string.

            Parameters:
            -----------
            xyz : str
                XYZ format string containing molecular structure

            Returns:
            --------
            Molecule
                New Molecule instance with parsed atoms
            """
            atoms = []
            for line in xyz.split("\n")[2:]:
                element, *coords = line.split()
                coords = np.array([float(coord) for coord in coords])
                atoms.append(Atom(element, coords))
            return cls(atoms)

        def to_xyz(self) -> str:
            """
            Convert molecule to XYZ format string.

            Returns:
            --------
            str
                XYZ format string representation of the molecule
            """
            xyz_str = f"{len(self.atoms)}\n\n"
            xyz_str += "\n".join((atom.to_str() for atom in self.atoms))
            return xyz_str

        @classmethod
        def from_smiles(cls, smiles: str) -> "Molecule":
            """
            Create a Molecule instance from SMILES string.

            Parameters:
            -----------
            smiles : str
                SMILES representation of molecule

            Returns:
            --------
            Molecule
                New Molecule instance with 3D structure
            """
            xyz = convert_smiles_to_xyz(smiles)
            return cls.from_xyz(xyz)

        def get_distance(self, i: int, j: int) -> float:
            """
            Calculate distance between two atoms in the molecule.

            Parameters:
            -----------
            i : int
                Index of first atom
            j : int
                Index of second atom

            Returns:
            --------
            float
                Distance between atoms in Angstroms
            """
            return float(
                np.linalg.norm(self.atoms[i].coords - self.atoms[j].coords)
            )

        def set_distance(self, i: int, j: int, distance: float) -> Self:
            """
            Set the distance between two atoms in the molecule.

            Parameters:
            -----------
            i : int
                Index of first atom
            j : int
                Index of second atom
            distance : float
                Desired distance in Angstroms

            Notes:
            ------
            The second atom (j) is moved while keeping the first atom (i) fixed.
            The direction vector between the atoms is preserved.
            """
            direction = self.atoms[j].coords - self.atoms[i].coords
            direction /= np.linalg.norm(direction)
            self.atoms[j].coords = self.atoms[i].coords + direction * distance
            return self

        def plot(self) -> go.Figure:
            """
            Visualize the molecular structure using 3D rendering.
            """
            visualizer = MoleculeVisualizer.from_xyz_string(self.to_xyz())
            return visualizer.plot()
    return (
        AllChem,
        Atom,
        Chem,
        CubeData,
        CubeFileRenderer,
        ELEMENTS,
        Molecule,
        MoleculeVisualizer,
        NDArray,
        Self,
        convert_smiles_to_xyz,
        dataclass,
        go,
        measure,
        namedtuple,
        np,
        zoom,
    )


if __name__ == "__main__":
    app.run()
