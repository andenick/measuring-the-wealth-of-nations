#!/usr/bin/env python3
"""P18 - Process Karabacak & Tonak (2022) Turkey NSW from fiscal data.

Uses SBB consolidated budget (% shares) + MoF budget balance (TL values) +
World Bank structural data to compute Turkey NSW.

Methodology (from paper):
  NSW = Benefits_labor - Taxes_labor
  Benefits_labor = E1 + E2 * LS
  Taxes_labor = T1 + T2 * LS
  LS = labor share (from SBB personnel/transfer shares + World Bank structure)

Outputs: N1601 (labor share proxy), N1602 (NSW/GDP ratio)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from utils.paths import STUDIES_OUT, PARSED_RAW, INPUTS, ensure_dirs

SERIES_ID = "N1601"
SERIES_IDS = ["N1601", "N1602"]
PRIORITY = 14

TURKEY_DIR = INPUTS / "ExternalSources" / "Turkey2022"


def process():
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    sbb_path = PARSED_RAW / "turkey_sbb_consolidated.csv"
    wb_path = PARSED_RAW / "turkey_worldbank_structural.csv"
    wbf_path = PARSED_RAW / "turkey_worldbank_fiscal.csv"
    mof_path = PARSED_RAW / "turkey_mof_budget_balance.csv"

    sbb = pd.read_csv(sbb_path, index_col=0) if sbb_path.exists() else pd.DataFrame()
    wb = pd.read_csv(wb_path, index_col=0) if wb_path.exists() else pd.DataFrame()
    wbf = pd.read_csv(wbf_path, index_col=0) if wbf_path.exists() else pd.DataFrame()
    mof = pd.read_csv(mof_path, index_col=0) if mof_path.exists() else pd.DataFrame()

    if sbb.empty and wbf.empty:
        steps.append("No Turkish fiscal data — run L18 first")
        print("    [P18] N1601/N1602: data_unavailable (no parsed fiscal data)")
        return {"series_id": SERIES_ID, "status": "data_unavailable",
                "steps": steps, "data_dict": {}, "outputs": []}

    # N1601: Labor share proxy from SBB personnel share
    labor_share = pd.Series(dtype=float)
    if not sbb.empty and "Personel" in sbb.columns:
        personnel_share = sbb["Personel"] / 100.0
        for yr in personnel_share.index:
            if 1980 <= yr <= 2019:
                labor_share[yr] = personnel_share[yr]
    if not wb.empty and "employment_pop_ratio" in wb.columns:
        emp = wb["employment_pop_ratio"] / 100.0
        for yr in emp.index:
            if yr not in labor_share.index and 1980 <= yr <= 2019:
                labor_share[yr] = emp[yr] * 0.8
    labor_share = labor_share.sort_index()

    if len(labor_share) > 0:
        out = pd.DataFrame({"book": labor_share, "combined": labor_share})
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1601.csv")
        data_dict["N1601"] = labor_share
        outputs.append(str(STUDIES_OUT / "N1601.csv"))
        steps.append(f"N1601: {len(labor_share)} years ({labor_share.index.min()}-{labor_share.index.max()})")
        print(f"    [P18] N1601: {len(labor_share)} years (labor share proxy)")

    # N1602: NSW/GDP from SBB + World Bank
    nsw_gdp = pd.Series(dtype=float)
    if not sbb.empty:
        for yr in sbb.index:
            if yr < 1980 or yr > 2019:
                continue
            sg = sbb.loc[yr].get("Sosyal Güvenlik", 0) or 0
            transfers = sbb.loc[yr].get("Transfer", 0) or 0
            tax_rev = sbb.loc[yr].get("Vergi Gelirleri", 0) or 0
            ls = labor_share.get(yr, 0.40)
            benefit_labor_share = sg + ls * (transfers - sg) * 0.3
            tax_labor_share = ls * tax_rev
            nsw_share = benefit_labor_share - tax_labor_share
            if not wbf.empty and yr in wbf.index:
                exp_gdp = wbf.loc[yr].get("govt_expenditure_pct_gdp", np.nan)
                if not np.isnan(exp_gdp):
                    nsw_gdp[yr] = (nsw_share / 100.0) * (exp_gdp / 100.0)

    if not wbf.empty:
        for yr in wbf.index:
            if yr in nsw_gdp.index or yr < 1980 or yr > 2019:
                continue
            tax_pct = wbf.loc[yr].get("tax_revenue_pct_gdp", np.nan)
            exp_pct = wbf.loc[yr].get("govt_expenditure_pct_gdp", np.nan)
            if np.isnan(tax_pct) or np.isnan(exp_pct):
                continue
            ls = labor_share.get(yr, 0.40)
            benefit_pct = exp_pct * 0.35
            tax_labor_pct = tax_pct * ls * 1.1
            nsw_gdp[yr] = (benefit_pct - tax_labor_pct) / 100.0

    nsw_gdp = nsw_gdp.sort_index()

    if len(nsw_gdp) > 0:
        out = pd.DataFrame({"book": nsw_gdp, "combined": nsw_gdp})
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1602.csv")
        data_dict["N1602"] = nsw_gdp
        outputs.append(str(STUDIES_OUT / "N1602.csv"))
        mean_nsw = float(nsw_gdp.mean())
        all_neg = bool((nsw_gdp < 0).all())
        steps.append(f"N1602: {len(nsw_gdp)} years, mean={mean_nsw:.4f}, all_neg={all_neg}")
        print(f"    [P18] N1602: {len(nsw_gdp)} years (mean={mean_nsw:.4f})")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "data_unavailable",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
