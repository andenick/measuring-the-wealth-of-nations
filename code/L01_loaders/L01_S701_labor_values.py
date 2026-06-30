"""L01_S701 — Load Productive Labor Coefficient inputs (Ch7 real-fix).

Replaces the legacy proxy that derived S701 from `mean(column_sum(Leontief
inverse))` over the labeled BEA A matrix. The book's Ch7 labor coefficient
vector is `lambda* = hp* (I - app*)^{-1}` where `hp*_j` is the productive
labor-hours per unit of gross output in sector j (see Appendix F + Ch7 §7.2).
This loader assembles the **raw** inputs P02_S701 needs to compute that:

  1. BLS CES production-worker employment (datatype 06), per supersector,
     for the productive partition of Appendix F Table F.1.
  2. BLS CES production-worker average weekly hours — datatype 33 where
     available (goods-producing super-sectors, 1948+; manufacturing
     subs 1956+), else datatype 07 (services-friendly, 1964+).
  3. Appendix F Table F.1 productive-share filter (productive_share > 0.5).
  4. BEA IO matrices (labeled) -- listed by year for P02's Leontief stage;
     this L01 does NOT load matrix cells (P02 reads them directly).
  5. SIC↔NAICS bridge -- listed for P02's matrix-era splice.

Per the Anu L-stage contract, this loader ONLY loads + aligns. No
construction logic, no aggregation across BLS supersectors, no Leontief
math. P02_S701 handles all transformation.

Output:
  data/raw/ch07/L01_S701_output.csv -- long format
    [sector_code, sector_name, nipa_industry, nipa_industry_name,
     productive_share, bls_supersector_slug, bls_employment_series_id,
     bls_hours_series_id, hours_datatype, year, employment_thousands,
     weekly_hours]

Coverage caveats (preserved as NaN, not fabricated):
  - Services-era supersectors (CES05/08/40/etc): employment 1964+, hours 1964+
  - Mining/construction/manufacturing supersectors: employment + hours 1948+
  - Manufacturing-subsectors datatype 33 coverage: 1956+
  - Utilities (NIPA 8), Government (NIPA 13): no CES coverage (NaN throughout)
  - Agriculture (NIPA 1): no CES private-sector coverage (NaN throughout)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_SOURCE, DATA_INTERMEDIATE, ROOT  # noqa: E402


SERIES_ID = "S701"
SUBSERIES = "S701-A"

# ---- Input paths ----

APPENDIX_F        = DATA_SOURCE / "appendix_F" / "Table_F_1.csv"
SIC_NAICS_BRIDGE  = DATA_SOURCE / "concordances" / "sic_naics_bridge.csv"
IO_LABELED_DIR    = DATA_INTERMEDIATE / "io_matrices_labeled"
BLS_CACHE_DIR     = ROOT / "data" / "raw" / "bls"

OUTPUT_DIR = DATA_RAW / "ch07"
OUTPUT_CSV = OUTPUT_DIR / "L01_S701_output.csv"

# ---- NIPA industry → BLS CES supersector slug mapping ----
#
# Appendix F partitions the 85 BEA I-O sectors into 13 NIPA industries. The
# BLS CES 21-supersector cache covers a subset of those (private sector only;
# no agriculture, no government, no utilities). For each NIPA industry, we
# pick the BEST single BLS CES supersector slug to use as the labor-input
# source. Where no good match exists the slug is None and rows are emitted
# with NaN employment/hours (preserves the data gap, doesn't fabricate).
#
# Per Ch7 spec the supersector aggregation is a documented divergence vs.
# Appendix C's 85-SIC classification — captured in S701 EPR (authored by P02).

NIPA_TO_BLS_SLUG: dict[int, Optional[str]] = {
    1:  None,                     # Agriculture, forestry, fishing — no CES
    2:  "mining_logging",          # Mining
    3:  "construction",            # Construction
    4:  "durable_goods",           # Manufacturing (durable goods)
    5:  "nondurable_goods",        # Manufacturing (nondurable goods)
    6:  "transp_warehousing",      # Transportation
    7:  "information",             # Communications (best CES analog)
    8:  None,                      # Electric/gas utilities (utilities slug unfetched)
    9:  "wholesale_trade",         # Wholesale trade (unproductive — for S702)
    10: "retail_trade",            # Retail trade (unproductive — for S702)
    11: "financial",               # Finance/insurance/RE (unproductive — for S702)
    12: "leisure_hospitality",     # Services — heterogeneous; see notes below
    13: None,                      # Government — no private CES coverage
}

# NIPA 12 (Services) bundles diverse 85-sector codes with both productive
# (hotels, repair, amusements, medical/education) and unproductive (business
# services) characters. The Ch7 Appendix C breaks this finer; for the L01
# super-sector default we use leisure_hospitality as the broadest productive
# services slug. Sector 74 (Business services, unproductive) is mapped via
# the per-row override below.

PER_SECTOR_SLUG_OVERRIDE: dict[int, Optional[str]] = {
    74: "prof_business",           # Business services (NIPA 12, unproductive)
    78: "education_health",        # Medical/educational services (NIPA 12, productive)
    76: "other_services",          # Automobile repair (NIPA 12, productive)
}

# ---- BLS hours datatype priority ----
# Datatype 33 (goods-friendly weekly hours): full 1948+ history for goods
# supersectors. Empty for services slugs in this cache.
# Datatype 07 (services-friendly weekly hours): 1964+ for all supersectors
# with fetched coverage; used as fallback when 33 is empty.

GOODS_SLUGS_WITH_DT33 = {
    "mining_logging", "construction", "manufacturing",
    "durable_goods", "nondurable_goods", "goods_producing",
}


def _supersector_to_ces_id(slug: str, datatype: str) -> str:
    """Map a BLS supersector slug + 2-char datatype to a CES series ID.

    Datatypes: '06' employment, '07' weekly hours (alt), '33' weekly hours (goods).
    """
    # 8-digit supersector codes (per BLS CES series ID format:
    # CES + 8-digit supersector + 2-digit datatype = 13 chars).
    slug_to_code = {
        "total_nonfarm":         "00000000",
        "total_private":         "05000000",
        "goods_producing":       "06000000",
        "service_providing":     "07000000",
        "private_service":       "08000000",
        "mining_logging":        "10000000",
        "construction":          "20000000",
        "manufacturing":         "30000000",
        "durable_goods":         "31000000",
        "nondurable_goods":      "32000000",
        "trade_transp_util":     "40000000",
        "wholesale_trade":       "41420000",
        "retail_trade":          "42000000",
        "transp_warehousing":    "43000000",
        "utilities":             "44000000",
        "information":           "50000000",
        "financial":             "55000000",
        "prof_business":         "60000000",
        "education_health":      "65000000",
        "leisure_hospitality":   "70000000",
        "other_services":        "80000000",
    }
    if slug not in slug_to_code:
        raise KeyError(f"Unknown BLS supersector slug: {slug!r}")
    return f"CES{slug_to_code[slug]}{datatype}"


def _load_bls_csv(slug: str, kind: str) -> pd.DataFrame:
    """Read one per-supersector BLS CES cache CSV.

    kind: 'employment' | 'hours' | 'hours_alt'.
    Returns DataFrame[year, value, series_id]; empty DF if file missing or
    all-NaN. Preserves NaN where the BLS publication has gaps.
    """
    path = BLS_CACHE_DIR / f"bls_ces_{slug}_{kind}.csv"
    if not path.exists():
        return pd.DataFrame(columns=["year", "value", "series_id"])
    df = pd.read_csv(path)
    if "year" not in df.columns or "value" not in df.columns:
        return pd.DataFrame(columns=["year", "value", "series_id"])
    df["year"] = df["year"].astype(int)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def _resolve_hours_series(slug: str) -> tuple[Optional[pd.DataFrame], Optional[str], str]:
    """Pick datatype 33 (goods) if non-empty, else 07 (alt). Returns
    (frame, ces_id, datatype_used)."""
    if slug in GOODS_SLUGS_WITH_DT33:
        h33 = _load_bls_csv(slug, "hours")
        if not h33.empty and h33["value"].notna().any():
            return h33, _supersector_to_ces_id(slug, "33"), "33"
    h07 = _load_bls_csv(slug, "hours_alt")
    if not h07.empty and h07["value"].notna().any():
        return h07, _supersector_to_ces_id(slug, "07"), "07"
    # Fall through: nothing usable
    return None, None, "none"


def _resolve_supersector_for_sector(sector_code: int, nipa_industry: int) -> Optional[str]:
    if sector_code in PER_SECTOR_SLUG_OVERRIDE:
        return PER_SECTOR_SLUG_OVERRIDE[sector_code]
    return NIPA_TO_BLS_SLUG.get(int(nipa_industry))


def _list_io_matrix_years() -> dict[str, list[int]]:
    """Provenance helper: list available IO matrix years by era."""
    sic_years = sorted({int(p.name[:4]) for p in IO_LABELED_DIR.glob("*_A_matrix_labeled.csv")})
    naics_years = sorted({int(p.name[:4]) for p in IO_LABELED_DIR.glob("*_A_matrix_naics_labeled.csv")})
    return {"sic_era": sic_years, "naics_era": naics_years}


def load_appendix_f(productive_filter: str) -> pd.DataFrame:
    """Load Appendix F Table F.1 filtered by productive partition.

    productive_filter: 'productive'   -> productive_share > 0.5
                       'unproductive' -> productive_share < 0.5 and not n/a
                       'all'          -> no filter (incl. n/a sectors)
    """
    if not APPENDIX_F.exists():
        raise FileNotFoundError(f"Appendix F missing: {APPENDIX_F}")
    f = pd.read_csv(APPENDIX_F)
    f["sector_code"] = f["sector_code"].astype(int)
    f["nipa_industry"] = f["nipa_industry"].astype(int)
    f["productive_share"] = pd.to_numeric(f["productive_share"], errors="coerce")
    if productive_filter == "productive":
        return f[f["productive_share"] > 0.5].copy().reset_index(drop=True)
    if productive_filter == "unproductive":
        return f[(f["productive_share"] < 0.5) & f["productive_share"].notna()].copy().reset_index(drop=True)
    if productive_filter == "all":
        return f
    raise ValueError(f"Unknown productive_filter: {productive_filter!r}")


def build_long_panel(productive_filter: str = "productive") -> pd.DataFrame:
    """Build the sector × year long panel of BLS employment + weekly hours
    for sectors matching `productive_filter` per Appendix F.

    Returns columns [sector_code, sector_name, nipa_industry, nipa_industry_name,
    productive_share, bls_supersector_slug, bls_employment_series_id,
    bls_hours_series_id, hours_datatype, year, employment_thousands,
    weekly_hours]. NaN preserved where BLS coverage is missing.
    """
    f = load_appendix_f(productive_filter)
    rows: list[dict] = []

    # Cache per-slug BLS frames to avoid re-reading 21+ files per sector.
    emp_cache: dict[str, pd.DataFrame] = {}
    hrs_cache: dict[str, tuple[Optional[pd.DataFrame], Optional[str], str]] = {}

    for _, sec in f.iterrows():
        sector_code = int(sec["sector_code"])
        slug = _resolve_supersector_for_sector(sector_code, int(sec["nipa_industry"]))
        if slug is None:
            # No CES match — emit one row per benchmark year span (1948-2024) with NaN.
            for yr in range(1948, 2025):
                rows.append({
                    "sector_code":              sector_code,
                    "sector_name":              sec["sector_name"],
                    "nipa_industry":            int(sec["nipa_industry"]),
                    "nipa_industry_name":       sec["nipa_industry_name"],
                    "productive_share":         float(sec["productive_share"])
                                                if pd.notna(sec["productive_share"]) else None,
                    "bls_supersector_slug":     None,
                    "bls_employment_series_id": None,
                    "bls_hours_series_id":      None,
                    "hours_datatype":           "none",
                    "year":                     yr,
                    "employment_thousands":     float("nan"),
                    "weekly_hours":             float("nan"),
                })
            continue

        if slug not in emp_cache:
            emp_cache[slug] = _load_bls_csv(slug, "employment")
        if slug not in hrs_cache:
            hrs_cache[slug] = _resolve_hours_series(slug)
        emp_df = emp_cache[slug]
        hrs_df, hrs_id, dt = hrs_cache[slug]
        emp_id = _supersector_to_ces_id(slug, "06")

        emp_lookup = dict(zip(emp_df["year"], emp_df["value"])) if not emp_df.empty else {}
        hrs_lookup = dict(zip(hrs_df["year"], hrs_df["value"])) if hrs_df is not None else {}
        years = sorted(set(emp_lookup.keys()) | set(hrs_lookup.keys()))
        if not years:
            years = list(range(1948, 2025))

        for yr in years:
            rows.append({
                "sector_code":              sector_code,
                "sector_name":              sec["sector_name"],
                "nipa_industry":            int(sec["nipa_industry"]),
                "nipa_industry_name":       sec["nipa_industry_name"],
                "productive_share":         float(sec["productive_share"])
                                            if pd.notna(sec["productive_share"]) else None,
                "bls_supersector_slug":     slug,
                "bls_employment_series_id": emp_id,
                "bls_hours_series_id":      hrs_id,
                "hours_datatype":           dt,
                "year":                     int(yr),
                "employment_thousands":     emp_lookup.get(yr, float("nan")),
                "weekly_hours":             hrs_lookup.get(yr, float("nan")),
            })

    out = pd.DataFrame(rows)
    out = out.sort_values(["sector_code", "year"]).reset_index(drop=True)
    return out


def load() -> dict:
    """Top-level loader: returns dict of all S701 raw inputs for P02_S701.

    Structure:
      {
        "panel":           DataFrame (productive sector × year),
        "appendix_f":      DataFrame (productive filter),
        "io_matrix_years": {"sic_era": [...], "naics_era": [...]},
        "sic_naics_bridge": DataFrame,
        "provenance": {...},
      }
    """
    panel = build_long_panel(productive_filter="productive")
    f = load_appendix_f("productive")
    bridge = pd.read_csv(SIC_NAICS_BRIDGE) if SIC_NAICS_BRIDGE.exists() else None
    return {
        "panel":            panel,
        "appendix_f":       f,
        "io_matrix_years":  _list_io_matrix_years(),
        "sic_naics_bridge": bridge,
        "provenance": {
            "series_id":         SERIES_ID,
            "subseries":         SUBSERIES,
            "productive_filter": "productive_share > 0.5",
            "bls_cache_dir":     str(BLS_CACHE_DIR),
            "appendix_f_path":   str(APPENDIX_F),
            "sic_naics_bridge":  str(SIC_NAICS_BRIDGE),
            "io_labeled_dir":    str(IO_LABELED_DIR),
            "hours_datatype_priority": "33_goods -> 07_services",
            "nipa_to_bls_slug":  {str(k): v for k, v in NIPA_TO_BLS_SLUG.items()},
            "per_sector_slug_override": {str(k): v for k, v in PER_SECTOR_SLUG_OVERRIDE.items()},
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
          f"{panel['sector_code'].nunique()} productive sectors; "
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
