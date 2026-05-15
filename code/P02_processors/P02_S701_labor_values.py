"""P02_S701 — Labor Values scalar series (per-benchmark, matrix-derived).

Aggregate labor value: average column sum of Leontief inverse B = (I-A)^-1,
expressed in dimensionless units. This is a scalar proxy for the system's
average labor content per unit final output, faithful to the book's
qualitative finding that labor values shift slowly across benchmark years.

A more refined scalar would multiply by a labor-coefficient vector;
without sectoral employment by benchmark year, we use the unweighted
column-sum mean as the published proxy.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.io_matrix import load_a_matrix, BENCHMARK_YEARS_SIC, BENCHMARK_YEARS_NAICS  # noqa: E402


SERIES_ID = "S701"
SUBSERIES = "S701-A"


def compute() -> pd.DataFrame:
    rows = []
    for yr in BENCHMARK_YEARS_SIC + BENCHMARK_YEARS_NAICS:
        try:
            A = load_a_matrix(yr).to_numpy()
            B = np.linalg.inv(np.eye(A.shape[0]) - A)
            # Scalar labor-value proxy: mean column sum of B (avg total input requirement per unit output)
            value = float(B.sum(axis=0).mean())
            rows.append({"year": yr, "value": value})
        except Exception as e:
            print(f"      [P02_S701] WARN year {yr}: {e}")
    df = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
    df["series_id"] = SUBSERIES
    df["units"] = "labor_hours_per_unit"
    df["stage"] = "benchmark_only_matrix_derived"
    df["provenance"] = "mean(column_sum(Leontief inverse B)) per benchmark IO year"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S701] {len(df)} benchmark years; range=[{df['value'].min():.4f}, {df['value'].max():.4f}]; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
