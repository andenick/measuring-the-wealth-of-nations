"""L01_S512 — Load Productive Wage Share (V*/W).

Book-period (1948-1989): Book Table 5.7 (digitized as Table5_7_KeyRatios.csv),
column `T512A` (book values). V*/W is the share of total wage bill paid to
productive labor.

Extension (1998-2024): BEA NIPA Table 6.2D compensation of employees by
industry. We sum compensation across the productive sectors per the EPR
methodology (Appendix C concordance adapted to NAICS: Farms + Mining +
Utilities + Construction + Manufacturing + Transportation & warehousing) and
divide by line 1 (Compensation of employees, total).

NOTE: 1990-1997 is a coverage gap (book ends 1989; BEA 6.2D starts 1998).
P02 handles the level-splice at the 1998 anchor.

The S511 (Lp/L) and S512 (V*/W) series are the two key ratios from Table 5.7
that drive most of the chapter's interpretive arguments and feed downstream
extension formulas (e.g., S506 extension uses e = 1.238/(V*/W) - 1).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.bea_cache import load_bea_line, load_bea_line_summed  # noqa: E402
from utils.paths import BOOK_TABLES  # noqa: E402
from utils.series import BookColumnLoader  # noqa: E402


# Book-period loader (S512-A, 1948-1989).
LOADER = BookColumnLoader(
    series_id     = "S512",
    subseries_id  = "S512-A",
    source_file   = BOOK_TABLES / "Table5_7_KeyRatios.csv",
    source_column = "T512A",
    units         = "share",
)


# NAICS productive-sector line numbers in BEA NIPA Table 6.2D.
# Per EPR conceptual_continuity, Appendix C must be rewritten for NAICS; this
# is the standard mapping used elsewhere in the project (matches the productive
# industries listed in S&T 1994 Ch.5: agriculture, mining, construction,
# transportation and public utilities, manufacturing).
PRODUCTIVE_LINES_6_2D = [
    5,   # Farms (Agriculture, forestry, fishing & hunting → farms only; forestry/fishing line 6 is small and split with services)
    7,   # Mining (header) — but it's an aggregate; we use the sub-detail to avoid double-counting; line 7 itself is the Mining total
    11,  # Utilities
    12,  # Construction
    13,  # Manufacturing (header; sums to durable+nondurable goods)
    43,  # Transportation and warehousing (header total)
]


def load_extension_components() -> dict[str, pd.DataFrame]:
    """Load the two BEA NIPA tables needed for the V*/W extension.

    Returns dict with keys:
      - 'compensation_total': line 1 (Compensation of employees), in millions
      - 'compensation_productive': sum across productive sector lines, in millions
    """
    table_6_2D = "nipa_6_2D_compensation_by_industry.csv"
    total = load_bea_line(table_6_2D, line_number=1)
    productive = load_bea_line_summed(table_6_2D, line_numbers=PRODUCTIVE_LINES_6_2D)
    return {
        "compensation_total":      total,
        "compensation_productive": productive,
    }


def run():
    df = LOADER.load()
    print(f"    [L01_S512] book loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    try:
        ext = load_extension_components()
        comp_tot = ext["compensation_total"]
        comp_p   = ext["compensation_productive"]
        print(f"    [L01_S512] BEA 6.2D extension components: total {len(comp_tot)} rows "
              f"({comp_tot['year'].min()}-{comp_tot['year'].max()}); "
              f"productive sum {len(comp_p)} rows")
    except Exception as exc:
        print(f"    [L01_S512] WARNING: extension components unavailable: {exc}")
    return df


if __name__ == "__main__":
    run()
