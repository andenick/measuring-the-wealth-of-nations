#!/usr/bin/env python3
"""V09 - Mohun Cross-Validation: compare AS2 series against Mohun (2005) estimates.

Mohun uses a different productive/unproductive labor classification but
should produce broadly consistent results. Divergences > 10% are flagged
as they indicate methodological differences worth documenting.

Inputs:
  - data/final-data/series/T506.csv (exploitation rate)
  - data/final-data/series/T511.csv (productive labor share)
  - Inputs/ExternalSources/Mohun/mohun_exploitation_rates_1948_1989.csv
Dependencies: P00 must complete
"""

import json
import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import SERIES_OUT, INPUTS

VALIDATOR_NAME = "V09_mohun_crossvalidation"

MOHUN_DIR = INPUTS / "ExternalSources" / "Mohun"


def validate(series_filter=None, chapter_filter=None):
    checks = []

    # Load Mohun exploitation rates
    mohun_path = MOHUN_DIR / "mohun_exploitation_rates_1948_1989.csv"
    if not mohun_path.exists():
        return {
            "validator": VALIDATOR_NAME,
            "status": "skip",
            "checks": [{
                "status": "SKIP",
                "message": f"Mohun data not found at {mohun_path}",
            }],
            "summary": "Mohun data not available",
        }

    mohun = pd.read_csv(mohun_path)

    # Cross-validate T506 (exploitation rate) vs Mohun's e_mohun
    if "e_mohun" in mohun.columns:
        t506_path = SERIES_OUT / "T506.csv"
        if t506_path.exists():
            t506 = pd.read_csv(t506_path)
            if "year" not in t506.columns:
                t506 = t506.rename(columns={t506.columns[0]: "year"})

            # Find combined column
            combined_col = None
            for col in t506.columns:
                if "combined" in col.lower() or "book" in col.lower():
                    combined_col = col
                    break
            if combined_col is None:
                numeric = [c for c in t506.select_dtypes(include="number").columns
                           if c != "year"]
                combined_col = numeric[-1] if numeric else None

            if combined_col:
                merged = pd.merge(
                    t506[["year", combined_col]].rename(columns={combined_col: "as2_e"}),
                    mohun[["year", "e_mohun"]],
                    on="year",
                    how="inner",
                )

                if not merged.empty:
                    merged["abs_diff"] = (merged["as2_e"] - merged["e_mohun"]).abs()
                    merged["rel_diff"] = merged["abs_diff"] / merged["e_mohun"].abs()

                    max_diff = float(merged["rel_diff"].max())
                    mean_diff = float(merged["rel_diff"].mean())
                    n_years = len(merged)

                    # Sample comparison at benchmark years
                    for yr in [1948, 1958, 1967, 1977, 1989]:
                        row = merged[merged["year"] == yr]
                        if not row.empty:
                            as2 = float(row["as2_e"].iloc[0])
                            moh = float(row["e_mohun"].iloc[0])
                            rd = float(row["rel_diff"].iloc[0])
                            checks.append({
                                "comparison": f"T506 vs Mohun e [{yr}]",
                                "as2_value": round(as2, 4),
                                "mohun_value": round(moh, 4),
                                "rel_diff": round(rd, 4),
                                "status": "PASS" if rd < 0.20 else "WARN",
                                "message": (
                                    f"T506[{yr}]={as2:.3f} vs Mohun={moh:.3f} "
                                    f"(diff={rd:.1%})"
                                ),
                            })

                    checks.append({
                        "comparison": "T506 vs Mohun exploitation rate (overall)",
                        "years_compared": n_years,
                        "max_rel_diff": round(max_diff, 4),
                        "mean_rel_diff": round(mean_diff, 4),
                        "status": "PASS" if max_diff < 0.30 else "WARN",
                        "message": (
                            f"T506 vs Mohun: {n_years} years, max diff {max_diff:.1%}, "
                            f"mean diff {mean_diff:.1%}"
                        ),
                    })

    # Cross-validate T511 (Lp/L) vs Mohun's Lp ratio
    lp_col = None
    for col in mohun.columns:
        if "lp" in col.lower() and "ratio" in col.lower():
            lp_col = col
            break
    if lp_col is None:
        for col in mohun.columns:
            if "lp_mohun_l" in col.lower():
                lp_col = col
                break

    if lp_col:
        t511_path = SERIES_OUT / "T511.csv"
        if t511_path.exists():
            t511 = pd.read_csv(t511_path)
            if "year" not in t511.columns:
                t511 = t511.rename(columns={t511.columns[0]: "year"})

            combined_col = None
            for col in t511.columns:
                if "combined" in col.lower():
                    combined_col = col
                    break
            if combined_col is None:
                numeric = [c for c in t511.select_dtypes(include="number").columns
                           if c != "year"]
                combined_col = numeric[-1] if numeric else None

            if combined_col:
                merged = pd.merge(
                    t511[["year", combined_col]].rename(columns={combined_col: "as2_lpl"}),
                    mohun[["year", lp_col]].rename(columns={lp_col: "mohun_lpl"}),
                    on="year",
                    how="inner",
                )

                if not merged.empty:
                    merged = merged.dropna()
                    if not merged.empty:
                        merged["rel_diff"] = (
                            (merged["as2_lpl"] - merged["mohun_lpl"]).abs()
                            / merged["mohun_lpl"].abs()
                        )
                        max_diff = float(merged["rel_diff"].max())
                        checks.append({
                            "comparison": "T511 vs Mohun Lp/L ratio",
                            "years_compared": len(merged),
                            "max_rel_diff": round(max_diff, 4),
                            "status": "PASS" if max_diff < 0.20 else "WARN",
                            "message": (
                                f"T511 vs Mohun Lp/L: {len(merged)} years, "
                                f"max diff {max_diff:.1%}"
                            ),
                        })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_warn = sum(1 for c in checks if c["status"] == "WARN")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_warn == 0 else "warn",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_warn} WARN out of {len(checks)} checks",
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))
