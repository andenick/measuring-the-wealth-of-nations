#!/usr/bin/env python3
"""V10 - IO Matrix Consistency: validate NAICS Input-Output matrices.

Checks for each benchmark year (1997-2017):
  - A-matrix column sums < 1
  - Leontief inverse elements >= 0
  - Leontief diagonal >= 1
  - Sector classification coverage
  - Labor values all positive

Inputs:
  - Inputs/IO_Matrices/NAICS/*.json
  - data/final-data/series/T701_labor_values_summary.json
Dependencies: NAICS IO files must exist
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import INPUTS

VALIDATOR_NAME = "V10_io_consistency"
NAICS_DIR = INPUTS / "IO_Matrices" / "NAICS"
BENCHMARK_YEARS = [1997, 2002, 2007, 2012, 2017]


def validate(series_filter=None, chapter_filter=None):
    checks = []

    if not NAICS_DIR.exists():
        return {
            "validator": VALIDATOR_NAME,
            "status": "skip",
            "checks": [{"status": "SKIP", "message": "NAICS IO directory not found"}],
            "summary": "No NAICS IO data",
        }

    try:
        from utils.io.naics_parser import extract_use_matrix, extract_leontief, compute_technical_coefficients_naics
        from utils.io.naics_classification import classify_naics_sectors, get_productive_sector_codes
    except ImportError as e:
        return {
            "validator": VALIDATOR_NAME,
            "status": "skip",
            "checks": [{"status": "SKIP", "message": f"Import error: {e}"}],
            "summary": "Cannot import NAICS modules",
        }

    for year in BENCHMARK_YEARS:
        use_path = NAICS_DIR / f"Use_of_Commodities_Summary_{year}.json"
        leontief_path = NAICS_DIR / f"Total_Requirements_IxI_Summary_{year}.json"

        if not use_path.exists() or not leontief_path.exists():
            checks.append({
                "year": year,
                "status": "SKIP",
                "message": f"{year}: IO files not found",
            })
            continue

        # Load matrices
        try:
            use = extract_use_matrix(use_path)
            B = extract_leontief(leontief_path)
            A = compute_technical_coefficients_naics(use)
        except Exception as e:
            checks.append({
                "year": year,
                "status": "FAIL",
                "message": f"{year}: parse error — {e}",
            })
            continue

        # Check 1: A-matrix column sums < 1
        col_sums = A.sum(axis=0)
        max_col_sum = float(col_sums.max())
        col_sum_ok = max_col_sum < 1.0
        checks.append({
            "year": year,
            "check": "A-matrix column sums < 1",
            "max_col_sum": round(max_col_sum, 4),
            "status": "PASS" if col_sum_ok else "WARN",
            "message": f"{year}: max A column sum = {max_col_sum:.4f} ({'<1' if col_sum_ok else '>=1'})",
        })

        # Check 2: Leontief elements >= 0
        min_element = float(B.values.min())
        neg_count = int((B.values < 0).sum())
        checks.append({
            "year": year,
            "check": "Leontief elements >= 0",
            "min_element": round(min_element, 6),
            "negative_count": neg_count,
            "status": "PASS" if neg_count == 0 else "WARN",
            "message": f"{year}: Leontief min={min_element:.6f}, {neg_count} negative elements",
        })

        # Check 3: Leontief diagonal >= 1
        common = B.index.intersection(B.columns)
        if len(common) > 0:
            diag = pd.Series([B.loc[c, c] for c in common], index=common)
            min_diag = float(diag.min())
            checks.append({
                "year": year,
                "check": "Leontief diagonal >= 1",
                "min_diagonal": round(min_diag, 4),
                "status": "PASS" if min_diag >= 1.0 else "WARN",
                "message": f"{year}: min diagonal = {min_diag:.4f}",
            })

        # Check 4: Sector classification coverage
        io_codes = list(use.index)
        groups = classify_naics_sectors(io_codes)
        unclassified = groups.get("unclassified", [])
        checks.append({
            "year": year,
            "check": "Sector classification coverage",
            "total_sectors": len(io_codes),
            "unclassified": len(unclassified),
            "status": "PASS" if len(unclassified) == 0 else "WARN",
            "message": f"{year}: {len(io_codes)} sectors, {len(unclassified)} unclassified",
        })

    # Check 5: IO coefficient stability across benchmark years
    prev_max_eigen = None
    prev_year = None
    for year in BENCHMARK_YEARS:
        use_path = NAICS_DIR / f"Use_of_Commodities_Summary_{year}.json"
        if not use_path.exists():
            continue
        try:
            use = extract_use_matrix(use_path)
            A = compute_technical_coefficients_naics(use)
            col_sums = A.sum(axis=0)
            max_col = float(col_sums.max())

            # Productive sector share of total intermediate flows
            prod_codes = [c for c in get_productive_sector_codes() if c in A.columns]
            prod_share = float(A[prod_codes].sum().sum() / A.sum().sum()) if A.sum().sum() > 0 else 0

            if prev_max_eigen is not None:
                change = abs(max_col - prev_max_eigen) / prev_max_eigen if prev_max_eigen > 0 else 0
                checks.append({
                    "year": year,
                    "check": f"A-matrix stability {prev_year}->{year}",
                    "max_col_sum_change": round(change, 4),
                    "status": "PASS" if change < 0.50 else "WARN",
                    "message": f"{prev_year}->{year}: max col sum change {change:.1%}",
                })

            checks.append({
                "year": year,
                "check": "Productive sector share",
                "productive_share": round(prod_share, 4),
                "status": "PASS" if 0.30 <= prod_share <= 0.85 else "WARN",
                "message": f"{year}: productive share of intermediates = {prod_share:.1%}",
            })

            prev_max_eigen = max_col
            prev_year = year
        except Exception:
            pass

    # Check 6: Labor values all positive (from T701 summary)
    lv_path = Path(__file__).resolve().parent.parent.parent / "data" / "final-data" / "series" / "T701_labor_values_summary.json"
    if lv_path.exists():
        with open(lv_path) as f:
            lv_data = json.load(f)
        for yr_str, vals in lv_data.items():
            checks.append({
                "year": int(yr_str),
                "check": "Labor values positive",
                "all_positive": vals.get("all_positive", False),
                "mean_lambda": vals.get("mean_lambda"),
                "status": "PASS" if vals.get("all_positive") else "FAIL",
                "message": f"{yr_str}: lambda* mean={vals.get('mean_lambda', '?'):.6f}, all_positive={vals.get('all_positive')}",
            })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_warn = sum(1 for c in checks if c["status"] == "WARN")
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_fail == 0 else "fail",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_fail} FAIL, {n_warn} WARN out of {len(checks)} checks",
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))
