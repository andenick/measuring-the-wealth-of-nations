"""L01_S702 — Load Unproductive Labor Coefficient inputs (Ch7 real-fix).

Symmetric counterpart of L01_S701. The book's Ch7 unproductive labor
coefficient `lambda_u = hu (I - app*)^{-1}` requires the unproductive
sector partition of Appendix F (productive_share < 0.5: wholesale trade,
retail trade, finance/insurance/RE, business services, plus the two
"special" intermediate-use entries).

Same input pattern as S701: BLS CES employment + weekly hours, Appendix F
filter, BEA IO matrices (year list for P02), SIC↔NAICS bridge.

The mapping logic and helpers are shared with L01_S701 via direct import
(per Decision 0004: small per-series scripts that delegate mechanics to
shared utilities — the sister L01 is the natural home for these helpers
since L01_S701 and L01_S702 are the only consumers).

Output:
  data/raw/ch07/L01_S702_output.csv -- long format
    [sector_code, sector_name, nipa_industry, nipa_industry_name,
     productive_share, bls_supersector_slug, bls_employment_series_id,
     bls_hours_series_id, hours_datatype, year, employment_thousands,
     weekly_hours]

Coverage caveats:
  - Wholesale_trade / retail_trade / transp_warehousing supersectors: 1972+
  - Financial / prof_business / information / leisure / education_health /
    other_services: 1964+
  - Special "n/a" sectors (81 imports, 84 scrap) excluded — they are not
    labor-bearing per Table_F_1 notes.
  - Sectors 82/83 (business travel, office supplies) are unproductive but
    are special intermediate-use categories with NIPA industry 13
    (Government) — no CES coverage, NaN preserved.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Reuse the sister loader's helpers — single source of truth for the
# NIPA→BLS slug map and hours-datatype priority logic.
from L01_loaders.L01_S701_labor_coefficient_productive import (  # noqa: E402
    APPENDIX_F,
    BLS_CACHE_DIR,
    DATA_RAW,
    IO_LABELED_DIR,
    SIC_NAICS_BRIDGE,
    _list_io_matrix_years,
    build_long_panel,
    load_appendix_f,
)


SERIES_ID = "S702"
SUBSERIES = "S702-A"

OUTPUT_DIR = DATA_RAW / "ch07"
OUTPUT_CSV = OUTPUT_DIR / "L01_S702_output.csv"


def load() -> dict:
    """Top-level loader: returns dict of all S702 raw inputs for P02_S702."""
    panel = build_long_panel(productive_filter="unproductive")
    f = load_appendix_f("unproductive")
    bridge = pd.read_csv(SIC_NAICS_BRIDGE) if SIC_NAICS_BRIDGE.exists() else None
    return {
        "panel":            panel,
        "appendix_f":       f,
        "io_matrix_years":  _list_io_matrix_years(),
        "sic_naics_bridge": bridge,
        "provenance": {
            "series_id":         SERIES_ID,
            "subseries":         SUBSERIES,
            "productive_filter": "productive_share < 0.5 (excludes n/a sectors 81/84)",
            "bls_cache_dir":     str(BLS_CACHE_DIR),
            "appendix_f_path":   str(APPENDIX_F),
            "sic_naics_bridge":  str(SIC_NAICS_BRIDGE),
            "io_labeled_dir":    str(IO_LABELED_DIR),
            "hours_datatype_priority": "33_goods -> 07_services",
            "shared_with":       "L01_S701_labor_coefficient_productive",
        },
    }


def write_raw_output(panel: pd.DataFrame) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUTPUT_CSV, index=False)
    return OUTPUT_CSV


def run():
    bundle = load()
    panel = bundle["panel"]
    out_path = write_raw_output(panel)
    print(f"    [L01_{SERIES_ID}] panel: {len(panel)} rows; "
          f"{panel['sector_code'].nunique()} unproductive sectors; "
          f"years {panel['year'].min()}-{panel['year'].max()}")
    print(f"    [L01_{SERIES_ID}] supersectors mapped: "
          f"{panel['bls_supersector_slug'].dropna().nunique()}; "
          f"unmapped-sector rows: {panel['bls_supersector_slug'].isna().sum()}")
    print(f"    [L01_{SERIES_ID}] io_matrix_years sic_era={bundle['io_matrix_years']['sic_era']}; "
          f"naics_era={bundle['io_matrix_years']['naics_era']}")
    print(f"    [L01_{SERIES_ID}] first 5 rows:")
    with pd.option_context("display.max_columns", None, "display.width", 220):
        print(panel.head(5).to_string(index=False))
    print(f"    [L01_{SERIES_ID}] wrote {out_path}")
    return bundle


if __name__ == "__main__":
    run()
