"""P02_AS002 — Khanjian (1989) cross-validation of S506.

Khanjian re-estimated the rate of exploitation using a different treatment of
unincorporated income (treating it ALL as profit). His estimates run ~20%
higher than Shaikh & Tonak's. The book's Section 5.10 reports these
benchmark values for cross-validation; we encode them as a fixed comparison
table and compute the gap from S506.

This is not a time series of new values — it's a 5-year benchmark comparison
table. The output is wide: each row is (year, S506_value, khanjian_e_star_rev,
khanjian_e_rev, gap_pct, our_gap_to_khanjian_e_star_rev_pct).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "AS002"
SUBSERIES = "AS002-A"

# Book Table 5.12 — Khanjian's published estimates
KHANJIAN = {
    1958: {"e_star_rev": 2.445, "e_rev": 2.638, "gap_pct": 7.3},
    1963: {"e_star_rev": 2.467, "e_rev": 2.644, "gap_pct": 6.7},
    1967: {"e_star_rev": 2.648, "e_rev": 2.884, "gap_pct": 8.2},
    1972: {"e_star_rev": 2.606, "e_rev": 2.874, "gap_pct": 9.3},
    1977: {"e_star_rev": 2.674, "e_rev": 2.913, "gap_pct": 8.2},
}


def compute() -> pd.DataFrame:
    s506 = pd.read_csv(DATA_FINAL / "S506.csv")
    s506 = s506[s506["series_id"] == "S506-A"][["year", "value"]].set_index("year")["value"].to_dict()

    rows = []
    for yr, k in KHANJIAN.items():
        s506_v = s506.get(yr)
        if s506_v is None:
            continue
        # Gap between our S506 and Khanjian's e_star_rev (revised money-form)
        gap_to_khanjian = (k["e_star_rev"] - s506_v) / s506_v * 100
        rows.append({
            "series_id":              SUBSERIES,
            "year":                   yr,
            "value":                  s506_v,
            "units":                  "ratio",
            "stage":                  "cross_validation",
            "provenance":             "S506 vs Khanjian Table 5.12",
            "khanjian_e_star_rev":    k["e_star_rev"],
            "khanjian_e_rev":         k["e_rev"],
            "book_published_gap_pct": k["gap_pct"],
            "our_gap_to_khanjian_pct": round(gap_to_khanjian, 2),
        })
    return pd.DataFrame(rows)


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(df)} cross-validation rows; wrote {final_path.name}")
    print(f"      Our S506 vs Khanjian e_star_rev gaps: "
          f"{df['our_gap_to_khanjian_pct'].tolist()}")
    return df


if __name__ == "__main__":
    run()
