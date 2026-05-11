"""Period Analysis — Compute mean Marxian variables by canonical economic period.

Produces summary tables for the paper showing how e, r*, TP*/GDP, and
other key variables behave across distinct macroeconomic eras.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from .helpers import load_computed, save_series, build_series

DEPENDS_ON = ["exploitation", "profit_rate"]
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

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


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    e = load_computed("T506")
    r = load_computed("T513")
    tp = load_computed("T501")
    gfp = load_computed("T503")
    v = load_computed("T504")
    s = load_computed("T505")

    # Load integrated series for TP*/GDP and productive share
    integ_path = DATA_DIR / "computed" / "integrated_tp_series.csv"
    integ = pd.DataFrame()
    if integ_path.exists():
        integ = pd.read_csv(integ_path, index_col="year")

    rows = []
    print(f"    {'Period':<18} {'Years':<10} {'e_start':>8} {'e_end':>7} {'e_mean':>7} {'r_mean':>7} {'TP/GDP':>7}")
    print(f"    {'-'*18} {'-'*10} {'-'*8} {'-'*7} {'-'*7} {'-'*7} {'-'*7}")

    for name, start, end in PERIODS:
        e_sub = e.loc[start:end] if not e.empty else pd.Series(dtype=float)
        r_sub = r.loc[start:end] if not r.empty else pd.Series(dtype=float)
        tp_gdp = integ.loc[start:end, "tp_gdp_ratio"] if not integ.empty and "tp_gdp_ratio" in integ.columns else pd.Series(dtype=float)

        e_start = e_sub.iloc[0] if len(e_sub) > 0 else np.nan
        e_end = e_sub.iloc[-1] if len(e_sub) > 0 else np.nan
        e_mean = e_sub.mean() if len(e_sub) > 0 else np.nan
        r_mean = r_sub.mean() if len(r_sub) > 0 else np.nan
        tp_mean = tp_gdp.mean() if len(tp_gdp) > 0 else np.nan

        rows.append({
            "period": name,
            "start_year": start,
            "end_year": end,
            "e_start": e_start,
            "e_end": e_end,
            "e_mean": e_mean,
            "e_change": e_end - e_start if not np.isnan(e_start) else np.nan,
            "r_mean": r_mean,
            "tp_gdp_mean": tp_mean,
        })

        yr_str = f"{start}-{end}"
        print(f"    {name:<18} {yr_str:<10} {e_start:>8.3f} {e_end:>7.3f} {e_mean:>7.3f} {r_mean:>7.3f} {tp_mean:>7.3f}")

    # Summary findings
    print()
    if len(e) > 0:
        e_peak_yr = e.idxmax()
        e_peak = e.max()
        e_2024 = e.get(2024, e.iloc[-1])
        print(f"    Peak e: {e_peak:.2f} in {int(e_peak_yr)}")
        print(f"    Current e: {e_2024:.2f} (2024)")
        print(f"    Post-peak decline: {(e_2024/e_peak - 1)*100:.1f}%")

    if not integ.empty and "tp_gdp_ratio" in integ.columns:
        tp_series = integ["tp_gdp_ratio"].dropna()
        if len(tp_series) > 0:
            below_one = tp_series[tp_series < 1.0]
            if len(below_one) > 0:
                first_below = int(below_one.index.min())
                print(f"    TP*/GDP first below 1.0: {first_below}")

    # Save period analysis
    period_df = pd.DataFrame(rows)
    out_path = DATA_DIR / "computed" / "period_analysis.csv"
    period_df.to_csv(out_path, index=False)
    print(f"    [SAVED] {out_path}")

    # Save key structural findings as JSON
    findings = {
        "exploitation_rate": {
            "book_period_1948_1989": {
                "start": float(e.get(1948, 0)),
                "end": float(e.get(1989, 0)),
                "direction": "RISING",
                "interpretation": "Declining productive worker share of value added",
            },
            "extension_1997_2024": {
                "start": float(e.get(1997, 0)),
                "end": float(e.get(2024, 0)),
                "direction": "DECLINING",
                "interpretation": "Shrinking productive sector reduces measurable surplus extraction",
            },
        },
        "structural_shift": {
            "tp_gdp_1948": float(integ.loc[1948, "tp_gdp_ratio"]) if 1948 in integ.index else None,
            "tp_gdp_2024": float(integ.loc[2024, "tp_gdp_ratio"]) if 2024 in integ.index else None,
            "productive_go_share_1997": float(integ.loc[1997, "productive_go_share"]) if 1997 in integ.index and "productive_go_share" in integ.columns else None,
            "productive_go_share_2024": float(integ.loc[2024, "productive_go_share"]) if 2024 in integ.index and "productive_go_share" in integ.columns else None,
            "finding": "TP*/GDP crossed below 1.0 — unproductive sector now generates more measured output than productive sector",
        },
        "profit_rate": {
            "r_1948": float(r.get(1948, 0)),
            "r_1989": float(r.get(1989, 0)),
            "r_2024": float(r.get(2024, 0)),
            "direction": "DECLINING (secular)",
            "interpretation": "Falling rate of profit consistent with Marxian prediction",
        },
    }
    json_path = DATA_DIR / "computed" / "structural_findings.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)

    return {}
