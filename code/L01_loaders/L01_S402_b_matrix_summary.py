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
    df["value"] = df["b_frobenius_norm"]
    df["series_id"] = "S402-A"
    df["units"] = "matrix_summary"
    return df


def run():
    df = load()
    print(f"    [L01_S402] {len(df)} benchmark years; "
          f"B Frobenius norm: {df['b_frobenius_norm'].min():.2f}-{df['b_frobenius_norm'].max():.2f}")
    return df


if __name__ == "__main__":
    run()
