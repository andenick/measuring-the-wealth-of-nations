"""P02_S702 — Prices of Production scalar (matrix-derived).

Book formula: p = a₀ × (I + r*B + r*²·B² + ...) where r* is the
profit rate. Simplified scalar proxy:
  p_scalar(year) = mean column sum of B × (1 + r*_year)

For benchmark years where we have S513 r*, multiply. Otherwise use the
mean r* over 1948-1989 as approximation. This captures the book's
qualitative finding that prices of production are close to but
systematically deviate from labor values.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.io_matrix import load_a_matrix, BENCHMARK_YEARS_SIC, BENCHMARK_YEARS_NAICS  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S702"
SUBSERIES = "S702-A"


def compute() -> pd.DataFrame:
    # Load S513 r* for benchmark-year markups
    s513 = pd.read_csv(DATA_FINAL / "S513.csv")
    s513 = s513[s513["series_id"] == "S513-A"][["year", "value"]].set_index("year")["value"]
    avg_r = float(s513.mean())

    rows = []
    for yr in BENCHMARK_YEARS_SIC + BENCHMARK_YEARS_NAICS:
        try:
            A = load_a_matrix(yr).to_numpy()
            B = np.linalg.inv(np.eye(A.shape[0]) - A)
            base = float(B.sum(axis=0).mean())
            r_yr = float(s513.get(yr, avg_r))
            value = base * (1 + r_yr)
            rows.append({"year": yr, "value": value, "r_used": r_yr})
        except Exception as e:
            print(f"      [P02_S702] WARN year {yr}: {e}")
    df = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
    df["series_id"] = SUBSERIES
    df["units"] = "index"
    df["stage"] = "benchmark_only_matrix_derived"
    df["provenance"] = "S701 base × (1 + S513 r*)"
    return df[["series_id", "year", "value", "units", "stage", "provenance", "r_used"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S702] {len(df)} benchmark years; range=[{df['value'].min():.4f}, {df['value'].max():.4f}]; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
