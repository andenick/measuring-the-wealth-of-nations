#!/usr/bin/env python3
"""L11 - Load IO Matrices: T401 (A-matrix), T402 (Leontief inverse B).

Loads 85x85 headerless CSV matrices for 6 benchmark years (1947-1977),
labels rows/columns using the IO-to-NIPA concordance, and writes parsed CSVs.

Inputs:  data/io-matrices/{year}_A_matrix.csv, {year}_L_matrix.csv
         Inputs/Concordances/io_85_to_nipa_13_concordance.csv
Outputs: parsed-raw/T401_{year}_parsed.csv, T402_{year}_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import IO_MATRICES, INPUTS, PARSED_RAW, ensure_dirs
from utils.transforms.io_transforms import load_matrix_csv

SERIES_IDS = ["T401", "T402"]
BENCHMARK_YEARS = [1947, 1958, 1963, 1967, 1972, 1977]


def _load_concordance():
    """Load the 85-sector concordance to get sector labels."""
    conc_path = INPUTS / "Concordances" / "io_85_to_nipa_13_concordance.csv"
    df = pd.read_csv(conc_path)
    return df


def load():
    """Load A and L (Leontief) matrices for all benchmark years."""
    ensure_dirs()
    outputs = []
    conc = _load_concordance()
    sector_labels = conc["io_sector_name"].tolist()

    for year in BENCHMARK_YEARS:
        # T401: A-matrix (technical coefficients)
        a_path = IO_MATRICES / f"{year}_A_matrix.csv"
        if not a_path.exists():
            print(f"    [L11] T401_{year}: A-matrix not found")
            continue
        a_arr = load_matrix_csv(a_path, n=85)
        a_df = pd.DataFrame(a_arr, index=sector_labels, columns=sector_labels)
        out_a = PARSED_RAW / f"T401_{year}_parsed.csv"
        a_df.to_csv(out_a)
        outputs.append(str(out_a))

        # T402: L-matrix (pre-computed Leontief inverse B)
        l_path = IO_MATRICES / f"{year}_L_matrix.csv"
        if not l_path.exists():
            print(f"    [L11] T402_{year}: L-matrix not found")
            continue
        l_arr = load_matrix_csv(l_path, n=85)
        l_df = pd.DataFrame(l_arr, index=sector_labels, columns=sector_labels)
        out_l = PARSED_RAW / f"T402_{year}_parsed.csv"
        l_df.to_csv(out_l)
        outputs.append(str(out_l))

        print(f"    [L11] {year}: A-matrix + Leontief inverse loaded (85×85)")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok" if outputs else "fail",
        "message": f"IO matrices | {len(BENCHMARK_YEARS)} years, {len(outputs)} files",
        "outputs": outputs,
    }
