#!/usr/bin/env python3
"""P02 - Process variable capital: T504 (V*).

V*_ext via growth-rate splice: V*[yr] = V*[1989] × (W[yr]/W[1989]) × (T512[yr]/T512[1989])
Growth rates are dimensionless, avoiding the book/BEA unit mismatch.

Inputs:  parsed-raw/T504_parsed.csv (from L02)
         final-data/series/T512.csv (from P05 — must run first)
         api-data/BEA/nipa_6_2D_compensation_by_industry.csv
Outputs: final-data/series/T504.csv
Dependencies: L02, P05 (for T512)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, API_DATA, ensure_dirs
from utils.data_io import load_parsed
from utils.api_data_io import load_bea_nipa

SERIES_ID = "T504"
SERIES_IDS = ["T504"]
PRIORITY = 2


def process():
    """Process V* with BEA compensation extension."""
    ensure_dirs()
    steps = []

    # Load book V* (1948-1989, billions)
    book_df, _ = load_parsed("T504")
    if book_df is None:
        return {"series_id": SERIES_ID, "status": "fail",
                "steps": ["T504 parsed not found"], "data_dict": {}, "outputs": []}

    book = book_df["value"]
    steps.append(f"T504 book: {len(book)} rows, {book.index.min()}-{book.index.max()}")

    # Load T512 combined (V*/W ratio) from final-data
    t512_path = SERIES_OUT / "T512.csv"
    if not t512_path.exists():
        # Fallback: book only
        out = pd.DataFrame({"book": book, "combined": book})
        out.index.name = "year"
        out_path = SERIES_OUT / "T504.csv"
        out.to_csv(out_path)
        steps.append("T512 not available — book only")
        print(f"    [P02] T504: book only ({len(book)} rows), T512 missing")
        return {"series_id": SERIES_ID, "status": "warn",
                "steps": steps, "data_dict": {"T504": book},
                "outputs": [str(out_path)]}

    t512 = pd.read_csv(t512_path, index_col=0)["combined"]

    # Load BEA total compensation W (for growth-rate splice)
    bea_path = API_DATA / "BEA" / "nipa_6_2D_compensation_by_industry.csv"
    if bea_path.exists():
        w_df = load_bea_nipa(bea_path, line_filter="Compensation of employees")
        w = w_df.iloc[:, 0]  # raw scaled values (units don't matter for growth rates)
        steps.append(f"BEA compensation: {len(w)} rows")
    else:
        out = pd.DataFrame({"book": book, "combined": book})
        out.index.name = "year"
        out_path = SERIES_OUT / "T504.csv"
        out.to_csv(out_path)
        steps.append("BEA compensation not found — book only")
        print(f"    [P02] T504: book only, BEA data missing")
        return {"series_id": SERIES_ID, "status": "warn",
                "steps": steps, "data_dict": {"T504": book},
                "outputs": [str(out_path)]}

    # Two-phase growth-rate splice (avoids unit mismatch):
    # Phase 1 (1990-1997): V*[yr] = V*[1989] × T512[yr]/T512[1989] (no W data)
    # Phase 2 (1998+): V*[yr] = V*[1998] × (W[yr]/W[1998]) × (T512[yr]/T512[1998])
    anchor = 1989
    if anchor in book.index and anchor in t512.index:
        val_89 = book[anchor]
        t512_89 = t512[anchor]
        v_star_ext = pd.Series(dtype=float)

        # Phase 1: 1990-1997 (T512 growth only — BEA W starts at 1998)
        for yr in range(1990, 1998):
            if yr in t512.index:
                v_star_ext[yr] = val_89 * (t512[yr] / t512_89)

        # Phase 2: 1998+ (W growth + T512 growth)
        w_1998 = w.get(1998)
        t512_1998 = t512.get(1998)
        if w_1998 is not None and t512_1998 is not None and w_1998 > 0:
            val_98 = val_89 * (t512_1998 / t512_89)
            v_star_ext[1998] = val_98
            for yr in w.index[w.index > 1998]:
                if yr in t512.index:
                    v_star_ext[yr] = val_98 * (w[yr] / w_1998) * (t512[yr] / t512_1998)

        if len(v_star_ext) > 0:
            combined = pd.concat([book, v_star_ext])
            combined = combined[~combined.index.duplicated(keep="first")]
            combined = combined.sort_index()
            steps.append(f"Growth-rate splice: {len(v_star_ext)} ext years")
            print(f"    [P02] T504: {len(v_star_ext)} ext years (1990-97 T512, 1998+ W+T512)")
        else:
            combined = book
    else:
        combined = book
        steps.append("Cannot splice — anchor year missing from book/T512")

    out = pd.DataFrame({"book": book, "combined": combined})
    out.index.name = "year"
    out_path = SERIES_OUT / "T504.csv"
    out.to_csv(out_path)

    n_ext = len(combined) - len(book)
    steps.append(f"Extension: {n_ext} years via growth-rate splice")
    print(f"    [P02] T504: {len(book)} book + {n_ext} ext rows")

    # Sector-level V* computation for comparison (P02b runs independently via discovery)

    return {
        "series_id": SERIES_ID,
        "status": "ok",
        "steps": steps,
        "data_dict": {"T504": combined},
        "outputs": [str(out_path)],
    }
