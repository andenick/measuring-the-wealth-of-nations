"""L01_S517 — Load K* (Productive Constant Capital Stock).

Source: BEA Fixed Assets Table 4.1 (ported from ST2 cache), Line 1
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


def load() -> pd.DataFrame:
    df = load_bea_line("fixed_assets_4_1_net_stock.csv", line_number=1)
    df["value"] = df["value"] / 1000.0  # millions -> billions
    df["series_id"] = SUBSERIES
    df["units"] = "billions_usd"
    return df[["series_id", "year", "value", "units"]]


def run():
    df = load()
    print(f"    [L01_S517] loaded {len(df)} rows; period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.1f}B, last={df.iloc[-1]['value']:.1f}B")
    return df


if __name__ == "__main__":
    run()
