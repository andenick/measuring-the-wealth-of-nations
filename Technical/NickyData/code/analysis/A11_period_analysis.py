#!/usr/bin/env python3
"""A11 - Period Analysis: compute mean Marxian variables by canonical economic period.

Produces summary tables showing how e, r*, TP*/GDP evolve across distinct
macroeconomic eras (Golden Age, Stagflation, Reagan, etc.).

Inputs:  final-data/series/T506.csv, T513.csv (exploitation rate, profit rate)
         raw-data/parsed/integrated_tp_series.csv (from L19)
Outputs: outputs/analysis/period_analysis.csv
         outputs/analysis/structural_findings.json
Dependencies: P04 (T506), P08 (T513), L19 (integrated TP)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, ensure_dirs

PRIORITY = 11

PERIODS = [
    ("Golden Age", 1948, 1973),
    ("Stagflation", 1973, 1980),
    ("Reagan Era", 1980, 1989),
    ("Transition", 1990, 1996),
    ("Clinton-Bush", 1997, 2007),
    ("GFC+Recovery", 2008, 2015),
    ("Late Expansion", 2016, 2019),
    ("COVID+Post", 2020, 2024),
]


def _load_combined(series_id: str) -> pd.Series:
    csv_path = SERIES_OUT / f"{series_id}.csv"
    if not csv_path.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(csv_path, index_col=0)
    if "combined" in df.columns:
        return df["combined"].dropna()
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        return numeric.iloc[:, -1].dropna()
    return pd.Series(dtype=float)


def run():
    """Compute period analysis and structural findings."""
    ensure_dirs()

    e = _load_combined("T506")
    r = _load_combined("T513")

    integ_path = PARSED_RAW / "integrated_tp_series.csv"
    integ = pd.DataFrame()
    if integ_path.exists():
        integ = pd.read_csv(integ_path, index_col="year")

    rows = []
    print(f"    {'Period':<18} {'Years':<10} {'e_start':>8} {'e_end':>7} {'e_mean':>7} "
          f"{'r_mean':>7} {'TP/GDP':>7}")
    print(f"    {'-'*18} {'-'*10} {'-'*8} {'-'*7} {'-'*7} {'-'*7} {'-'*7}")

    for name, start, end in PERIODS:
        e_sub = e.loc[start:end] if not e.empty else pd.Series(dtype=float)
        r_sub = r.loc[start:end] if not r.empty else pd.Series(dtype=float)
        tp_gdp = (integ.loc[start:end, "tp_gdp_ratio"]
                  if not integ.empty and "tp_gdp_ratio" in integ.columns
                  else pd.Series(dtype=float))

        e_start_val = float(e_sub.iloc[0]) if len(e_sub) > 0 else np.nan
        e_end_val = float(e_sub.iloc[-1]) if len(e_sub) > 0 else np.nan
        e_mean = float(e_sub.mean()) if len(e_sub) > 0 else np.nan
        r_mean = float(r_sub.mean()) if len(r_sub) > 0 else np.nan
        tp_mean = float(tp_gdp.mean()) if len(tp_gdp) > 0 else np.nan

        rows.append({
            "period": name, "start_year": start, "end_year": end,
            "e_start": e_start_val, "e_end": e_end_val, "e_mean": e_mean,
            "e_change": e_end_val - e_start_val if not np.isnan(e_start_val) else np.nan,
            "r_mean": r_mean, "tp_gdp_mean": tp_mean,
        })

        yr_str = f"{start}-{end}"
        print(f"    {name:<18} {yr_str:<10} {e_start_val:>8.3f} {e_end_val:>7.3f} "
              f"{e_mean:>7.3f} {r_mean:>7.3f} {tp_mean:>7.3f}")

    if len(e) > 0:
        e_peak_yr = int(e.idxmax())
        print(f"\n    Peak e: {e.max():.2f} in {e_peak_yr}")
        print(f"    Current e: {e.iloc[-1]:.2f} ({int(e.index[-1])})")

    # Save
    out_dir = Path(__file__).resolve().parent.parent.parent / "outputs" / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)

    period_df = pd.DataFrame(rows)
    csv_path = out_dir / "period_analysis.csv"
    period_df.to_csv(csv_path, index=False)
    print(f"    [A11] Saved {csv_path}")

    findings = {
        "exploitation_rate": {
            "book_period": {"start": float(e.get(1948, 0)), "end": float(e.get(1989, 0)), "direction": "RISING"},
            "extension": {"start": float(e.get(1997, 0)), "end": float(e.get(2024, e.iloc[-1] if len(e) else 0)),
                          "direction": "DECLINING"},
        },
        "structural_shift": {
            "tp_gdp_1948": float(integ.loc[1948, "tp_gdp_ratio"]) if 1948 in integ.index else None,
            "tp_gdp_2024": float(integ.loc[2024, "tp_gdp_ratio"]) if 2024 in integ.index else None,
            "finding": "TP*/GDP crossed below 1.0 — unproductive sector now generates more measured output",
        },
        "profit_rate": {
            "r_1948": float(r.get(1948, 0)), "r_2024": float(r.get(2024, 0)),
            "direction": "DECLINING (secular)",
        },
    }
    json_path = out_dir / "structural_findings.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)

    return {
        "series_id": "A11",
        "status": "ok",
        "summary": f"Period analysis: {len(rows)} periods, e peak {e.max():.2f}" if len(e) > 0 else "No data",
        "outputs": [str(csv_path), str(json_path)],
    }
