#!/usr/bin/env python3
"""P01 - Process revenue aggregates: T501-T503, T508, T509.

Book data (1948-1961 from TableE2) extended via:
  - 1962-1996: BEA aggregate GDP growth rates (NIPA 1.7.5)
  - 1997-2024: IO-based productive sector growth rates (NAICS_marxian_aggregates.csv)

The IO-based extension uses TV* (productive + trading sector GO) growth rates
which better match the book's Marxian Total Product concept than aggregate GDP.

Inputs:  parsed-raw/T501_parsed.csv .. T509_parsed.csv (from L01)
         api-data/BEA/nipa_1_7_5_gross_output_by_industry.csv
         final-data/series/NAICS_marxian_aggregates.csv (optional, from naics_aggregator)
Outputs: final-data/series/T501.csv .. T509.csv (book + combined columns)
Dependencies: L01. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, API_DATA, ensure_dirs
from utils.data_io import load_parsed
from utils.api_data_io import load_bea_nipa
from utils.transforms.splice import splice

SERIES_ID = "T501"
SERIES_IDS = ["T501", "T502", "T503", "T508", "T509"]
PRIORITY = 1

SPLICE_YEAR = 1961


def _load_gdp_series():
    """Load BEA GDP series for growth-rate splicing."""
    gdp_path = API_DATA / "BEA" / "nipa_1_7_5_gross_output_by_industry.csv"
    if not gdp_path.exists():
        return None
    gdp_df = load_bea_nipa(gdp_path, line_filter="Gross domestic product (GDP)")
    col = gdp_df.columns[0]
    gdp = gdp_df[col]
    gdp.index.name = "year"
    return gdp


def _load_io_tv_star():
    """Load IO-based Total Value (TV*) from NAICS Marxian aggregates.

    Returns TV* series (productive + trading sector GO) for 1997-2024.
    Used for IO-based growth rates post-1997 (more faithful than aggregate GDP).
    """
    tv_path = SERIES_OUT / "NAICS_marxian_aggregates.csv"
    if not tv_path.exists():
        return None
    df = pd.read_csv(tv_path, index_col=0)
    if "TV_star" in df.columns:
        return df["TV_star"]
    return None


def process():
    """Process revenue aggregates — book data + BEA GDP extension."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    gdp = _load_gdp_series()
    has_gdp = gdp is not None and len(gdp) > 0
    if not has_gdp:
        steps.append("BEA GDP data not found — book only")

    tv_star = _load_io_tv_star()
    has_io = tv_star is not None and len(tv_star) > 0
    if has_io:
        steps.append(f"IO TV* loaded: {len(tv_star)} years ({int(tv_star.index.min())}-{int(tv_star.index.max())})")

    for sid in SERIES_IDS:
        df, path = load_parsed(sid)
        if df is None:
            steps.append(f"{sid}: parsed file not found at {path}")
            continue

        book = df["value"].dropna()

        # Two-phase extension:
        # Phase 1 (1962-1996): GDP growth rates (no IO data)
        # Phase 2 (1997+): IO-based TV* growth rates (more faithful)
        if has_gdp and SPLICE_YEAR in book.index and SPLICE_YEAR in gdp.index:
            combined = splice(book, gdp, at_year=SPLICE_YEAR, method="growth_rate")
            n_ext = len(combined) - len(book)
            ext_note = f"+ {n_ext} GDP-extended"

            # Overlay IO-based growth rates for 1997+ (for T501 only)
            if has_io and sid == "T501" and 1997 in combined.index:
                anchor_1997 = combined[1997]
                tv_1997 = tv_star.get(1997)
                if tv_1997 and tv_1997 > 0:
                    for yr in tv_star.index:
                        if yr > 1997:
                            io_growth = tv_star[yr] / tv_1997
                            combined[yr] = anchor_1997 * io_growth
                    combined = combined.sort_index()
                    ext_note += " (1997+ IO-based)"
        else:
            combined = book.copy()
            ext_note = "book only"

        out = pd.DataFrame({"book": book, "combined": combined})
        out.index.name = "year"

        out_path = SERIES_OUT / f"{sid}.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict[sid] = combined
        steps.append(f"{sid}: {len(book)} book rows {ext_note} → {len(combined)} total")
        print(f"    [P01] {sid}: {len(combined)} rows ({ext_note})")

    status = "ok" if data_dict and has_gdp else ("warn" if data_dict else "fail")

    return {
        "series_id": SERIES_ID,
        "status": status,
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
