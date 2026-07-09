"""P02_XS001 — Social Burden Rate b = 1 - Pn/S*.

Book Chapter 7 central finding: surplus value S* is decomposed into:
  S* = Pn + T + Eu

Where:
  Pn = profit-type income net of ALL taxes (Table 7.1 / Table 5.8)
  T  = state taxes from production
  Eu = unproductive expenses

The social burden rate b = (T + Eu) / S* = 1 - Pn/S* measures what fraction
of surplus value is absorbed by state and unproductive activities rather
than reinvested as productive capital.

REVIEW 2026-07 (workpackage E, Group A) — quantity correction:
  The prior implementation used NIPA Table 1.7.5 Line 17 (Corporate profits
  with IVA and CCAdj) as Pn. That is the WRONG quantity: corporate profits
  (~$31B in 1948) are far narrower than the book's Pn = "profit-type income
  net of all taxes" (Table 7.1 = $66.51B in 1948, which also includes
  proprietors'/rental/interest profit-type income net of taxes). Using
  corporate profits produced b = 0.79-0.86, whereas the book's b is 0.56-0.68
  (Table 7.1). See DIV-025.

  Fix: Pn is now sourced directly from ST 1994 Table 7.1 (book_tables CSV),
  and S* is S505-A (which reproduces the book's Table 7.1 S* column EXACTLY
  for 1948-1989 — verified 2026-07). b = 1 - Pn/S505 then reproduces the
  book's printed social burden rate to <=0.005 (2-dp rounding).

Book finding (1948-1989): b rises ~0.56 -> ~0.66 (16% increase), Figure 7.1.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "XS001"
SUBSERIES = "XS001-A"

# Book Pn (profit-type income net of all taxes), ST 1994 Table 7.1, 1948-1989.
PN_CSV = (Path(__file__).resolve().parents[2]
          / "data" / "source" / "book_tables" / "XS001_Table71_Pn.csv")


def compute() -> pd.DataFrame:
    Pn = pd.read_csv(PN_CSV)[["year", "Pn"]]

    s505 = pd.read_csv(DATA_FINAL / "S505.csv")
    s505 = s505[s505["series_id"] == "S505-A"][["year", "value"]].rename(columns={"value": "S_star"})

    merged = Pn.merge(s505, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["value"] = 1 - (merged["Pn"] / merged["S_star"])
    merged["series_id"] = SUBSERIES
    merged["units"] = "ratio"
    merged["stage"] = "book_period_derived"
    merged["provenance"] = "1 - (ST1994 Table 7.1 Pn / S505-A = S*)"
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
