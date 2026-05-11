"""T504 (V*, variable capital) and T505 (S* = VA* - V*, surplus value).

Book period: Table H.1 (V_star, S_star columns, billions). DEC-020.
Extension:   V*[yr] = V*[1989] × (T512[yr] / T512[1989]) for 1990-1997,
             V*[yr] = W[yr] × T512[yr] for 1998+ (W from BEA NIPA T20100).
             ec_u/ec_p adjustment applied INLINE (no separate M01 pass).

Source: Appendix G methodology, Table G.2.
"""

import numpy as np
import pandas as pd
from pipeline.sources.book_data import load_table_h1
from pipeline.sources.paths import API_DATA, BOOK_SERIES

DEPENDS_ON = ["labor_shares"]  # needs T512 for extension


def _load_bea_compensation() -> pd.DataFrame:
    path = API_DATA / "BEA" / "nipa_6_2D_compensation_by_industry.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _compute_ec_ratio(comp_df: pd.DataFrame) -> pd.Series:
    """Compute ec_u/ec_p ratio from NIPA 6.2D industry compensation data."""
    if comp_df.empty:
        return pd.Series(dtype=float)

    productive_lines = [4, 7, 11, 12, 13, 43, 73, 74, 79, 82, 85]
    unproductive_lines = [35, 38, 57, 62, 65, 69]

    ratios = {}
    for year in comp_df["TimePeriod"].unique():
        yr_data = comp_df[comp_df["TimePeriod"] == year]
        prod_ec = 0
        unprod_ec = 0
        for _, row in yr_data.iterrows():
            ln = int(row["LineNumber"])
            val_str = str(row["DataValue"]).replace(",", "")
            try:
                val = float(val_str)
            except ValueError:
                continue
            if ln in productive_lines:
                prod_ec += val
            elif ln in unproductive_lines:
                unprod_ec += val
        if prod_ec > 0 and unprod_ec > 0:
            ratios[int(year)] = unprod_ec / prod_ec

    return pd.Series(ratios)


def compute(series_store: dict = None) -> dict[str, pd.DataFrame]:
    h1 = load_table_h1()
    if h1.empty:
        return {}

    v_book = h1["V_star"]
    s_book = h1["S_star"]

    # Load T512 for extension
    t512_path = BOOK_SERIES / "T512.csv"
    t512 = pd.Series(dtype=float)
    if t512_path.exists():
        df = pd.read_csv(t512_path, index_col="year")
        t512 = df["combined"].dropna() if "combined" in df.columns else df.iloc[:, 0].dropna()

    # Load W (total compensation) for extension
    w_path = API_DATA / "BEA" / "nipa_T20100_compensation_1929_2025.csv"
    w = pd.Series(dtype=float)
    if w_path.exists():
        w_df = pd.read_csv(w_path)
        if "year" in w_df.columns and "compensation_millions" in w_df.columns:
            w = w_df.set_index("year")["compensation_millions"] / 1e3  # to billions

    # ec_u/ec_p for inline adjustment (replaces M01)
    comp_df = _load_bea_compensation()
    ec_ratio = _compute_ec_ratio(comp_df)

    # Extension
    v_ext = pd.Series(dtype=float)
    anchor = 1989
    if anchor in v_book.index and anchor in t512.index:
        val_89 = v_book[anchor]
        t512_89 = t512[anchor]

        # Adjust T512 for ec_u/ec_p (inline M01 logic)
        t512_adj = t512.copy()
        t511_path = BOOK_SERIES / "T511.csv"
        if t511_path.exists():
            t511_df = pd.read_csv(t511_path, index_col="year")
            t511 = t511_df["book"].dropna() if "book" in t511_df.columns else pd.Series(dtype=float)
            ec_1989 = t512.get(1989, 0.36) / t511.get(1989, 0.36) if t511.get(1989, 0) != 0 else 1.0

            for yr in range(1990, int(t512.index.max()) + 1):
                if yr in t511.index:
                    ec_yr = ec_ratio.get(yr, ec_1989)
                    t512_adj[yr] = t511[yr] * ec_yr if yr in t511.index else t512.get(yr, 0.33)

        # Phase 1 (1990-1997): T512 growth only
        for yr in range(1990, 1998):
            if yr in t512_adj.index:
                v_ext[yr] = val_89 * (t512_adj[yr] / t512_89)

        # Phase 2 (1998+): W growth + T512 growth
        w_1998 = w.get(1998)
        t512_1998 = t512_adj.get(1998)
        if w_1998 and t512_1998 and w_1998 > 0:
            val_98 = val_89 * (t512_1998 / t512_89)
            v_ext[1998] = val_98
            for yr in w.index[w.index > 1998]:
                if yr in t512_adj.index:
                    v_ext[yr] = val_98 * (w[yr] / w_1998) * (t512_adj[yr] / t512_1998)

    # S* extension: use exploitation rate from T506
    s_ext = pd.Series(dtype=float)
    t506_path = BOOK_SERIES / "book_tableH1_1948_1989.csv"
    if t506_path.exists() and len(v_ext) > 0:
        # For extension: S* = e × V* where e comes from T506 combined
        t506_csv = BOOK_SERIES / "T506.csv"
        if t506_csv.exists():
            t506 = pd.read_csv(t506_csv, index_col="year")
            e = t506["combined"].dropna() if "combined" in t506.columns else pd.Series(dtype=float)
            common = v_ext.index.intersection(e.index)
            s_ext = e[common] * v_ext[common]

    t504 = _build(v_book, v_ext)
    t505 = _build(s_book, s_ext)
    return {"T504": t504, "T505": t505}


def _build(book: pd.Series, ext: pd.Series) -> pd.DataFrame:
    combined = pd.concat([book, ext])
    combined = combined[~combined.index.duplicated(keep="first")].sort_index()
    out = pd.DataFrame({"book": book, "combined": combined})
    out.index.name = "year"
    return out
