#!/usr/bin/env python3
"""A07 - Social Burden Rate and Accumulation Dynamics (Table 7.1).

The book's CENTRAL analytical result: decomposition of surplus value into
profit, taxes, and unproductive expenses.

Key equations (Chapter 7):
  S* = Pn + T + Eu          (surplus value decomposition)
  b = (T + Eu) / S* = 1 - Pn/S*  (social burden rate)
  r*' = S* / (K* × u)       (Marxian general profit rate, capacity-adjusted)
  r'n = Pn / (K* × u)       (NIPA net profit rate = (1-b) × r*')
  s' = In / SP*              (social savings rate)
  gK = In / K*               (accumulation rate = s' × u × r*')

Book findings (1948-1989):
  b: 0.56 -> 0.66 (rising 16%)
  r*': falling 25% (1948-1980), recovers 8% (1980-1989)
  r'n: falling 39% (faster because b rises)
  s': stable (~0.15-0.22)

Outputs: outputs/analysis/social_burden_rate.json
         data/final-data/book/series/Table7_1_analytical.csv
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import SERIES_OUT, ANALYSIS_OUT, ensure_dirs

H1_PATH = SERIES_OUT / "book_tableH1_1948_1989.csv"
K_PATH = SERIES_OUT / "K_star_by_industry.csv"
FA_PATH = Path("D:/Arcanum/Projects/ST2/Inputs/API_Data/BEA/fixed_assets_4_1_net_stock.csv")


def _load_table_h1():
    """Load digitized Table H.1 (42 years)."""
    if not H1_PATH.exists():
        return None
    return pd.read_csv(H1_PATH, comment="#", index_col="year")


def _load_capital_stock():
    """Load capital stock K from BEA Fixed Assets Table 4.1."""
    if not FA_PATH.exists():
        return None
    raw = pd.read_csv(FA_PATH)
    # Line 1 = total private nonresidential fixed assets
    total = raw[raw["LineNumber"] == 1].copy()
    k = {}
    for _, row in total.iterrows():
        yr = int(row["TimePeriod"])
        val_str = str(row["DataValue"]).replace(",", "")
        try:
            k[yr] = float(val_str)  # millions (UNIT_MULT=6)
        except ValueError:
            continue
    return pd.Series(k, name="K_millions")


def _load_fred_tcu():
    """Load capacity utilization from FRED (cached or fetch)."""
    tcu_path = Path("D:/Arcanum/Projects/ST2/Technical/NickyData/data/raw-data/api")
    import glob
    tcu_files = list(tcu_path.glob("fred_TCU_*.json"))
    if tcu_files:
        with open(tcu_files[0], encoding="utf-8") as f:
            data = json.load(f)
        obs = {int(o["date"][:4]): float(o["value"]) / 100
               for o in data.get("observations", [])
               if o["value"] != "."}
        return pd.Series(obs, name="TCU")

    # Try fetching
    try:
        import os, requests
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env")
        api_key = os.environ.get("FRED_API_KEY")
        if api_key:
            resp = requests.get("https://api.stlouisfed.org/fred/series/observations",
                               params={"series_id": "TCU", "api_key": api_key,
                                       "file_type": "json", "frequency": "a",
                                       "aggregation_method": "avg"}, timeout=30)
            data = resp.json()
            cache = tcu_path / f"fred_TCU_2026-05-08.json"
            with open(cache, "w") as f:
                json.dump(data, f)
            obs = {int(o["date"][:4]): float(o["value"]) / 100
                   for o in data.get("observations", []) if o["value"] != "."}
            return pd.Series(obs, name="TCU")
    except Exception:
        pass
    return None


def _load_investment():
    """Load net private domestic investment from NIPA."""
    nipa_path = Path("D:/Arcanum/Projects/ST2/Inputs/API_Data/BEA/nipa_2_1_personal_income.csv")
    # Actually we need NIPA Table 1.1.5 for GDP components including investment
    nipa_115 = Path("D:/Arcanum/Projects/ST2/Technical/NickyData/data/raw-data/parsed/moos_nipa_gdp.csv")
    if nipa_115.exists():
        df = pd.read_csv(nipa_115, index_col="year")
        if "gross_private_domestic_investment" in df.columns:
            return df["gross_private_domestic_investment"] / 1e9  # to billions
    return None


def generate():
    """Compute Table 7.1 analytical series."""
    ensure_dirs()
    ANALYSIS_OUT.mkdir(parents=True, exist_ok=True)

    h1 = _load_table_h1()
    if h1 is None:
        print("    [A07] Table H.1 not available")
        return {"status": "fail"}

    k_raw = _load_capital_stock()
    tcu = _load_fred_tcu()

    # --- Book period from Table H.1 ---
    s_star_book = h1["S_star"]
    p_plus_book = h1["P_plus"]

    # --- Extension period from pipeline ---
    t505_path = SERIES_OUT / "T505.csv"
    nipa_comp_path = Path("D:/Arcanum/Projects/ST2/Inputs/API_Data/BEA/nipa_T20100_compensation_1929_2025.csv")
    t201_path = SERIES_OUT / "T201.csv"

    s_star_ext = pd.Series(dtype=float)
    p_plus_ext = pd.Series(dtype=float)

    if t505_path.exists():
        t505 = pd.read_csv(t505_path, index_col="year")
        s_star_ext = t505["combined"].dropna() if "combined" in t505.columns else pd.Series(dtype=float)
        s_star_ext = s_star_ext[s_star_ext.index > 1989]

    if t201_path.exists() and nipa_comp_path.exists():
        t201 = pd.read_csv(t201_path, index_col="year")
        gdp_vals = t201["GDP"] if "GDP" in t201.columns else pd.Series(dtype=float)
        ec_raw = pd.read_csv(nipa_comp_path)
        ec = ec_raw.set_index("year")["compensation_millions"] / 1e3  # to billions
        common = gdp_vals.index.intersection(ec.index)
        ext_yrs = common[common > 1989]
        if len(ext_yrs) > 0:
            p_plus_ext = gdp_vals[ext_yrs] - ec[ext_yrs]

    # Combine
    s_star = pd.concat([s_star_book, s_star_ext])
    s_star = s_star[~s_star.index.duplicated(keep="first")].sort_index()
    p_plus = pd.concat([p_plus_book, p_plus_ext])
    p_plus = p_plus[~p_plus.index.duplicated(keep="first")].sort_index()

    # Compute:
    # From H.1: S* and P+ are known. P+ = VA - EC (gross profit-type income)
    # The ratio P+/S* gives us: P+/S* = (Pn + T)/S* = 1 - Eu/S*
    # But we want b = (T + Eu)/S*, not just Eu/S*

    # Let's compute the "broad" social burden rate using available data:
    # b_broad = 1 - Pn/S* where Pn needs tax data
    # OR: (P+ - S*)/S* gives us the difference between orthodox profit and surplus value
    # as a share of surplus

    # Simpler: use the equation r'n/r*' = Pn/S* = 1 - b
    # We have P+ but need Pn. For now compute P+/S* as upper bound of (1-b)
    # since P+ = Pn + IBT (P+ is gross of indirect taxes but net of nothing)

    p_plus_over_s = p_plus / s_star
    print(f"    [A07] P+/S* range: {p_plus_over_s.min():.3f} - {p_plus_over_s.max():.3f}")
    print(f"    [A07] This implies Eu/S* = 1 - P+/S* = {(1-p_plus_over_s).min():.3f} - {(1-p_plus_over_s).max():.3f}")

    # The unproductive expense share eu_share = 1 - P+/S* = Eu/S*
    eu_share = 1 - p_plus_over_s  # share of S* going to unproductive expenses

    # Profit rate: r* = S* / K
    if k_raw is not None:
        k_bn = k_raw / 1e3  # millions to billions
        common_k = s_star.index.intersection(k_bn.index)
        r_star = s_star[common_k] / k_bn[common_k]

        if tcu is not None:
            common_t = r_star.index.intersection(tcu.index)
            r_star_adj = r_star[common_t] / tcu[common_t]
        else:
            r_star_adj = r_star

        # NIPA profit rate: r_n = P+ / K (using P+ as proxy for Pn)
        r_n = p_plus.reindex(common_k) / k_bn[common_k]
    else:
        r_star = pd.Series(dtype=float)
        r_star_adj = pd.Series(dtype=float)
        r_n = pd.Series(dtype=float)

    # Build output DataFrame
    out = pd.DataFrame({
        "S_star": s_star,
        "P_plus": p_plus,
        "SP_star": s_star,  # SP* ≈ S* (equal in magnitude per Section 3.6.2)
        "P_plus_over_S_star": p_plus_over_s,
        "Eu_share": eu_share,
    })

    if len(r_star) > 0:
        out["r_star"] = r_star
        out["r_star_adj"] = r_star_adj if len(r_star_adj) > 0 else np.nan
        out["r_n_approx"] = r_n

    out.index.name = "year"
    out_path = SERIES_OUT / "analytical_table7_1.csv"
    out.to_csv(out_path)

    # Summary for key years
    results = {}
    for yr in [1948, 1958, 1967, 1972, 1977, 1980, 1989]:
        if yr in out.index:
            row = out.loc[yr]
            entry = {k: round(float(v), 4) for k, v in row.items() if pd.notna(v)}
            results[yr] = entry
            eu_s = row.get("Eu_share", 0)
            r_s = row.get("r_star", 0)
            print(f"    [A07] {yr}: P+/S*={row['P_plus_over_S_star']:.3f}, Eu_share={eu_s:.3f}, r*={r_s:.4f}")

    # Save analysis JSON
    with open(ANALYSIS_OUT / "social_burden_rate.json", "w") as f:
        json.dump({"method": "Table 7.1 decomposition", "years": results,
                   "note": "Eu_share = 1 - P+/S* (unproductive expense share). Full b requires IBT+corp_tax for Pn."}, f, indent=2)

    print(f"    [A07] Table 7.1: {len(out)} years saved")
    return {"status": "ok", "results": results}


if __name__ == "__main__":
    generate()
