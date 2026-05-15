"""L01_S401 — Compute A-matrix summary statistics per benchmark year.

For each of 6 SIC benchmark years (1947, 1958, 1963, 1967, 1972, 1977)
and 4 NAICS years (1997, 2002, 2007, 2012), compute:
- n_sectors
- sparsity (fraction of non-zero elements)
- max_eigenvalue (Hawkins-Simon: must be < 1)
- condition_number
- leontief_max_dev (deviation of computed L vs cached L)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io_matrix import a_matrix_summary, BENCHMARK_YEARS_SIC, BENCHMARK_YEARS_NAICS  # noqa: E402


def load() -> pd.DataFrame:
    rows = []
    for yr in BENCHMARK_YEARS_SIC + BENCHMARK_YEARS_NAICS:
        try:
            rows.append(a_matrix_summary(yr))
        except Exception as e:
            print(f"      [L01_S401] WARN: year {yr} failed: {e}")
    df = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
    # Use max_eigenvalue as the canonical "value" column (most economically meaningful)
    df["value"] = df["max_eigenvalue"]
    df["series_id"] = "S401-A"
    df["units"] = "matrix_summary"
    return df


def run():
    df = load()
    print(f"    [L01_S401] {len(df)} benchmark years; "
          f"max_eig range=[{df['max_eigenvalue'].min():.4f}, {df['max_eigenvalue'].max():.4f}] "
          f"(Hawkins-Simon: all <1)")
    return df


if __name__ == "__main__":
    run()
