"""
L00_bls_fetch.py - Anu Framework v12.0 / RMWND v1.1 Phase 4

BLS CES fetch for Ch7 real-fix: production-worker employment AND
production-worker average weekly hours for the SIC/NAICS supersectors
that aggregate to the 85 SIC sectors in Shaikh & Tonak (1994) Appendix C.

Background
----------
The v1.0 Ch7 BLOCKER was that the existing BLS cache at
Inputs/ST2/Inputs/API_Data/BLS/bls_ces_production_workers.csv covers only
5 super-sectors (total private, goods, mining, construction, manufacturing)
and contains no weekly-hours data. The Ch7 real-fix requires per-sector
hp*_j = (Lp_j * weekly_hours_j) / X_j   [hr/$, producer prices]
which propagates into S701/S702/S703 via lambda* = hp* (I - app*)^{-1}.

This script fetches:
  * Production-worker employment (CES datatype 06) - thousands of workers
  * Production-worker average weekly hours (CES datatype 33) - hours/week

for ~16 NAICS supersectors that span 1948-2024 (BLS CES carries SIC-era
historical series under the same supersector codes; the underlying SIC->NAICS
bridge is handled internally by BLS).

API key
-------
Uses the registered BLS_API_KEY from Council/Robin (centralized) or the
ST2 AnuData env file. With a registered key the BLS public API v2 allows
500 queries/day and 50 series per request - far more than this script needs.

Outputs
-------
  Inputs/ST2/Inputs/API_Data/BLS/bls_ces_<supersector>_employment.csv
  Inputs/ST2/Inputs/API_Data/BLS/bls_ces_<supersector>_hours.csv
  Inputs/ST2/Inputs/API_Data/BLS/bls_ces_fetch_provenance.json

CONSTRAINTS
-----------
- Foreground only
- Idempotent: existing files skipped unless --force
- Honest about coverage gaps (some weekly-hours series only start 1964 or 1972)
- Does NOT touch series_registry.json, PIPELINE_STATE.json, ANU_LEDGER.json,
  PROVENANCE_INDEX.json, or SUBSERIES_PLAN
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library required (pip install requests)", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # bundle root
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "BLS"

# BLS API key: set the BLS_API_KEY environment variable, or place a
# `api_keys.env` file (KEY=VALUE lines) at the bundle root or in
# `data/user-inputs/`. Registration: https://data.bls.gov/registrationEngine/
ENV_CANDIDATES: List[Path] = [
    PROJECT_ROOT / "api_keys.env",
    PROJECT_ROOT / "data" / "user-inputs" / "api_keys.env",
]

BLS_API_BASE = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# -----------------------------------------------------------------------------
# Series specification
# -----------------------------------------------------------------------------
# CES Series ID format: CES<supersector_2digit><industry_6digit><datatype_2digit>
#   datatype 06 = production and nonsupervisory employees (employment, thousands)
#   datatype 33 = average weekly hours of production and nonsupervisory employees
#
# Supersector codes that span SIC and NAICS (CES historical alignment):
#   00 = total nonfarm                (post-1939)
#   05 = total private                (post-1939)
#   06 = goods-producing              (post-1939)
#   07 = service-providing            (post-1939)
#   08 = private service-providing    (post-1939)
#   10 = mining and logging           (post-1939)
#   20 = construction                 (post-1939)
#   30 = manufacturing                (post-1939)
#   31 = durable goods                (post-1939)
#   32 = nondurable goods             (post-1939)
#   40 = trade, transportation, utilities (post-1939, finer breakdown post-1964)
#   41 = wholesale trade              (post-1939)
#   42 = retail trade                 (post-1939)
#   43 = transportation and warehousing (post-1939)
#   44 = utilities                    (post-1939)
#   50 = information                  (post-1948)
#   55 = financial activities         (post-1939)
#   60 = professional and business services (post-1939)
#   65 = education and health services (post-1939)
#   70 = leisure and hospitality      (post-1939)
#   80 = other services               (post-1939)
#   90 = government                   (post-1939, NO production-worker breakdown - excluded)
#
# Datatype 06 (production workers) is NOT published for service-only supersectors
# (50, 55, 60, 65, 70, 80) and not for government. For those, BLS publishes
# datatype 06 only where "production AND nonsupervisory" makes sense.
# We attempt all and let the API tell us which fail (graceful degradation).

SUPERSECTORS: Dict[str, Dict[str, str]] = {
    "00000000": {"slug": "total_nonfarm",          "name": "Total nonfarm"},
    "05000000": {"slug": "total_private",          "name": "Total private"},
    "06000000": {"slug": "goods_producing",        "name": "Goods-producing"},
    "07000000": {"slug": "service_providing",      "name": "Service-providing"},
    "08000000": {"slug": "private_service",        "name": "Private service-providing"},
    "10000000": {"slug": "mining_logging",         "name": "Mining and logging"},
    "20000000": {"slug": "construction",           "name": "Construction"},
    "30000000": {"slug": "manufacturing",          "name": "Manufacturing"},
    "31000000": {"slug": "durable_goods",          "name": "Durable goods"},
    "32000000": {"slug": "nondurable_goods",       "name": "Nondurable goods"},
    "40000000": {"slug": "trade_transp_util",      "name": "Trade, transportation, and utilities"},
    "41420000": {"slug": "wholesale_trade",        "name": "Wholesale trade"},
    "42000000": {"slug": "retail_trade",           "name": "Retail trade"},
    "43000000": {"slug": "transp_warehousing",     "name": "Transportation and warehousing"},
    "44000000": {"slug": "utilities",              "name": "Utilities"},
    "50000000": {"slug": "information",            "name": "Information"},
    "55000000": {"slug": "financial",              "name": "Financial activities"},
    "60000000": {"slug": "prof_business",          "name": "Professional and business services"},
    "65000000": {"slug": "education_health",       "name": "Education and health services"},
    "70000000": {"slug": "leisure_hospitality",    "name": "Leisure and hospitality"},
    "80000000": {"slug": "other_services",         "name": "Other services"},
}

# Datatypes we need
# 06: Production and nonsupervisory employees (thousands)
# 07: Average weekly hours of production and nonsupervisory employees
#     (published for all supersectors including services; service-sector
#      coverage starts 1964)
# 33: Average weekly hours of production and nonsupervisory employees
#     (alternate code published for goods-producing supersectors back to 1948;
#      same conceptual variable as 07 but with deeper history for goods)
#
# For hours: we fetch BOTH 07 and 33 because the historical depth differs by
# sector. For goods (mining/construction/manufacturing/durable/nondurable/06),
# datatype 33 is published 1948+; for services, only datatype 07 is published
# and only 1964+. The construction step in P02 will prefer 33 where available
# and fall back to 07.
DATATYPES = {
    "06": "production_worker_employment",        # thousands of workers
    "07": "prodworker_weekly_hours_alt",         # alt hours code (covers services 1964+)
    "33": "prodworker_weekly_hours_goods",       # goods-sector hours, deep history 1948+
}

DATATYPE_TO_OUTPUT_SUFFIX = {
    "06": "employment",
    "07": "hours_alt",
    "33": "hours",
}


# -----------------------------------------------------------------------------
# API key resolution
# -----------------------------------------------------------------------------
def resolve_api_key() -> Optional[str]:
    """Try environment variable, then known env files. Return None if unfound."""
    # Direct env var first
    key = os.environ.get("BLS_API_KEY")
    if key and key.strip() and key.strip() != "your_bls_api_key_here":
        return key.strip()

    # Try dotenv files
    if load_dotenv is None:
        print("WARNING: python-dotenv not installed; only checking BLS_API_KEY env var",
              file=sys.stderr)
        return None

    for env_path in ENV_CANDIDATES:
        if not env_path.exists():
            continue
        # Parse manually so we don't pollute os.environ across files
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    k, _, v = line.partition("=")
                    if k.strip() == "BLS_API_KEY":
                        v = v.strip().strip('"').strip("'")
                        if v and v != "your_bls_api_key_here":
                            print(f"  Found BLS_API_KEY in {env_path}")
                            return v
        except Exception as e:
            print(f"  WARNING: could not read {env_path}: {e}", file=sys.stderr)
            continue
    return None


# -----------------------------------------------------------------------------
# BLS API fetch
# -----------------------------------------------------------------------------
def build_series_ids() -> List[str]:
    """Build the full list of series IDs from supersector x datatype cross."""
    ids = []
    for super_code in SUPERSECTORS.keys():
        for dt in DATATYPES.keys():
            ids.append(f"CES{super_code}{dt}")
    return ids


def fetch_chunk(
    api_key: str,
    series_ids: List[str],
    start_year: int,
    end_year: int,
    max_retries: int = 3,
) -> dict:
    """Fetch one BLS API call. Retries on 429/5xx with exponential backoff."""
    payload = {
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": api_key,
    }
    last_err = None
    for attempt in range(max_retries):
        try:
            r = requests.post(BLS_API_BASE, json=payload, timeout=90)
            if r.status_code == 429:
                wait = 30 * (2 ** attempt)
                print(f"    429 rate limit; sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            status = data.get("status")
            if status != "REQUEST_SUCCEEDED":
                msg = data.get("message") or ["unknown"]
                raise RuntimeError(f"BLS API status={status} msg={msg}")
            return data
        except Exception as e:
            last_err = e
            wait = 5 * (2 ** attempt)
            print(f"    attempt {attempt + 1} failed: {e}; sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"BLS fetch failed after {max_retries} retries: {last_err}")


def fetch_all(
    api_key: str,
    series_ids: List[str],
    start_year: int,
    end_year: int,
) -> Dict[str, Dict[int, float]]:
    """
    Fetch all series across years. BLS allows up to 50 series/request and
    up to 20-year spans/request. Returns sid -> {year -> annual_avg_value}.
    """
    # Aggregate monthly observations per sid per year, then annualize.
    monthly: Dict[str, Dict[int, List[float]]] = {sid: {} for sid in series_ids}

    # Chunk series (50/request) x year-spans (20yr/request)
    series_chunks = [series_ids[i : i + 50] for i in range(0, len(series_ids), 50)]
    for ci, sid_chunk in enumerate(series_chunks, 1):
        for yr in range(start_year, end_year + 1, 20):
            ye = min(yr + 19, end_year)
            print(f"  Chunk {ci}/{len(series_chunks)} years {yr}-{ye} "
                  f"({len(sid_chunk)} series)...")
            data = fetch_chunk(api_key, sid_chunk, yr, ye)
            for s in data.get("Results", {}).get("series", []):
                sid = s["seriesID"]
                if sid not in monthly:
                    monthly[sid] = {}
                for item in s.get("data", []):
                    period = item.get("period", "")
                    # Skip M13 (annual avg) and non-monthly
                    if not period.startswith("M") or period == "M13":
                        continue
                    try:
                        year = int(item["year"])
                        val = float(str(item["value"]).replace(",", ""))
                    except (KeyError, ValueError):
                        continue
                    monthly[sid].setdefault(year, []).append(val)

    # Annual averages (require >=6 months for a valid annual figure)
    annual: Dict[str, Dict[int, float]] = {}
    for sid, year_months in monthly.items():
        annual[sid] = {}
        for year, vals in year_months.items():
            if len(vals) >= 6:
                annual[sid][year] = round(sum(vals) / len(vals), 2)
    return annual


# -----------------------------------------------------------------------------
# Output writers
# -----------------------------------------------------------------------------
def write_per_supersector_csvs(
    annual: Dict[str, Dict[int, float]],
    output_dir: Path,
    start_year: int,
    end_year: int,
    force: bool,
) -> List[Path]:
    """
    Emit one CSV per (supersector, datatype) pair:
      bls_ces_<slug>_<employment|hours>.csv
    Each file has columns: year, value, series_id
    """
    written: List[Path] = []
    years = list(range(start_year, end_year + 1))
    for super_code, meta in SUPERSECTORS.items():
        for dt, dt_label in DATATYPES.items():
            sid = f"CES{super_code}{dt}"
            data = annual.get(sid, {})
            suffix = DATATYPE_TO_OUTPUT_SUFFIX[dt]
            out_path = output_dir / f"bls_ces_{meta['slug']}_{suffix}.csv"

            if out_path.exists() and not force:
                # Skip silently to be idempotent; still record as "present"
                written.append(out_path)
                continue

            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["year", "value", "series_id"])
                rows_written = 0
                for yr in years:
                    if yr in data:
                        w.writerow([yr, data[yr], sid])
                        rows_written += 1
                    else:
                        w.writerow([yr, "", sid])
            print(f"    Wrote {out_path.name} ({sum(1 for y in years if y in data)} "
                  f"observed / {len(years)} years)")
            written.append(out_path)
    return written


def write_provenance(
    output_dir: Path,
    api_key_source: str,
    start_year: int,
    end_year: int,
    annual: Dict[str, Dict[int, float]],
    written: List[Path],
) -> Path:
    """Emit fetch provenance with per-series coverage diagnostics."""
    coverage = {}
    for super_code, meta in SUPERSECTORS.items():
        for dt, dt_label in DATATYPES.items():
            sid = f"CES{super_code}{dt}"
            obs = annual.get(sid, {})
            obs_years = sorted(obs.keys())
            coverage[sid] = {
                "supersector": super_code,
                "supersector_name": meta["name"],
                "datatype": dt,
                "datatype_label": dt_label,
                "n_years": len(obs_years),
                "first_year": obs_years[0] if obs_years else None,
                "last_year": obs_years[-1] if obs_years else None,
                "fetched": len(obs_years) > 0,
            }
    fetched_count = sum(1 for c in coverage.values() if c["fetched"])
    prov = {
        "script": "Technical/code/L00_setup/L00_bls_fetch.py",
        "project": "RMWND",
        "version": "v1.1 Phase 4 (Ch7 real-fix Stage 5 sub-stage)",
        "api": "BLS Public API v2",
        "base_url": BLS_API_BASE,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "api_key_source": api_key_source,
        "start_year": start_year,
        "end_year": end_year,
        "supersector_count": len(SUPERSECTORS),
        "datatype_count": len(DATATYPES),
        "series_attempted": len(SUPERSECTORS) * len(DATATYPES),
        "series_fetched": fetched_count,
        "datatypes": {
            "06": "Production and nonsupervisory employees (thousands)",
            "07": "Average weekly hours of production and nonsupervisory employees "
                  "(services-friendly code, coverage 1964+)",
            "33": "Average weekly hours of production and nonsupervisory employees "
                  "(goods-friendly code, deep history 1948+)",
        },
        "supersectors": {
            code: {"slug": meta["slug"], "name": meta["name"]}
            for code, meta in SUPERSECTORS.items()
        },
        "coverage": coverage,
        "outputs": sorted(p.name for p in written),
        "notes": [
            "Datatype 06 (production workers) and datatype 33 (their weekly hours) "
            "are not published for some service-only supersectors. Empty CSVs are "
            "written for those to make the gap explicit.",
            "Supports Ch7 real-fix per Technical/Handoffs/CH7_REAL_FIX_PLAN.md: "
            "hp*_j = (Lp_j * weekly_hours_j) / X_j, feeding lambda* = hp* (I-app*)^{-1}.",
            "Does not modify series_registry.json, PIPELINE_STATE.json, ANU_LEDGER.json.",
        ],
    }
    prov_path = output_dir / "bls_ces_fetch_provenance.json"
    with open(prov_path, "w", encoding="utf-8") as f:
        json.dump(prov, f, indent=2)
    print(f"  Wrote {prov_path.name}")
    return prov_path


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-year", type=int, default=1948)
    parser.add_argument("--end-year", type=int, default=2024)
    parser.add_argument("--force", action="store_true",
                        help="overwrite existing CSVs")
    parser.add_argument("--dry-run", action="store_true",
                        help="only print plan, do not fetch")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    api_key = resolve_api_key()
    if not api_key:
        print("ERROR: BLS_API_KEY not found in env or any candidate file.",
              file=sys.stderr)
        print("Searched:", file=sys.stderr)
        for p in ENV_CANDIDATES:
            print(f"  - {p} (exists={p.exists()})", file=sys.stderr)
        print("\nRegister a free key at https://data.bls.gov/registrationEngine/",
              file=sys.stderr)
        return 2

    # Find which env file we used (for provenance)
    api_key_source = "BLS_API_KEY env var"
    for p in ENV_CANDIDATES:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    if api_key in f.read():
                        api_key_source = str(p)
                        break
            except Exception:
                continue

    series_ids = build_series_ids()
    print(f"Plan: fetch {len(series_ids)} series "
          f"({len(SUPERSECTORS)} supersectors x {len(DATATYPES)} datatypes) "
          f"for {args.start_year}-{args.end_year}")
    print(f"API key source: {api_key_source}")
    print(f"Output dir:     {OUTPUT_DIR}")

    if args.dry_run:
        print("\n--dry-run set; exiting without fetching.")
        return 0

    print("\nFetching from BLS...")
    annual = fetch_all(api_key, series_ids, args.start_year, args.end_year)

    print("\nWriting CSVs...")
    written = write_per_supersector_csvs(
        annual, OUTPUT_DIR, args.start_year, args.end_year, args.force
    )

    print("\nWriting provenance...")
    prov_path = write_provenance(
        OUTPUT_DIR, api_key_source, args.start_year, args.end_year, annual, written
    )

    fetched = sum(1 for sid in series_ids if annual.get(sid))
    print(f"\nDone. {fetched}/{len(series_ids)} series fetched. "
          f"Outputs in {OUTPUT_DIR}")
    return 0 if fetched > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
