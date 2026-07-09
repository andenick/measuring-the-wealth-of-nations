"""P02_XS002 — Khanjian (1989) cross-validation of S506.

Book Table 5.12 (Section 5.10, p.144; source Khanjian 1989 table 19) reports, on the
SAME aggregate and via the consistent procedure, the labor-value rate e = S/V and the
money-form rate e* = S*/V*. The money rate e* is uniformly 6%-9% LOWER than the value
rate e (revenue-side (e-e*)/e = 7.3/6.7/8.2/9.3/8.2% at 1958/1963/1967/1972/1977) — this
is the book's "differ by only small amounts (6%-9%)" statement (Ch7 s7.3, folio 223). The
KHANJIAN dict below encodes that table verbatim: e_star_rev = e* (money form), e_rev = e
(value form), gap_pct = (e-e*)/e. VALUES VERIFIED against the canonical v2 KB Table 5.12
(book_digitization_v2/CSV_Tables/table_017_017_01.csv, Revenue side)
— no numeric change.

SEPARATE COMPARISON (do not conflate with the 6%-9%): Khanjian's LEVELS (e* ~2.4-2.9) sit
ABOVE Shaikh & Tonak's own money rate S*/V* (S506 ~2.0). The book (Ch6) attributes this to
Khanjian making "no adjustment for the wage equivalent of proprietors and partners in the
noncorporate sector" — an adjustment S&T incorporate (lowering surplus value, raising
variable capital), so Khanjian's estimates are "substantially larger than the authors'".
The column our_gap_to_khanjian_pct = (e* - S506)/S506 measures THIS ~+20% level gap, NOT
the 6%-9% value-vs-money deviation. The validated XS002 quantity is S&T's own S*/V* at the
I-O benchmark years (V03 anchors to book Table H.1 / Table I.1 Line 23), not Khanjian's e*.

This is not a time series of new values — it's a 5-year benchmark comparison table. The
output is wide: each row is (year, S506_value, khanjian_e_star_rev, khanjian_e_rev,
gap_pct, our_gap_to_khanjian_pct).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "XS002"
SUBSERIES = "XS002-A"

# Book Table 5.12 — Khanjian's published estimates. De-hardcoded 2026-07-08
# (Tier-A W2, anti-pattern #3): the inline dict was moved verbatim to a source
# CSV; this helper loads it. No numeric change (output byte-identical).
KHANJIAN_CSV = (Path(__file__).resolve().parents[2]
                / "data" / "source" / "book_tables"
                / "XS002_Table512_khanjian.csv")


def _load_khanjian() -> dict:
    df = pd.read_csv(KHANJIAN_CSV, comment="#")
    return {
        int(r.year): {"e_star_rev": float(r.e_star_rev),
                      "e_rev": float(r.e_rev),
                      "gap_pct": float(r.gap_pct)}
        for r in df.itertuples()
    }


def compute() -> pd.DataFrame:
    KHANJIAN = _load_khanjian()
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
