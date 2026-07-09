"""L01_S517 — Load K* (Productive Constant Capital Stock).

Source: BEA Fixed Assets Table 4.1 (ported from predecessor-build cache), Line 1
"Private nonresidential fixed assets". Period 1925-2024.

**Productive partition note**: Line 1 is total private nonresidential fixed
assets — includes both productive (manufacturing, agriculture, transport,
utilities, trade-related infrastructure under S&T's broad classification)
and a small unproductive component (some financial-sector real estate).
For a first-pass K* this approximation is standard. A concordance-based
refinement (per IMPLEMENTATION_PLAN.md Phase 2.A) would subtract Line 33
(Financial sector) — about 5-10% of the total. The DPR documents this
choice; current build uses Line 1 unmodified.

Units: native cache is millions; loader divides by 1000 for billions USD.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.bea_cache import load_bea_line  # noqa: E402


SERIES_ID = "S517"
SUBSERIES = "S517-A"

# Book-period GROSS K* variant (F2, 2026-07-07). The book's Table 5.8 K* = C*_f is
# fixed nonresidential GROSS private capital (current $, "BEA 1987" vintage), which
# the primary S517-A (BEA FA 4.1 NET) runs ~21.8% below (DIV-058). The gross panel
# is already in the tree and reproduces the book's own r*/r*' to MAE ~0.0025 (F2).
# Book period ONLY (1948-1989); current-$ gross is genuinely non-constructible
# 1990-> (BEA discontinued current-cost gross at the 1997 revision) -> no extension.
GROSS_PANEL = (
    Path(__file__).resolve().parents[2]
    / "data" / "source" / "book_tables" / "_panel_Kstar_gross_1948_1989.csv"
)
GROSS_SUBSERIES = "S517-GROSS-A"


def load() -> pd.DataFrame:
    df = load_bea_line("fixed_assets_4_1_net_stock.csv", line_number=1)
    df["value"] = df["value"] / 1000.0  # millions -> billions
    df["series_id"] = SUBSERIES
    df["units"] = "billions_usd"
    return df[["series_id", "year", "value", "units"]]


def load_gross_book() -> pd.DataFrame:
    """Book-period GROSS K* (book Table 5.8 C*_f), current $bn, 1948-1989 only.

    Source: data/source/book_tables/_panel_Kstar_gross_1948_1989.csv (the book's
    own Table 5.8 gross K* row; verified vs KB v2 _combined/5.8.csv by F1b). No
    synthetic extension beyond 1989 (BEA current-$ gross discontinued at 1997).
    """
    df = pd.read_csv(GROSS_PANEL, comment="#")
    df = df.rename(columns={"K_star_gross": "value"})
    df["series_id"] = GROSS_SUBSERIES
    df["units"] = "billions_usd"
    return df[["series_id", "year", "value", "units"]].sort_values("year").reset_index(drop=True)


def run():
    df = load()
    print(f"    [L01_S517] loaded {len(df)} rows; period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.1f}B, last={df.iloc[-1]['value']:.1f}B")
    return df


if __name__ == "__main__":
    run()
