"""T511 (Lp/L, productive labor share) and T512 (V*/W, productive wage share).

Book period: Table 5.7 KeyRatios (1948-1989).
Extension:
  T511: IO productive employment ratio from NAICS benchmarks, growth-rate bridge from 1989.
  T512: V*/W from T504 (V* combined) / NIPA total compensation W.

Source: Appendix F/G. DEC-019 documents T511 IO extension. DEC-016 documents T512.
"""

import pandas as pd
from pathlib import Path
from pipeline.sources.book_data import load_key_ratios
from pipeline.sources.paths import BOOK_SERIES, PARSED_RAW, API_DATA

DEPENDS_ON = []  # T511 uses IO ratios (pre-computed by io_matrices), T512 fallback doesn't need upstream


def compute(series_store: dict = None) -> dict[str, pd.DataFrame]:
    ratios = load_key_ratios()
    if ratios.empty:
        return {}

    t511_book = ratios["T511A"] if "T511A" in ratios.columns else pd.Series(dtype=float)
    t512_book = ratios["T512A"] if "T512A" in ratios.columns else pd.Series(dtype=float)

    # T511 extension via IO productive ratio
    t511_ext = _extend_t511_io(t511_book)

    # T512 extension via V*/W components (or fallback to book-only)
    t512_ext = _extend_t512_vw(t512_book)

    t511 = _build(t511_book, t511_ext)
    t512 = _build(t512_book, t512_ext)
    return {"T511": t511, "T512": t512}


def _extend_t511_io(book: pd.Series) -> pd.Series:
    """Extend T511 using IO productive employment ratio."""
    io_path = BOOK_SERIES / "IO_productive_ratios.csv"
    if not io_path.exists() or 1989 not in book.index:
        return pd.Series(dtype=float)

    io = pd.read_csv(io_path, index_col="year")
    col = "ratio_productive_employment" if "ratio_productive_employment" in io.columns else "ratio_productive_output"
    if col not in io.columns:
        return pd.Series(dtype=float)

    ratio = io[col]
    book_1989 = book[1989]
    first_io_yr = int(ratio.index.min())
    t511_at_io_start = book_1989 * (ratio[first_io_yr] / ratio.get(min(ratio.index), ratio[first_io_yr]))

    ext = pd.Series(dtype=float)
    for yr in range(1990, first_io_yr):
        frac = (yr - 1989) / (first_io_yr - 1989)
        ext[yr] = book_1989 + frac * (t511_at_io_start - book_1989)
    for yr in ratio.index[ratio.index > 1989]:
        ext[yr] = t511_at_io_start * (ratio[yr] / ratio[first_io_yr])
    return ext


def _extend_t512_vw(book: pd.Series) -> pd.Series:
    """Extend T512 = V*/W from components."""
    comp_path = API_DATA / "BEA" / "nipa_T20100_compensation_1929_2025.csv"
    t504_path = BOOK_SERIES / "T504.csv"

    if not comp_path.exists() or not t504_path.exists():
        return pd.Series(dtype=float)

    w_df = pd.read_csv(comp_path)
    if "year" not in w_df.columns or "compensation_millions" not in w_df.columns:
        return pd.Series(dtype=float)
    w = w_df.set_index("year")["compensation_millions"] / 1e3  # to billions

    t504 = pd.read_csv(t504_path, index_col="year")
    v_star = t504["combined"].dropna() if "combined" in t504.columns else pd.Series(dtype=float)

    common = v_star.index.intersection(w.index)
    ext_yrs = common[common > 1989]
    if len(ext_yrs) == 0:
        return pd.Series(dtype=float)

    return v_star[ext_yrs] / w[ext_yrs]


def _build(book: pd.Series, ext: pd.Series) -> pd.DataFrame:
    combined = pd.concat([book, ext])
    combined = combined[~combined.index.duplicated(keep="first")].sort_index()
    out = pd.DataFrame({"book": book, "combined": combined})
    out.index.name = "year"
    return out
