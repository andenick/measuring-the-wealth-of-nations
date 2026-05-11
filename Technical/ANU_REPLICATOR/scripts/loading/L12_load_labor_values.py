#!/usr/bin/env python3
"""L12 - Load Labor Value Inputs: T701, T702, T703.

For each benchmark year (1947-1977):
1. Load Z-matrix and A-matrix to recover gross output
2. Distribute Mohun 13-industry employment to 85 sectors via output weights
3. Compute direct labor coefficients hp*_j = Employment_j / x_j
4. Write parsed hp* vectors

Inputs:  data/io-matrices/{year}_Z_matrix.csv, {year}_A_matrix.csv
         Inputs/ExternalSources/Mohun/mohun_employment_by_industry_1948_1989.csv
         Inputs/Concordances/io_85_to_nipa_13_concordance.csv
Outputs: parsed-raw/T701_{year}_hp_parsed.csv
Dependencies: None (but uses same matrices as L11)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from lib.paths import IO_MATRICES, INPUTS, PARSED_RAW, ensure_dirs
from lib.transforms.io_transforms import (
    load_matrix_csv, recover_gross_output, distribute_employment,
)

SERIES_IDS = ["T701", "T702", "T703"]
BENCHMARK_YEARS = [1947, 1958, 1963, 1967, 1972, 1977]


def _load_concordance():
    conc_path = INPUTS / "Concordances" / "io_85_to_nipa_13_concordance.csv"
    return pd.read_csv(conc_path)


def _load_mohun_employment(year):
    """Load Mohun employment by industry for a given year."""
    emp_path = (INPUTS / "ExternalSources" / "Mohun"
                / "mohun_employment_by_industry_1948_1989.csv")
    if not emp_path.exists():
        return None
    df = pd.read_csv(emp_path)
    df["year"] = df["year"].astype(int)
    year_data = df[df["year"] == year][["industry", "employment"]].copy()
    if len(year_data) == 0:
        return None
    return year_data


def load():
    """Load labor value inputs — hp* vectors for benchmark years."""
    ensure_dirs()
    outputs = []
    conc = _load_concordance()
    sector_labels = conc["io_sector_name"].tolist()

    for year in BENCHMARK_YEARS:
        # Load Z and A matrices
        z_path = IO_MATRICES / f"{year}_Z_matrix.csv"
        a_path = IO_MATRICES / f"{year}_A_matrix.csv"
        if not z_path.exists() or not a_path.exists():
            print(f"    [L12] {year}: Z or A matrix not found")
            continue

        z_arr = load_matrix_csv(z_path, n=85)
        a_arr = load_matrix_csv(a_path, n=85)
        x = recover_gross_output(z_arr, a_arr)

        # Get employment data — Mohun covers 1948-1989
        # For 1947, use 1948 as proxy
        emp_year = year if year >= 1948 else 1948
        emp_data = _load_mohun_employment(emp_year)
        if emp_data is None:
            print(f"    [L12] {year}: Mohun employment not available for {emp_year}")
            continue

        # Distribute 13-industry employment to 85 sectors
        emp_85 = distribute_employment(emp_data, x, conc)

        # Compute direct labor coefficients: hp*_j = emp_j / x_j
        with np.errstate(divide="ignore", invalid="ignore"):
            hp_star = np.where(x > 0, emp_85 / x, 0.0)

        # Write as parsed CSV
        hp_df = pd.DataFrame({
            "sector": sector_labels,
            "employment": emp_85,
            "gross_output": x,
            "hp_star": hp_star,
        })
        out_path = PARSED_RAW / f"T701_{year}_hp_parsed.csv"
        hp_df.to_csv(out_path, index=False)
        outputs.append(str(out_path))
        print(f"    [L12] {year}: hp* vector computed "
              f"(emp from {'1948 proxy' if year < 1948 else str(emp_year)})")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok" if outputs else "fail",
        "message": f"Labor value inputs | {len(outputs)} benchmark years",
        "outputs": outputs,
    }
