#!/usr/bin/env python3
"""A06 - Labor Value vs Price of Production: IO-based computation.

Computes prices of production using the CORRECT formula from the book:
  c_j_labor = sum_i(lambda*_i * a_ij)  (labor value of constant capital via A-matrix)
  pp*_j = (c_j_labor + v_j_labor) * (1 + r_bar) / go_j_labor

This differs from the previous attempt which used a simple markup formula.
The key insight: constant capital c_j must be computed from the A-matrix
and labor values, not from money compensation alone.

Expected: R² > 0.90, slope ≈ 1.0 (per book Section 4.2, pp.86-88)

Outputs: outputs/analysis/labor_value_price_deviations.json
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import INPUTS, ANALYSIS_OUT
from utils.io.naics_parser import extract_use_matrix, extract_leontief, get_sector_descriptions, compute_technical_coefficients_naics
from utils.io.naics_classification import get_productive_sector_codes

NAICS_DIR = INPUTS / "IO_Matrices" / "NAICS"
KLEMS_DIR = Path("D:/Arcanum/Council/Robin/DATA/SHAIKH_TONAK/TECHNICAL_DATA/data/modern/klems_processed")


def generate():
    ANALYSIS_OUT.mkdir(parents=True, exist_ok=True)
    results = {}

    klems_go = pd.read_csv(KLEMS_DIR / "[2025.09.22] st_gross_output_1997_2023.csv")
    klems_hrs = pd.read_csv(KLEMS_DIR / "[2025.09.22] st_labor_hours_1997_2023.csv")
    klems_comp = pd.read_csv(KLEMS_DIR / "[2025.09.22] st_labor_compensation_nocol_1997_2023.csv")
    klems_va = pd.read_csv(KLEMS_DIR / "[2025.09.22] st_value_added_1997_2023.csv")

    for year in [1997, 2002, 2007, 2012, 2017]:
        # Load matrices
        use = extract_use_matrix(NAICS_DIR / f"Use_of_Commodities_Summary_{year}.json")
        B = extract_leontief(NAICS_DIR / f"Total_Requirements_IxI_Summary_{year}.json")
        descs = get_sector_descriptions(NAICS_DIR / f"Use_of_Commodities_Summary_{year}.json")
        io_desc_to_code = {v: k for k, v in descs.items()}

        # Compute A-matrix (technical coefficients)
        A = compute_technical_coefficients_naics(use)

        # Align A to B dimensions (B is industry×industry, A may differ)
        common_sectors = sorted(set(A.index) & set(A.columns) & set(B.index) & set(B.columns))
        A_sq = A.loc[common_sectors, common_sectors]
        B_sq = B.loc[common_sectors, common_sectors]

        # Load KLEMS data for this year
        go_yr = klems_go[klems_go['Year'] == year].set_index('Industry Description')['Value']
        hrs_yr = klems_hrs[klems_hrs['Year'] == year].set_index('Industry Description')['Value']
        comp_yr = klems_comp[klems_comp['Year'] == year].set_index('Industry Description')['Value']
        va_yr = klems_va[klems_va['Year'] == year].set_index('Industry Description')['Value']

        # Step 1: Compute labor values lambda* = hp* @ B
        hp_star = pd.Series(0.0, index=common_sectors)
        for ind_name, hours in hrs_yr.items():
            go = go_yr.get(ind_name)
            code = io_desc_to_code.get(ind_name)
            if code and go and go > 0 and code in common_sectors:
                hp_star[code] = hours / go

        lv = pd.Series(hp_star.values @ B_sq.values, index=common_sectors)

        # Step 2: Compute lambda_m (labor value of money)
        total_hrs = sum(hrs_yr.get(ind, 0) for ind in hrs_yr.index
                       if io_desc_to_code.get(ind) in common_sectors)
        total_va = sum(va_yr.get(ind, 0) for ind in va_yr.index
                      if io_desc_to_code.get(ind) in common_sectors)
        lambda_m = total_hrs / total_va if total_va > 0 else 0

        # Step 3: Compute c_j_labor = lambda* @ A (IO-BASED constant capital in labor terms)
        # This is the KEY FIX: c_j = sum_i(lambda*_i * a_ij)
        c_labor = pd.Series(lv.values @ A_sq.values, index=common_sectors)

        # Step 4: Compute v_j_labor (variable capital in labor terms)
        v_labor = pd.Series(0.0, index=common_sectors)
        for ind_name in comp_yr.index:
            code = io_desc_to_code.get(ind_name)
            if code and code in common_sectors:
                v_labor[code] = comp_yr.get(ind_name, 0) * lambda_m

        # Step 5: Compute equalized profit rate in labor terms
        # r_bar = total_surplus_labor / total_(c+v)_labor
        total_c = c_labor.sum()
        total_v = v_labor.sum()
        # go_labor = go * lambda_m for each sector
        go_labor = pd.Series(0.0, index=common_sectors)
        for ind_name in go_yr.index:
            code = io_desc_to_code.get(ind_name)
            if code and code in common_sectors:
                go_labor[code] = go_yr.get(ind_name, 0) * lambda_m

        total_surplus = go_labor.sum() - total_c - total_v
        r_bar = total_surplus / (total_c + total_v) if (total_c + total_v) > 0 else 0

        # Step 6: Compute prices of production
        # pp*_j = (c_j_labor + v_j_labor) * (1 + r_bar) / go_j_labor
        pp_star = pd.Series(dtype=float, index=common_sectors)
        for code in common_sectors:
            if go_labor[code] > 0:
                pp_star[code] = (c_labor[code] + v_labor[code]) * (1 + r_bar) / go_labor[code]

        # Step 7: Regression ln(lambda*) vs ln(pp*)
        valid = (lv > 0) & (pp_star > 0)
        lv_v = lv[valid]
        pp_v = pp_star[valid]

        if len(lv_v) > 5:
            log_lv = np.log(lv_v.values)
            log_pp = np.log(pp_v.values)
            slope, intercept = np.polyfit(log_pp, log_lv, 1)
            corr = np.corrcoef(log_pp, log_lv)[0, 1]
            r_sq = corr ** 2
            dev = ((lv_v - pp_v).abs() / lv_v)
            mad = float(dev.mean())

            results[year] = {
                'slope': round(float(slope), 4),
                'r_squared': round(float(r_sq), 4),
                'mad': round(mad, 4),
                'r_bar': round(float(r_bar), 4),
                'lambda_m': round(float(lambda_m), 8),
                'n_sectors': len(lv_v),
                'method': 'IO-based c_j = lambda* @ A',
            }
            print(f"    [A06] {year}: slope={slope:.3f}, R2={r_sq:.3f}, MAD={mad:.1%}, r_bar={r_bar:.3f}, n={len(lv_v)}")

    with open(ANALYSIS_OUT / "labor_value_price_deviations.json", "w") as f:
        json.dump(results, f, indent=2)

    return {"status": "ok", "results": results}


if __name__ == "__main__":
    generate()
