"""P02_XS001 — Social Burden Rate b = 1 - Pn/S*.

Book Chapter 7 central finding: surplus value S* is decomposed into:
  S* = Pn + T + Eu

Where:
  Pn = net profit (corporate profits, productively employed)
  T  = state taxes from production
  Eu = unproductive expenses

The social burden rate b = (T + Eu) / S* = 1 - Pn/S* measures what fraction
of surplus value is absorbed by state and unproductive activities rather
than reinvested as productive capital.

**Pn approximation**: we use NIPA Table 1.7.5 Line 17 (Corporate profits
with IVA and CCAdj) as Pn. This is TOTAL corporate profits — slightly
over-counts vs S&T's "productive corporate profits" (excludes financial-
sector profits). The DPR documents this approximation; a more refined
version would apply the productive/unproductive concordance to NIPA
profit-by-industry data.

Book finding (1948-1989): b rises 0.56 -> 0.66 (16% increase).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.bea_cache import load_bea_line  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "XS001"
SUBSERIES = "XS001-A"


def compute() -> pd.DataFrame:
    # Pn from NIPA 1.7.5 Line 17 (corporate profits)
    Pn = load_bea_line("nipa_1_7_5_gross_output_by_industry.csv", 17)
    Pn["value"] = Pn["value"] / 1000.0  # millions -> billions
    Pn = Pn.rename(columns={"value": "Pn"})

    s505 = pd.read_csv(DATA_FINAL / "S505.csv")
    s505 = s505[s505["series_id"] == "S505-A"][["year", "value"]].rename(columns={"value": "S_star"})

    merged = Pn.merge(s505, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["value"] = 1 - (merged["Pn"] / merged["S_star"])
    merged["series_id"] = SUBSERIES
    merged["units"] = "ratio"
    merged["stage"] = "book_period_derived"
    merged["provenance"] = "1 - (NIPA 1.7.5 Line 17 / S505)"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    v_1948 = float(df[df["year"] == 1948]["value"].iloc[0]) if (df["year"] == 1948).any() else None
    v_1989 = float(df[df["year"] == 1989]["value"].iloc[0]) if (df["year"] == 1989).any() else None
    print(f"    [P02_XS001] {len(df)} rows; b 1948={v_1948:.4f}, 1989={v_1989:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
