"""P02_XS004 — Marxian Productivity index (1948 = 100).

Real productive output per productive WORKER, indexed to 1948 = 100 to match
the book's Table J.1 row 2 base ("q* index numbers 1948 = 100").

Components:
- TPr = TP* (S501-A) deflated by GDPDEF (real total productive product)
- Lp  = productive worker count from S515-A (Appendix E.3 / Table G.2),
        1948-1989.

REVIEW 2026-07 (workpackage E, Group A):
  1. Rebased so 1948 = 100 (was 112.09, an arbitrary un-normalized level) to
     match book Table J.1 row 2. Rebase = value / value[1948] * 100.
  2. NOTE ON QUANTITY: the book's q* = TPr / Hp is per productive-worker-HOUR
     (Hp = hp x Lp, total hours; Table J.1 line 23). XS004 divides by Lp
     (worker COUNT), so it is a per-productive-WORKER index — a close cousin,
     NOT identical. Because hours-per-worker declined over 1948-1989, the
     rebased XS004 tracks the book's per-hour q* index within ~4.4% (deltas
     rise to +2.4% by 1989). Validated against book J.1 (class `book`,
     share_series tolerance); the per-worker-vs-per-hour gap is DIV-026.

For Lp coverage gaps outside 1948-1989, values are absent (no synthetic fill).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.fred_cache import load_fred_annual  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "XS004"
SUBSERIES = "XS004-A"


def compute() -> pd.DataFrame:
    s501 = pd.read_csv(DATA_FINAL / "S501.csv")
    s501 = s501[s501["series_id"] == "S501-A"][["year", "value"]].rename(columns={"value": "TP_star"})
    s515 = pd.read_csv(DATA_FINAL / "S515.csv")
    s515 = s515[s515["series_id"] == "S515-A"][["year", "value"]].rename(columns={"value": "Lp_thousands"})

    gdpdef = load_fred_annual("fred_GDPDEF.json").rename(columns={"value": "deflator"})

    # Merge on year; result limited to overlap (S515 has 14 years 1948-1961; deflator has 1947+)
    merged = s501.merge(s515, on="year").merge(gdpdef, on="year").sort_values("year").reset_index(drop=True)
    # Real productive output per productive worker (pre-index level).
    merged["TPr"] = merged["TP_star"] / (merged["deflator"] / 100)  # real in 2017 $
    merged["level"] = merged["TPr"] / (merged["Lp_thousands"] / 1000.0)  # $B / millions of workers

    # Rebase to 1948 = 100 (book Table J.1 row 2 base). No 1948 -> fail loudly.
    base_rows = merged.loc[merged["year"] == 1948, "level"]
    if base_rows.empty:
        raise ValueError("XS004 rebasing requires a 1948 base value; none found.")
    base = float(base_rows.iloc[0])
    merged["value"] = merged["level"] / base * 100.0

    merged["series_id"] = SUBSERIES
    merged["units"] = "index"  # productivity index, 1948 = 100 (per productive worker)
    merged["stage"] = "book_period_indexed_1948_base"
    merged["provenance"] = "index(1948=100) of real TP*(S501)/GDPDEF / Lp(S515-A)"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_XS004] {len(df)} rows {df['year'].min()}-{df['year'].max()}; "
          f"q* {df.iloc[0]['year']}={df.iloc[0]['value']:.2f}, {df.iloc[-1]['year']}={df.iloc[-1]['value']:.2f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
