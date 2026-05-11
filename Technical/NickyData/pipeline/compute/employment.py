"""T515 (Lp, productive employment) and T516 (Lu, unproductive employment).

Book period: Employment_1948_1989.csv (thousands).
Extension:   BLS CES production workers scaled at 1989 splice point.
             Total employment from FRED PAYEMS (includes government).

Source: Appendix F (Table F.1). Book's L includes government + self-employed.
"""

import pandas as pd
from pipeline.sources.book_data import load_employment
from pipeline.sources.api_fetch import load_parsed, load_nipa_csv
from pipeline.sources.paths import API_DATA

DEPENDS_ON = []


def compute(series_store: dict = None) -> dict[str, pd.DataFrame]:
    emp = load_employment()
    if emp.empty:
        return {}

    lp_book = emp["T515"] if "T515" in emp.columns else pd.Series(dtype=float)
    lu_book = emp["T516"] if "T516" in emp.columns else pd.Series(dtype=float)

    # Extension via BLS CES + PAYEMS
    lp_ext = pd.Series(dtype=float)
    lu_ext = pd.Series(dtype=float)

    bls_path = API_DATA / "BLS" / "bls_ces_production_workers.csv"
    payems_df = load_parsed("total_nonfarm_employment.csv")

    if bls_path.exists() and not payems_df.empty:
        bls = pd.read_csv(bls_path, index_col="year")
        prod_col = "CES0500000006"
        if prod_col in bls.columns:
            prod = bls[prod_col].dropna()
            total_nonfarm = payems_df["value"].dropna()

            ext_years = prod.index[prod.index > 1989]
            if 1989 in lp_book.index and 1989 in prod.index:
                scale = lp_book[1989] / prod[1989]
                lp_ext = prod[ext_years] * scale

                book_total = lp_book[1989] + lu_book[1989]
                total_1989 = total_nonfarm.get(1989, None)
                if total_1989 and total_1989 > 0:
                    total_scale = book_total / total_1989
                    common = ext_years.intersection(total_nonfarm.index)
                    total_scaled = total_nonfarm[common] * total_scale
                    lu_ext = total_scaled - lp_ext.reindex(common).fillna(0)

    t515 = _build(lp_book, lp_ext)
    t516 = _build(lu_book, lu_ext)
    return {"T515": t515, "T516": t516}


def _build(book: pd.Series, ext: pd.Series) -> pd.DataFrame:
    combined = pd.concat([book, ext])
    combined = combined[~combined.index.duplicated(keep="first")].sort_index()
    out = pd.DataFrame({"book": book, "combined": combined})
    out.index.name = "year"
    return out
