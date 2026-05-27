"""M04_S504 — BLS CES 2003 Overhaul Bridge Application (per-series wrapper).

Reads bridge factors from
  data/adjusted-final-data/bls_ces_2003_bridge_factors.json
and verifies that the wiring is in place to apply per-sector factors to
S504-EXT post-2003 values.

S504 (Variable Capital V*) depends on BLS CES production-worker counts
indirectly (through the productive-wages share used in the splice).
The relevant CES super-sectors are CES0500000006 (total private production
workers) and CES0600000006 (goods-producing production workers).

In v1.1 the bridge is a documented null (factor=1.0 per sector) — see
M04_bls_ces_2003_bridge.py for the rationale (cached BLS API series is
post-overhaul back-revised vintage, so deriving a factor from it would
double-count cyclical decline as a methodology shift). This script
exists to make the v1.2 plug-in point unambiguous and to assert that the
factors JSON is present and parseable.

VERIFICATION (executable):
  python Technical/code/M04_manual/M04_S504_2003_bridge.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL, ROOT  # noqa: E402

SERIES_ID = "S504"
BRIDGE_YEAR = 2003
FACTORS_JSON = ROOT / "data" / "adjusted-final-data" / "bls_ces_2003_bridge_factors.json"
# CES super-sectors that feed S504 (productive-wages share construction).
RELEVANT_CES = ["CES0500000006", "CES0600000006"]


def load_factors() -> dict:
    if not FACTORS_JSON.exists():
        raise FileNotFoundError(
            f"Bridge factors not found at {FACTORS_JSON}. "
            f"Run M04_bls_ces_2003_bridge.py first."
        )
    return json.loads(FACTORS_JSON.read_text(encoding="utf-8"))


def apply_bridge(extension_df: pd.DataFrame, value_col: str, factor: float) -> pd.DataFrame:
    """Multiplicative bridge applied to all rows with year >= BRIDGE_YEAR.

    In v1.1, factor == 1.0 ⇒ identity transform. Wired for v1.2.
    """
    out = extension_df.copy()
    mask = out["year"] >= BRIDGE_YEAR
    out.loc[mask, value_col] = out.loc[mask, value_col] * factor
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
        f"ext rows on disk >=2003: {n_post_2003}"
    )
    return summary


if __name__ == "__main__":
    verify()
