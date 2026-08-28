"""
Utility functions for running electronic structure calculations.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


HARTREE_TO_EV = 27.211386245988
DEBYE_LIMIT = 10.0


def make_input(xyz, name, method="wB97X-D3", basis="def2-SVP",
               charge=0, mult=1, solvent="water"):

    xyz_text = Path(xyz).read_text()

    inp = []

    inp.append(
        f"! {method} {basis} TightSCF CPCM({solvent})"
    )

    inp.append(
        "%pal nprocs 8 end"
    )

    inp.append(
        "%maxcore 4000"
    )

    inp.append(
        "%output Print[P_Basis] 2 end"
    )

    inp.append(
        "* xyz {} {}".format(
            charge,
            mult
        )
    )

    inp.append(
        xyz_text
    )

    inp.append("*")

    return "\n".join(inp)


def run_orca(input_file, executable="orca"):

    output_file = str(input_file) + ".out"

    cmd = [
        executable,
        str(input_file),
    ]

    with open(output_file, "w") as f:

        subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.STDOUT,
            check=True,
        )

    return output_file


def read_energy(path):

    energy = None

    for line in Path(path).read_text().splitlines():

        if "FINAL SINGLE POINT ENERGY" in line:

            energy = float(
                line.split()[-1]
            )

    if energy is None:
        raise RuntimeError(
            "energy not found"
        )

    return energy


def extract_summary(path):

    text = Path(path).read_text()

    e = read_energy(path)

    dipole = None

    m = re.search(
        r"Total Dipole Moment\s+:\s+([0-9.]+)",
        text
    )

    if m:
        dipole = float(
            m.group(1)
        )


    imag = []

    for line in text.splitlines():

        if "cm**-1" in line:

            value = float(
                line.split()[1]
            )

            if value < -50:
                imag.append(value)


    return {
        "energy_hartree": e,
        "energy_ev": e * HARTREE_TO_EV,
        "dipole_debye": dipole,
        "imaginary_frequencies": imag,
    }


def create_cube_job(
    filename,
    orbital="HOMO",
    isovalue=0.03,
):

    text = []

    text.append(
        "Multiwfn cube generation"
    )

    text.append(
        f"orbital={orbital}"
    )

    text.append(
        f"isovalue={isovalue}"
    )

    Path(filename).write_text(
        "\n".join(text)
    )


def analyse_structure(
    xyz,
    input_file,
    output_file,
):

    inp = make_input(
        xyz,
        Path(input_file).stem,
    )

    Path(input_file).write_text(
        inp
    )

    run_orca(
        input_file
    )

    summary = extract_summary(
        output_file
    )

    if len(summary["imaginary_frequencies"]) > 0:

        summary["status"] = "unstable"

    else:

        summary["status"] = "stable"


    if summary["dipole_debye"]:

        if summary["dipole_debye"] > DEBYE_LIMIT:

            summary["note"] = (
                "large dipole"
            )


    create_cube_job(
        "density.cube",
        "HOMO",
        0.03,
    )


    return summary