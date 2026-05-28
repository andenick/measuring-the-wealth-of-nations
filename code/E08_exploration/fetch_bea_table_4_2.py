"""Fetch BEA Fixed Assets Table 4.2 (Current-Cost Gross Stock of Private Fixed Assets).

Used by VPR_S517_gross_vs_net to compare gross vs net capital stock K*.
Caches CSV to Inputs/ST2/Inputs/API_Data/BEA/fixed_assets_4_2_gross_stock.csv.
"""
from __future__ import annotations
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

PROJECT_ROOT = Path("D:/Arcanum/Projects/RMWND")
OUT_CSV = PROJECT_ROOT / "Inputs/ST2/Inputs/API_Data/BEA/fixed_assets_4_2_gross_stock.csv"
PROV_JSON = PROJECT_ROOT / "Inputs/ST2/Inputs/API_Data/BEA/provenance_fixed_assets_4_2.json"
ENV_FILE = PROJECT_ROOT / "Inputs/ST2/Technical/AnuData/data/user-inputs/api_keys.env"


def load_bea_key() -> str:
    key = os.environ.get("BEA_API_KEY", "").strip()
    if key:
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("BEA_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("BEA_API_KEY not available")


def fetch_table(api_key: str, table_name: str = "FAAt402") -> dict:
    url = "https://apps.bea.gov/api/data?" + urlencode({
        "UserID": api_key,
        "method": "GetData",
        "datasetname": "FixedAssets",
        "TableName": table_name,
        "Frequency": "A",
        "Year": "ALL",
        "ResultFormat": "JSON",
    })
    print(f"GET {url.replace(api_key, '<KEY>')}")
    with urlopen(url, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def write_csv(payload: dict, path: Path) -> int:
    results = payload.get("BEAAPI", {}).get("Results", {})
    if "Error" in results:
        raise RuntimeError(f"BEA API error: {results['Error']}")
    data = results.get("Data", [])
    if not data:
        raise RuntimeError(f"No data returned. Payload top-keys: {list(results.keys())}")
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = ["TableName", "SeriesCode", "LineNumber", "LineDescription",
            "TimePeriod", "METRIC_NAME", "CL_UNIT", "UNIT_MULT", "DataValue", "NoteRef"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for row in data:
            w.writerow({k: row.get(k, "") for k in cols})
    return len(data)


def main() -> int:
    try:
        key = load_bea_key()
    except RuntimeError as e:
        print(f"BLOCKED: {e}")
        return 2
    payload = fetch_table(key, "FAAt402")
    rows = write_csv(payload, OUT_CSV)
    prov = {
        "script": "fetch_bea_table_4_2.py",
        "project": "RMWND",
        "phase": "v1.1 Phase 3 (VPR_S517_gross_vs_net)",
        "api": "BEA Fixed Assets",
        "table_id": "FAAt402",
        "description": "Current-Cost Gross Stock of Private Fixed Assets (Fixed Assets 4.2)",
        "output_file": str(OUT_CSV.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "row_count": rows,
        "status": "success",
    }
    PROV_JSON.write_text(json.dumps(prov, indent=2))
    print(f"OK: {rows} rows -> {OUT_CSV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
