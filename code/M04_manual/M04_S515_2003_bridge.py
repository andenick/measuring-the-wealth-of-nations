"""M04_S515 — BLS CES 2003 Overhaul Bridge Application (per-series wrapper).

Post-D2 (REVIEW_2026-07 seam redesign): the PUBLISHED S515-EXT is now
Lp = S511 share × book-anchored total-employment L (share×total), so the raw
per-sector 2003 bridge applies conceptually to (a) the S511 super-sector share
and (b) the retained honest raw arm S515-EXT-CONSTRUCTIBLE, which still is the
direct sum of production-worker counts across the productive super-sectors:

  Lp_constructible = CES1000000006 + CES2000000006 + CES3000000006
       (mining/logging + construction + manufacturing, production workers)

As a level (not ratio) series, that raw count is fully exposed to the 2003
overhaul: any per-sector factor passes through additively to the sum. The 2003
CES overhaul is the employment-side vintage divergence DIV-010.

v1.1 applies a documented null bridge (factor=1.0 per sector ⇒ no level
change). Wiring in place for v1.2 when per-sector factors can be
sourced from the BLS Employment Situation archive.

See M04_bls_ces_2003_bridge.py for the master rationale.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL, ROOT  # noqa: E402

SERIES_ID = "S515"
BRIDGE_YEAR = 2003
FACTORS_JSON = ROOT / "data" / "adjusted-final-data" / "bls_ces_2003_bridge_factors.json"
RELEVANT_CES = [
    "CES1000000006",  # mining/logging PW
    "CES2000000006",  # construction PW
    "CES3000000006",  # manufacturing PW
]


def load_factors() -> dict:
    if not FACTORS_JSON.exists():
        raise FileNotFoundError(
            f"Bridge factors not found at {FACTORS_JSON}. "
            f"Run M04_bls_ces_2003_bridge.py first."
        )
    return json.loads(FACTORS_JSON.read_text(encoding="utf-8"))


def apply_bridge_to_sum(
    components: dict[str, pd.Series], factors: dict[str, float],
) -> pd.Series:
    """For each component series, multiply post-2003 values by per-sector
    factor, then sum. In v1.1 all factors == 1.0 ⇒ identity sum.
    """
    out = None
    for ces_id, s in components.items():
        f = factors[ces_id]
        adjusted = s.copy()
        adjusted.loc[adjusted.index >= BRIDGE_YEAR] = (
            adjusted.loc[adjusted.index >= BRIDGE_YEAR] * f
        )
        out = adjusted if out is None else out.add(adjusted, fill_value=0.0)
    return out


def verify() -> dict:
    payload = load_factors()
    factors_for_series = {
        k: v for k, v in payload["factors"].items() if k in RELEVANT_CES
    }
    assert factors_for_series, f"No relevant CES factors found for {SERIES_ID}"

    csv_path = DATA_FINAL / f"{SERIES_ID}.csv"
    n_post_2003 = None
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        ext = df[df["series_id"] == f"{SERIES_ID}-EXT"]
        if not ext.empty:
            n_post_2003 = int((ext["year"] >= BRIDGE_YEAR).sum())

    summary = {
        "series_id": SERIES_ID,
        "bridge_year": BRIDGE_YEAR,
        "relevant_ces_series": RELEVANT_CES,
        "factors": {k: v["bridge_factor_post_2003"] for k, v in factors_for_series.items()},
        "bridge_is_null_v1_1": all(
            v["bridge_factor_post_2003"] == 1.0 for v in factors_for_series.values()
        ),
        "ext_rows_post_2003_on_disk": n_post_2003,
        "v1_3_followup": payload.get("v1_3_followup", payload.get("v1_2_followup", "n/a")),
    }
    print(f"[M04_{SERIES_ID}_2003_bridge] factors: {summary['factors']}")
    print(
        f"[M04_{SERIES_ID}_2003_bridge] null_bridge={summary['bridge_is_null_v1_1']}; "
        f"ext rows >=2003: {n_post_2003}"
    )
    return summary


if __name__ == "__main__":
    verify()
