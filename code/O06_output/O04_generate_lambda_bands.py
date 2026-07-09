"""O04 -- Generate DIV-042 uncertainty-band sidecars for the Ch7 labor-value series.

Emits `data/final/S701_LAMBDA_BAND.csv` and `data/final/S702_LAMBDA_BAND.csv`,
one row per published (COMBINED) benchmark/extension year:

    year, central, lo, hi, basis

The band is the DIV-042 worst-case (common-mode) X_j error propagated through the
published lambda computation. lambda ~ 1/X, so a systematic +/-11.5% error in the
recovered per-sector gross output X_j maps ASYMMETRICALLY to lambda:

    lo = central / (1 + 0.115)   # X high  -> lambda low   (-10.3%)
    hi = central / (1 - 0.115)   # X low   -> lambda high  (+13.0%)

This reproduces F3's `worstcase_lo_Xplus` / `worstcase_hi_Xminus` columns
(F3_lambda_sensitivity_aggregate.csv, 2026-07-07) and is the honest worst case;
the independent-error Monte-Carlo half-widths are tighter (S701 ~+/-3-4%,
S702 ~+/-6-9%) but the worst-case common-mode bound is what DIV-042 documents.
Pattern mirrors data/final/S506_KIO_BAND.csv.

`central` and `lo`/`hi` are reported at the same 3-significant-figure published
precision as the rounded final CSV (P02 emit), so the sidecar is internally
consistent with chopped/S70x.csv.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402

X_BOUND = 0.115           # DIV-042 median per-sector X_j error (~11.5%)
SIG = 3                   # published significant figures
SERIES = ["S701", "S702"]
BASIS = "DIV-042 worst-case common-mode X_j +/-11.5% (lo=central/1.115, hi=central/0.885)"


def _round_sig(x: float, sig: int = SIG) -> float:
    if x is None or not math.isfinite(x) or x == 0.0:
        return x
    return round(x, -int(math.floor(math.log10(abs(x)))) + (sig - 1))


def band_for(sid: str) -> Path | None:
    final_csv = DATA_FINAL / f"{sid}.csv"
    if not final_csv.exists():
        return None
    df = pd.read_csv(final_csv)
    pub = (df[df["series_id"] == f"{sid}-COMBINED"]
           .dropna(subset=["value"])
           .sort_values("year"))
    out_path = DATA_FINAL / f"{sid}_LAMBDA_BAND.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "central", "lo", "hi", "basis"])
        for _, row in pub.iterrows():
            central = float(row["value"])           # already 3-sig-fig from P02 emit
            lo = _round_sig(central / (1.0 + X_BOUND))
            hi = _round_sig(central / (1.0 - X_BOUND))
            w.writerow([int(row["year"]), central, lo, hi, BASIS])
    return out_path


def run() -> dict:
    written = []
    for sid in SERIES:
        p = band_for(sid)
        if p is not None:
            written.append(p.name)
    print(f"    [O04] lambda-band sidecars: wrote {len(written)} ({', '.join(written)})")
    return {"written": written}


if __name__ == "__main__":
    run()
