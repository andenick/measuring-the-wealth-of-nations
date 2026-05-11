"""T504 (V*) and T505 (S*) — Unified Method.

Three eras:
- 1948-1989: Book Table H.1 V* (Shaikh & Tonak's own 82-sector SIC computation)
- 1990-1997: Log-linear interpolation between book endpoint and sector method start
- 1998-2024: Sector method from NIPA T60200D (compensation by industry)

S* = GFP* - Dp - V* where:
- GFP* from integrated_tp_series (detail-level IO)
- Dp = COFC × productive_output_ratio
"""

import numpy as np
import pandas as pd
from pathlib import Path
from .helpers import build_series, save_series, load_computed, interpolate_annual
from nickydata.fetch.bea_nipa import parse_line, parse_by_industry

DEPENDS_ON = ["total_product", "employment"]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

PRODUCTION_SECTORS = {
    "agriculture": {"nipa_line": 4, "pw_source": "bls_proxy", "bls_proxy": "mining"},
    "mining": {"nipa_line": 7, "pw_source": "bls", "bls_sector": "mining"},
    "utilities": {"nipa_line": 11, "pw_source": "bls_proxy", "bls_proxy": "manufacturing"},
    "construction": {"nipa_line": 12, "pw_source": "bls", "bls_sector": "construction"},
    "manufacturing": {"nipa_line": 13, "pw_source": "bls", "bls_sector": "manufacturing"},
    "transportation": {"nipa_line": 43, "pw_source": "bls_proxy", "bls_proxy": "manufacturing"},
    "education": {"nipa_line": 73, "pw_source": "gva_ratio"},
    "health_care": {"nipa_line": 74, "pw_source": "gva_ratio"},
    "arts_entertainment": {"nipa_line": 79, "pw_source": "gva_ratio"},
    "accommodation_food": {"nipa_line": 82, "pw_source": "gva_ratio"},
    "other_services": {"nipa_line": 85, "pw_source": "gva_ratio"},
    "fed_govt_enterprises": {"nipa_line": 91, "pw_source": "avg_private"},
    "sl_govt_enterprises": {"nipa_line": 96, "pw_source": "avg_private"},
}
PROD_SVC_LINES = [73, 74, 79, 82, 85]
ALL_SVC_LINES = [65, 69, 70, 73, 74, 79, 82, 85]


def _val(df, ln):
    if df.empty:
        return 0
    r = df[df["line"] == ln]
    return r["value"].iloc[0] if len(r) > 0 else 0


def _load_book_vstar() -> pd.Series:
    """Load V* from book Table H.1 (1948-1989)."""
    # NickyData project root is two levels up from this file (compute/variable_capital.py -> nickydata -> NickyData)
    project_root = Path(__file__).resolve().parent.parent.parent
    h1_path = project_root / "data" / "final-data" / "book" / "series" / "book_tableH1_1948_1989.csv"
    if not h1_path.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(h1_path, comment="#")
    df = df.set_index("year")
    return df["V_star"]


def _compute_sector_vstar(data: dict, methodology: dict) -> pd.Series:
    """Compute V* from NIPA T60200D sector data (1998-2024)."""
    nipa_ec = parse_by_industry(data.get("nipa", {}).get("T60200D", []))
    nipa_fee = parse_by_industry(data.get("nipa", {}).get("T60500D", []))
    nipa_ws = parse_by_industry(data.get("nipa", {}).get("T60600D", []))
    nipa_pep = parse_by_industry(data.get("nipa", {}).get("T61000D", []))
    nipa_gva = parse_by_industry(data.get("nipa", {}).get("T60100D", []))
    bls_wages = data.get("bls_wages", pd.DataFrame())
    bls_counts = data.get("bls_counts", pd.DataFrame())
    bls_ratios = data.get("bls_ratios", pd.DataFrame())

    avail = sorted(nipa_ec["year"].unique()) if not nipa_ec.empty else []

    # Service GVA ratio from data
    svc_ratio = pd.Series(dtype=float)
    if not nipa_gva.empty:
        for yr in nipa_gva["year"].unique():
            g = nipa_gva[nipa_gva["year"] == yr]
            num = sum(_val(g, ln) for ln in PROD_SVC_LINES)
            den = sum(_val(g, ln) for ln in ALL_SVC_LINES)
            if den > 0:
                svc_ratio[yr] = num / den

    # Average private PW ratio
    avg_pw = bls_ratios.mean(axis=1) if not bls_ratios.empty else pd.Series(dtype=float)

    v_star = pd.Series(dtype=float)

    for yr in avail:
        if yr > 2024:
            continue
        ec_yr = nipa_ec[nipa_ec["year"] == yr]
        fee_yr = nipa_fee[nipa_fee["year"] == yr] if not nipa_fee.empty else pd.DataFrame()
        ws_yr = nipa_ws[nipa_ws["year"] == yr] if not nipa_ws.empty else pd.DataFrame()
        pep_yr = nipa_pep[nipa_pep["year"] == yr] if not nipa_pep.empty else pd.DataFrame()
        total = 0.0

        for name, spec in PRODUCTION_SECTORS.items():
            try:
                ln = spec["nipa_line"]
                ec = _val(ec_yr, ln)
                fee = _val(fee_yr, ln)
                ws = _val(ws_yr, ln)
                pep = _val(pep_yr, ln)
                if ec <= 0 or fee <= 0:
                    continue

                # Supplements ratio from data (EC/WS)
                x = ec / ws if ws > 0 else 1.12

                # Self-employed factor from data (PEP/FEE)
                sep = pep / fee if pep > 0 and fee > 0 else 1.0

                src = spec["pw_source"]
                bs = spec.get("bls_sector", spec.get("bls_proxy", ""))

                if src == "bls" and bs in bls_wages.columns:
                    wp = bls_wages[bs].get(yr, 0)
                    ecp = wp * x if wp > 0 else ec / fee * 1000 * bls_ratios[bs].get(yr, 0.7)
                    lp = bls_counts[bs].get(yr, fee * bls_ratios[bs].get(yr, 0.7)) if bs in bls_counts.columns else fee * 0.7
                elif src == "bls_proxy" and bs in bls_ratios.columns:
                    r = bls_ratios[bs].get(yr, 0.7)
                    ecp = ec / fee * 1000 * r
                    lp = fee * r
                elif src == "gva_ratio":
                    ecp = ec / fee * 1000
                    sr = svc_ratio.get(yr, svc_ratio.mean() if len(svc_ratio) > 0 else 0.5)
                    lp = fee * sr
                elif src == "avg_private":
                    r = avg_pw.get(yr, 0.7)
                    ecp = ec / fee * 1000 * r
                    lp = fee * r
                else:
                    continue

                total += ecp * lp * sep / 1e6
            except Exception:
                continue

        if total > 0:
            v_star[yr] = total

    return v_star


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    t503 = load_computed("T503")

    # Era 1: Book V* (1948-1989)
    book_vstar = _load_book_vstar()
    if not book_vstar.empty:
        print(f"    Book V*: {len(book_vstar)} years ({int(book_vstar.index.min())}-{int(book_vstar.index.max())})")

    # Era 3: Sector method V* (1998-2024)
    sector_vstar = _compute_sector_vstar(data, methodology)
    if not sector_vstar.empty:
        print(f"    Sector V*: {len(sector_vstar)} years ({int(sector_vstar.index.min())}-{int(sector_vstar.index.max())})")
        print(f"    Sector V*(1998) = {sector_vstar.iloc[0]:.1f}bn")

    # Era 2: Interpolate 1990-1997
    interp_vstar = pd.Series(dtype=float)
    if not book_vstar.empty and not sector_vstar.empty:
        v_1989 = book_vstar.get(1989, book_vstar.iloc[-1])
        v_1998 = sector_vstar.iloc[0]
        yr_1989 = 1989
        yr_1998 = int(sector_vstar.index.min())

        for yr in range(yr_1989 + 1, yr_1998):
            t = (yr - yr_1989) / (yr_1998 - yr_1989)
            # Log-linear interpolation for smooth growth
            interp_vstar[yr] = v_1989 * (v_1998 / v_1989) ** t

        print(f"    Interpolated: {len(interp_vstar)} years (1990-{yr_1998 - 1})")
        print(f"    V*(1989)={v_1989:.1f} -> V*(1998)={v_1998:.1f} (gap: {(v_1998/v_1989 - 1)*100:.1f}%)")

    # Combine all eras
    v_star = pd.concat([book_vstar, interp_vstar, sector_vstar])
    v_star = v_star[~v_star.index.duplicated(keep="first")].sort_index()
    v_star.name = "V_star"

    # S* = GFP* - Dp - V*
    # Dp sources:
    # - 1948-1989: Book Table H.1 "Dp" column (depreciation of productive fixed capital)
    # - 1990-2024: COFC × productive output ratio from detail IO data

    # Load book Dp
    book_dp = pd.Series(dtype=float)
    project_root = Path(__file__).resolve().parent.parent.parent
    h1_path = project_root / "data" / "final-data" / "book" / "series" / "book_tableH1_1948_1989.csv"
    if h1_path.exists():
        h1_df = pd.read_csv(h1_path, comment="#").set_index("year")
        book_dp = h1_df["Dp"]

    # Computed Dp for post-book era
    cofc = data.get("cofc", pd.Series(dtype=float))

    # Use detail-level productive GO share from integrated series for the ratio
    integrated_path = Path(__file__).resolve().parent.parent / "data" / "computed" / "integrated_tp_series.csv"
    if integrated_path.exists():
        integ = pd.read_csv(integrated_path, index_col="year")
        # productive_go_share available for 1997+; for interpolated/book years use TP*/GO proxy
        pr_series = pd.Series(dtype=float)
        if "productive_go_share" in integ.columns:
            pr_series = integ["productive_go_share"].dropna()
        # For book years, estimate from TP*/GDP / (GO/GDP): book's productive share was ~0.85-0.95
        if not pr_series.empty:
            pr_1997 = pr_series.iloc[0] if 1997 in pr_series.index else 0.54
        else:
            pr_1997 = 0.54
    else:
        pr_1997 = 0.54

    # Build Dp series
    dp_series = pd.Series(dtype=float)
    for yr in book_dp.index:
        dp_series[yr] = book_dp[yr]

    # Interpolate 1990-1996 and compute 1997+
    if not book_dp.empty and not cofc.empty:
        dp_1989 = book_dp.get(1989, book_dp.iloc[-1])
        # For 1990+: COFC × productive share
        # Productive share for pre-1997: interpolate from book-implied to detail data
        # Book Dp(1989) / COFC(1989): what was the book's productive ratio?
        cofc_1989 = cofc.get(1989, 0)
        if cofc_1989 > 0:
            book_ratio_1989 = dp_1989 / cofc_1989
        else:
            book_ratio_1989 = 0.75

        for yr in range(1990, 2025):
            if yr in cofc.index:
                if yr < 1997:
                    # Interpolate ratio from book's to detail data's
                    t = (yr - 1989) / (1997 - 1989)
                    ratio = book_ratio_1989 + t * (pr_1997 - book_ratio_1989)
                else:
                    # Use detail-level productive share
                    ratio = pr_series.get(yr, pr_1997) if not pr_series.empty else pr_1997
                dp_series[yr] = cofc[yr] * ratio

    s_star = pd.Series(dtype=float)
    if not t503.empty and not v_star.empty:
        common = t503.index.intersection(v_star.index)
        for yr in common:
            dp = dp_series.get(yr, 0)
            va = t503[yr] - dp
            s_star[yr] = va - v_star[yr]

    results = {
        "T504": build_series(v_star, pd.Series(dtype=float)),
        "T505": build_series(s_star, pd.Series(dtype=float)),
    }
    for sid, df in results.items():
        save_series(sid, df)
        print(f"    {sid}: {len(df)} years")

    # Diagnostics
    if 1948 in v_star.index:
        print(f"    V*(1948) = {v_star[1948]:.1f}bn (book: 88.4)")
    if 1989 in v_star.index and 1948 in v_star.index:
        e48 = s_star.get(1948, 0) / v_star[1948] if v_star[1948] > 0 else 0
        e89 = s_star.get(1989, 0) / v_star[1989] if v_star[1989] > 0 else 0
        print(f"    e(1948) = {e48:.2f} (book: 1.70)")
        print(f"    e(1989) = {e89:.2f} (book: 2.44)")
        print(f"    e trajectory: {'RISING' if e89 > e48 else 'FALLING'}")

    return results
