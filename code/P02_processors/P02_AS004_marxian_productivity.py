"""P02_AS004 — Marxian Productivity (q* = TPr / Hp).

Real productive output per productive worker, in 2017 dollars per worker.

Components:
- TPr = TP* (S501-COMBINED) deflated by GDPDEF (real total productive product)
- Hp ≈ productive worker count from S515 (TableE3 narrow) for 1948-1961;
       book-period only. Modern extension via BLS sectoral production workers
       requires sectoral concordance — left for refinement.

For Hp coverage gaps (1962-2024), emit explicit NaN per the no-synthetic
rule. The book's central q* trajectory (1948-1961) is still captured.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.fred_cache import load_fred_annual  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "AS004"
SUBSERIES = "AS004-A"


def compute() -> pd.DataFrame:
    s501 = pd.read_csv(DATA_FINAL / "S501.csv")
    s501 = s501[s501["series_id"] == "S501-A"][["year", "value"]].rename(columns={"value": "TP_star"})
    s515 = pd.read_csv(DATA_FINAL / "S515.csv")
    s515 = s515[s515["series_id"] == "S515-A"][["year", "value"]].rename(columns={"value": "Lp_thousands"})

    gdpdef = load_fred_annual("fred_GDPDEF.json").rename(columns={"value": "deflator"})

    # Merge on year; result limited to overlap (S515 has 14 years 1948-1961; deflator has 1947+)
    merged = s501.merge(s515, on="year").merge(gdpdef, on="year").sort_values("year").reset_index(drop=True)
    # q* = real TP / Hp (Hp in thousands → real $ per thousand workers → divide for $/worker)
    merged["TPr"] = merged["TP_star"] / (merged["deflator"] / 100)  # real in 2017 $
    merged["value"] = merged["TPr"] / (merged["Lp_thousands"] / 1000.0)  # $B / millions of workers = $thousands per worker
    merged["series_id"] = SUBSERIES
    merged["units"] = "index"  # productivity index, real $ per productive worker (in thousands)
    merged["stage"] = "book_period_partial_1948_1961"
    merged["provenance"] = "S501 / GDPDEF / S515 (book-period coverage only)"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_AS004] {len(df)} rows {df['year'].min()}-{df['year'].max()}; "
          f"q* {df.iloc[0]['year']}={df.iloc[0]['value']:.2f}, {df.iloc[-1]['year']}={df.iloc[-1]['value']:.2f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
