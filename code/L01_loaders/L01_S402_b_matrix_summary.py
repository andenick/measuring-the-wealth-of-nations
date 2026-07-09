"""L01_S402 — Leontief inverse B-matrix summary statistics."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io_matrix import b_matrix_summary, BENCHMARK_YEARS_SIC, BENCHMARK_YEARS_NAICS  # noqa: E402


def load() -> pd.DataFrame:
    rows = []
    for yr in BENCHMARK_YEARS_SIC + BENCHMARK_YEARS_NAICS:
        try:
            rows.append(b_matrix_summary(yr))
        except Exception as e:
            print(f"      [L01_S402] WARN year {yr}: {e}")
    df = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
    # workpackage C: canonical scalar = mean total-requirements column multiplier of the
    # REBUILT Leontief inverse (interpretable, ~1.8-2.7 for the US; for NAICS
    # years it summarizes BEA's own published Total Requirements table).
    # Replaces the Frobenius norm of the defective-cache inverse (~30-100).
    df["value"] = df["b_colsum_mean"]
    df["series_id"] = "S402-A"
    df["units"] = "matrix_summary"
    return df


def run():
    df = load()
    print(f"    [L01_S402] {len(df)} benchmark years; "
          f"B mean column multiplier: {df['b_colsum_mean'].min():.3f}-{df['b_colsum_mean'].max():.3f}")
    return df


if __name__ == "__main__":
    run()
