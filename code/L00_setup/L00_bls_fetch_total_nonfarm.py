"""
L00_bls_fetch_total_nonfarm.py - RMWND REVIEW_2026-07 item D2 (S515/S516 seam redesign)

Fetch BLS CES **total nonfarm ALL EMPLOYEES INCLUDING GOVERNMENT** (series
CES0000000001) into the project's BLS cache. This is the total-employment
universe the Shaikh-Tonak book's L refers to (Table 5.5 / Appendix F: total
labor L over ALL sectors, explicitly including the government "dummy" and
trade/finance — FULL_TEXT.md L449/L295).

Why a new fetch
---------------
The existing 5-super-sector cache (bls_ces_production_workers.csv) holds only
CES0500000001 (total PRIVATE all employees). Building the extension L on that
private universe drops government employment (~16.3M workers in 1989) and drove
the dominant -19.7% L break at the 1989/1990 seam documented in
internal-review-notes_2026-07/S515_S516_SEAM_REDESIGN.md. CES0000000001 = total
nonfarm incl. government is the correct establishment-side total; it is
re-anchored to the book L at 1989 by the P02_S515/P02_S516 processors.

Caching pattern
---------------
Mirrors code/L00_setup/L00_bls_fetch.py (same API-key resolution, chunked
BLS Public API v2 POST, monthly->annual averaging requiring >=6 months, and an
idempotent-unless--force CSV writer). Output is one long CSV plus a provenance
JSON, alongside the existing per-super-sector caches.

Output
------
  data/raw/Inputs/API_Data/BLS/bls_ces_total_nonfarm_all_employees.csv
      columns: year, value, series_id   (value = thousands of employees)
  data/raw/Inputs/API_Data/BLS/bls_ces_total_nonfarm_all_employees_provenance.json

CONSTRAINTS
-----------
- Foreground only; idempotent (skip if output exists unless --force).
- Does NOT touch series_registry.json, PIPELINE_STATE.json, ANU_LEDGER.json,
  the canonical bls_ces_production_workers.csv, or any other cache.
- Real fetched data only. On API failure the script exits non-zero and writes
  nothing (no placeholder rows).
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


PROJECT_ROOT = Path("(local path)")
OUTPUT_DIR = PROJECT_ROOT / "Inputs" / "predecessor-build" / "Inputs" / "API_Data" / "BLS"

ENV_CANDIDATES: List[Path] = [
    Path("(local path)"),
    PROJECT_ROOT / "data/raw/Technical/AnuData/data/user-inputs/api_keys.env",
    Path("(local path)"),
]

BLS_API_BASE = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# CES total nonfarm, ALL EMPLOYEES (datatype 01), incl. government supersector.
SERIES_ID = "CES0000000001"
OUTPUT_CSV = OUTPUT_DIR / "bls_ces_total_nonfarm_all_employees.csv"
PROV_JSON = OUTPUT_DIR / "bls_ces_total_nonfarm_all_employees_provenance.json"


def resolve_api_key() -> tuple[Optional[str], str]:
    """Return (key, source). Direct env var first, then known env files."""
    key = os.environ.get("BLS_API_KEY")
    if key and key.strip() and key.strip() != "your_bls_api_key_here":
        return key.strip(), "BLS_API_KEY env var"

    for env_path in ENV_CANDIDATES:
        if not env_path.exists():
            continue
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, _, v = line.partition("=")
                    if k.strip() == "BLS_API_KEY":
                        v = v.strip().strip('"').strip("'")
                        if v and v != "your_bls_api_key_here":
                            return v, str(env_path)
        except Exception as e:
            print(f"  WARNING: could not read {env_path}: {e}", file=sys.stderr)
            continue
    return None, ""


def fetch_chunk(api_key: str, start_year: int, end_year: int, max_retries: int = 3) -> dict:
    """Fetch one BLS API call for SERIES_ID. Retries on 429/5xx with backoff."""
    payload = {
        "seriesid": [SERIES_ID],
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
                raise RuntimeError(f"BLS API status={status} msg={data.get('message')}")
            return data
        except Exception as e:
            last_err = e
            wait = 5 * (2 ** attempt)
            print(f"    attempt {attempt + 1} failed: {e}; sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"BLS fetch failed after {max_retries} retries: {last_err}")


def fetch_annual(api_key: str, start_year: int, end_year: int) -> Dict[int, float]:
    """Fetch CES0000000001 across years; return {year: annual_avg_thousands}.

    Monthly observations (M01-M12) averaged; require >=6 months for a valid
    annual figure (matches L00_bls_fetch.py).
    """
    monthly: Dict[int, List[float]] = {}
    # BLS allows up to 20-year spans per request.
    for yr in range(start_year, end_year + 1, 20):
        ye = min(yr + 19, end_year)
        print(f"  Fetching {SERIES_ID} {yr}-{ye}...")
        data = fetch_chunk(api_key, yr, ye)
        for s in data.get("Results", {}).get("series", []):
            if s.get("seriesID") != SERIES_ID:
                continue
            for item in s.get("data", []):
                period = item.get("period", "")
                if not period.startswith("M") or period == "M13":
                    continue
                try:
                    year = int(item["year"])
                    val = float(str(item["value"]).replace(",", ""))
                except (KeyError, ValueError):
                    continue
                monthly.setdefault(year, []).append(val)
    annual: Dict[int, float] = {}
    for year, vals in monthly.items():
        if len(vals) >= 6:
            annual[year] = round(sum(vals) / len(vals), 2)
    return annual


def write_csv(annual: Dict[int, float], start_year: int, end_year: int) -> Path:
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "value", "series_id"])
        for yr in range(start_year, end_year + 1):
            w.writerow([yr, annual.get(yr, ""), SERIES_ID])
    n = sum(1 for y in range(start_year, end_year + 1) if y in annual)
    print(f"    Wrote {OUTPUT_CSV.name} ({n} observed / {end_year - start_year + 1} years)")
    return OUTPUT_CSV


def write_provenance(annual: Dict[int, float], key_source: str, start_year: int, end_year: int) -> Path:
    obs_years = sorted(annual.keys())
    prov = {
        "script": "Technical/code/L00_setup/L00_bls_fetch_total_nonfarm.py",
        "project": "RMWND",
        "purpose": "REVIEW_2026-07 D2 S515/S516 seam redesign: total-employment L incl. government",
        "api": "BLS Public API v2",
        "base_url": BLS_API_BASE,
        "series_id": SERIES_ID,
        "series_description": "CES total nonfarm, all employees, incl. government (thousands)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "api_key_source": key_source,
        "start_year": start_year,
        "end_year": end_year,
        "n_years_observed": len(obs_years),
        "first_year": obs_years[0] if obs_years else None,
        "last_year": obs_years[-1] if obs_years else None,
        "value_1989": annual.get(1989),
        "value_1990": annual.get(1990),
        "annualization": "mean of monthly M01-M12, require >=6 months",
        "output": OUTPUT_CSV.name,
        "notes": [
            "Book L (Shaikh-Tonak 1994 Table 5.5/Appendix F) is total employment over ALL "
            "sectors incl. government (FULL_TEXT.md L449/L295). CES0000000001 is the "
            "establishment-side total nonfarm incl. government; it excludes self-employed "
            "and agriculture, which the P02 re-anchor (multiplicative level-splice @1989) "
            "corrects at the anchor. Residual growth-basis concept gap = registered DIV.",
            "Does not modify series_registry.json or bls_ces_production_workers.csv.",
        ],
    }
    PROV_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"  Wrote {PROV_JSON.name}")
    return PROV_JSON


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-year", type=int, default=1948)
    parser.add_argument("--end-year", type=int, default=2024)
    parser.add_argument("--force", action="store_true", help="overwrite existing CSV")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_CSV.exists() and not args.force:
        print(f"Idempotent: {OUTPUT_CSV.name} already present; use --force to refetch.")
        return 0

    api_key, key_source = resolve_api_key()
    if not api_key:
        print("ERROR: BLS_API_KEY not found in env or any candidate file.", file=sys.stderr)
        for p in ENV_CANDIDATES:
            print(f"  - {p} (exists={p.exists()})", file=sys.stderr)
        return 2

    print(f"Fetching {SERIES_ID} for {args.start_year}-{args.end_year}")
    print(f"API key source: {key_source}")
    annual = fetch_annual(api_key, args.start_year, args.end_year)
    if not annual:
        print("ERROR: no observations returned; writing nothing.", file=sys.stderr)
        return 1

    write_csv(annual, args.start_year, args.end_year)
    write_provenance(annual, key_source, args.start_year, args.end_year)
    print(f"\nDone. {len(annual)} annual observations. 1989={annual.get(1989)} 1990={annual.get(1990)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
