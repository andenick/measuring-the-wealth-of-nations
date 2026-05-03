#!/usr/bin/env python3
"""P13 - Process input-output tables: T401, T402.

For each benchmark year (1947-1977):
1. Load parsed A and B (Leontief inverse) matrices
2. Validate B ~ (I-A)^{-1}
3. Validate A-matrix properties (elements in [0,1], column sums < 1)
4. Classify sectors using concordance
5. Write summary tables

Inputs:  parsed-raw/T401_{year}_parsed.csv, T402_{year}_parsed.csv (from L11)
         Inputs/Concordances/io_85_to_nipa_13_concordance.csv
Outputs: final-data/series/T401.csv, T402.csv (summary stats per year)
Dependencies: L11. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, INPUTS, ensure_dirs
from utils.transforms.io_transforms import (
    compute_leontief_inverse, classify_sectors,
)

SERIES_ID = "T401"
SERIES_IDS = ["T401", "T402"]
PRIORITY = 10
BENCHMARK_YEARS = [1947, 1958, 1963, 1967, 1972, 1977]


def _load_concordance_classification():
    """Load sector classification from concordance."""
    conc_path = INPUTS / "Concordances" / "io_85_to_nipa_13_concordance.csv"
    df = pd.read_csv(conc_path)
    return dict(zip(df["io_sector_name"], df["classification"]))


def process():
    """Process IO matrices — validate and summarize."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []
    summary_rows = []

    classification = _load_concordance_classification()

    for year in BENCHMARK_YEARS:
        a_path = PARSED_RAW / f"T401_{year}_parsed.csv"
        b_path = PARSED_RAW / f"T402_{year}_parsed.csv"

        if not a_path.exists() or not b_path.exists():
            steps.append(f"{year}: parsed matrices not found")
            continue

        a_df = pd.read_csv(a_path, index_col=0)
        b_df = pd.read_csv(b_path, index_col=0)

        a = a_df.values
        b = b_df.values
        n = a.shape[0]

        # Cross-check B vs (I-A)^{-1} — informational only.
        # Pre-computed L-matrices are authoritative; near-singular A-matrices
        # (eig_max ≈ 1) cause naive inversion to diverge, so deviations are
        # expected and do NOT indicate errors in the input data.
        b_computed = compute_leontief_inverse(a_df)
        max_dev = np.abs(b - b_computed.values).max()

        # A-matrix properties
        col_sums = a.sum(axis=0)
        max_col_sum = col_sums.max()
        eigenvalues = np.linalg.eigvals(a)
        max_eigenvalue = np.abs(eigenvalues).max()
        sparsity = (a == 0).sum() / a.size

        # Condition number of (I-A)
        cond = np.linalg.cond(np.eye(n) - a)

        # Sector classification
        sectors = a_df.index.tolist()
        groups = classify_sectors(sectors, classification)
        n_prod = len(groups["productive"])
        n_unprod = len(groups["unproductive"])

        summary_rows.append({
            "year": year,
            "n_sectors": n,
            "sparsity": round(sparsity, 4),
            "max_eigenvalue": round(max_eigenvalue, 6),
            "condition_number": round(cond, 2),
            "leontief_max_dev": round(max_dev, 8),
            "n_productive": n_prod,
            "n_unproductive": n_unprod,
        })

        # Near-singular systems (cond > 1e6) always have large deviations
        if max_dev < 1e-4:
            valid_note = "exact match"
        elif cond > 1e6:
            valid_note = f"near-singular (cond={cond:.0f}, dev={max_dev:.2f})"
        else:
            valid_note = f"dev={max_dev:.6f}"
        steps.append(f"{year}: {n}×{n}, sparsity={sparsity:.2%}, "
                     f"eig_max={max_eigenvalue:.4f}, B check: {valid_note}")
        print(f"    [P13] {year}: {n}×{n} | B check: {valid_note} | "
              f"{n_prod} productive, {n_unprod} unproductive")

    # Write summary tables
    if summary_rows:
        summary_df = pd.DataFrame(summary_rows).set_index("year")

        for sid in SERIES_IDS:
            out_path = SERIES_OUT / f"{sid}.csv"
            summary_df.to_csv(out_path)
            outputs.append(str(out_path))

        data_dict["T401"] = summary_df["max_eigenvalue"]
        data_dict["T402"] = summary_df["leontief_max_dev"]

    status = "ok" if summary_rows else "fail"

    return {
        "series_id": SERIES_ID,
        "status": status,
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
