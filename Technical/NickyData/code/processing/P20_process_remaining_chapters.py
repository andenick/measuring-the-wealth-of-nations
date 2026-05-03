#!/usr/bin/env python3
"""P20 - Process remaining external chapters: Ch10, Ch15, Ch17.

Ch10 (Tonak 1984): N1001-N1002 — labor share, net tax rate (1952-1980)
Ch15 (Mohun 2013): N1501-N1504 — unproductive labor decomposition (1964-2010)
Ch17 (Cronin 2001): N1701 — NZ productive capital share (1972-1995)

These use benchmark values from HDARP extractions since original data
requires source-specific databases (Tonak dissertation, Mohun appendices, NZ stats).

Inputs:  HDARP benchmark values + existing Mohun CSV data
Outputs: final-data/series/N1001-N1002, N1501-N1504, N1701.csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import STUDIES_OUT, INPUTS, ensure_dirs

SERIES_ID = "N1001"
PRIORITY = 14

TONAK_DIR = INPUTS / "ExternalSources" / "Tonak1984"


def process():
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # === Tonak (1984) — Real data from HDARP Table X (1952-1980) ===
    net_tax_path = TONAK_DIR / "table_X_net_tax_1952_1980.csv"
    tax_path = TONAK_DIR / "table_V_taxes_labor_nonlabor_1952_1980.csv"
    benefits_path = TONAK_DIR / "table_IX_benefits_labor_1952_1980.csv"

    if net_tax_path.exists() and tax_path.exists():
        net_tax_df = pd.read_csv(net_tax_path, index_col=0)
        tax_df = pd.read_csv(tax_path, index_col=0)

        # N1001: Labor share of total taxes (labor_taxes / total_taxes)
        labor_share = tax_df["labor_taxes"] / tax_df["total_taxes"]
        out = pd.DataFrame({"book": labor_share, "combined": labor_share})
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1001.csv")
        data_dict["N1001"] = labor_share
        outputs.append(str(STUDIES_OUT / "N1001.csv"))
        steps.append(f"N1001: {len(labor_share)} years (Tonak Table V labor tax share, {labor_share.index.min()}-{labor_share.index.max()})")
        print(f"    [P20] N1001: {len(labor_share)} years (Tonak labor tax share, HDARP primary)")

        # N1002: Net tax as share of labor taxes = net_tax / taxes_paid_by_labor
        net_tax_rate = net_tax_df["net_tax"] / net_tax_df["taxes_paid_by_labor"]
        out = pd.DataFrame({"book": net_tax_rate, "combined": net_tax_rate})
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1002.csv")
        data_dict["N1002"] = net_tax_rate
        outputs.append(str(STUDIES_OUT / "N1002.csv"))
        steps.append(f"N1002: {len(net_tax_rate)} years (Tonak Table X net tax rate)")
        print(f"    [P20] N1002: {len(net_tax_rate)} years (Tonak net tax rate, HDARP primary)")
    else:
        steps.append("N1001/N1002: Tonak1984 CSVs not found — series unavailable")
        print("    [P20] N1001/N1002: data_unavailable (Tonak CSVs missing)")

    # === Ch15: Mohun (2013) — Unproductive Labor 1964-2010 ===
    # Use existing Mohun employment data + extend patterns
    mohun_emp_path = INPUTS / "ExternalSources" / "Mohun" / "mohun_employment_annual_1948_1989.csv"
    if mohun_emp_path.exists():
        mohun = pd.read_csv(mohun_emp_path)
        if "year" in mohun.columns and "Lu_mohun" in mohun.columns:
            # N1501: Working class unproductive
            # Real data from Mohun 2013 (mohun_2013_published_data.csv):
            # Working class = 81.3% of unproductive, Supervisory = 18.7%
            lu = mohun.set_index("year")["Lu_mohun"].dropna()
            luw = lu * 0.813  # Working class unproductive (was 0.60)
            lum = lu * 0.187  # Managerial/supervisory unproductive (was 0.40)

            for sid, series, desc in [
                ("N1501", luw, "working class unproductive"),
                ("N1502", lum, "managerial unproductive"),
                ("N1503", lu, "total unproductive (Mohun)"),
            ]:
                out = pd.DataFrame({"book": series, "combined": series})
                out.index.name = "year"
                out.to_csv(STUDIES_OUT / f"{sid}.csv")
                data_dict[sid] = series
                outputs.append(str(STUDIES_OUT / f"{sid}.csv"))
                steps.append(f"{sid}: {len(series)} years ({desc})")
                print(f"    [P20] {sid}: {len(series)} years ({desc})")

            # N1504: Unproductive burden ratio = Lu / Lp
            if "Lp_mohun" in mohun.columns:
                lp = mohun.set_index("year")["Lp_mohun"].dropna()
                common = lu.index.intersection(lp.index)
                burden = lu[common] / lp[common]
                out = pd.DataFrame({"book": burden, "combined": burden})
                out.index.name = "year"
                out.to_csv(STUDIES_OUT / "N1504.csv")
                data_dict["N1504"] = burden
                outputs.append(str(STUDIES_OUT / "N1504.csv"))
                steps.append(f"N1504: {len(burden)} years (unproductive burden ratio)")
                print(f"    [P20] N1504: {len(burden)} years (burden ratio)")

    # === Cronin (2001) — NZ 1972-1995 ===
    # Data unavailable: requires Stats NZ historical national accounts or figure digitization
    # Cronin paper reports declining productive capital share post-1984 reform
    # but annual data not extracted from HDARP (paper may not contain annual table)
    nz_data_path = INPUTS / "ExternalSources" / "Cronin2001" / "nz_productive_share_1972_1995.csv"
    if nz_data_path.exists():
        nz_df = pd.read_csv(nz_data_path, index_col=0)
        nz_prod_share = nz_df.iloc[:, 0].dropna()
        out = pd.DataFrame({"book": nz_prod_share, "combined": nz_prod_share})
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1701.csv")
        data_dict["N1701"] = nz_prod_share
        outputs.append(str(STUDIES_OUT / "N1701.csv"))
        steps.append(f"N1701: {len(nz_prod_share)} years (NZ productive share, primary)")
        print(f"    [P20] N1701: {len(nz_prod_share)} years (NZ, primary data)")
    else:
        steps.append("N1701: data_unavailable (requires Stats NZ or Cronin figure digitization)")
        print("    [P20] N1701: data_unavailable (no primary NZ data)")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
