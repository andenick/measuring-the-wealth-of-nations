"""Step 3: Build detail-level NAICS classification for 412 industries.

Uses Shaikh & Tonak (1994) Appendix F rules:
- Productive: creation/transformation of use values (agriculture, mining, manufacturing,
  construction, transportation, utilities, health, education, entertainment, accommodation)
- Trading: circulation of commodities (wholesale, retail)
- Unproductive: FIRE, real estate, professional services, management, admin
- Government: federal and state/local government

Output: updates config/classifications.json with naics_detail_412 section.
"""
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / "data" / "user-inputs" / "api_keys.env")

BEA_KEY = os.environ.get("BEA_API_KEY", "")
BASE_URL = "https://apps.bea.gov/api/data"


def fetch_2017_detail():
    """Fetch 2017 detail-level gross output to get industry list."""
    cache = ROOT / "data" / "cache" / "bea_underlying_go_detail_2017.json"
    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        params = {
            "UserID": BEA_KEY,
            "method": "GetData",
            "DataSetName": "UnderlyingGDPbyIndustry",
            "TableID": "237",
            "Frequency": "A",
            "Year": "2017",
            "Industry": "ALL",
            "ResultFormat": "JSON",
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        cache.parent.mkdir(parents=True, exist_ok=True)
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)

    results = data.get("BEAAPI", {}).get("Results", {})
    if isinstance(results, list) and results:
        return results[0].get("Data", [])
    elif isinstance(results, dict):
        return results.get("Data", [])
    return []


def classify_industry(code: str, desc: str) -> str:
    """Classify a NAICS industry based on Appendix F rules.

    Rules (Shaikh & Tonak 1994):
    - PRODUCTIVE: Agriculture, mining, utilities, construction, manufacturing,
      transportation/warehousing, information (media production), waste management,
      education, health care, arts/entertainment, accommodation/food, other services
    - TRADING: Wholesale trade, retail trade
    - UNPRODUCTIVE: Finance, insurance, real estate, rental/leasing, professional services,
      management of companies, administrative services (except waste), publishing (non-physical)
    - GOVERNMENT: Federal/state/local government
    """
    desc_lower = desc.lower()
    c = code.strip()

    # Government codes
    if c.startswith("S0") or c.startswith("GF") or c.startswith("GS"):
        return "government"
    if "government" in desc_lower and ("federal" in desc_lower or "state" in desc_lower):
        return "government"

    # Agriculture (11xxxx)
    if c.startswith("11"):
        return "productive"

    # Mining (21xxxx)
    if c.startswith("21"):
        return "productive"

    # Utilities (22xxxx)
    if c.startswith("22"):
        return "productive"

    # Construction (23xxxx)
    if c.startswith("23"):
        return "productive"

    # Manufacturing (31xxxx - 33xxxx)
    if c[0] == "3" and len(c) >= 2 and c[1] in "0123":
        return "productive"
    if c.startswith("31") or c.startswith("32") or c.startswith("33"):
        return "productive"

    # Wholesale trade (42xxxx)
    if c.startswith("42"):
        return "trading"

    # Retail trade (44xxxx - 45xxxx)
    if c.startswith("44") or c.startswith("45"):
        return "trading"

    # Transportation and warehousing (48xxxx - 49xxxx)
    if c.startswith("48") or c.startswith("49"):
        return "productive"

    # Information (51xxxx) - split per book's SIC classification:
    # SIC 27 (Printing & Publishing) = Manufacturing = PRODUCTIVE
    # SIC 48 (Communications) = PRODUCTIVE
    # SIC 73 (Computer/data processing services) = UNPRODUCTIVE
    if c.startswith("51"):
        # Publishing (newspapers, books, periodicals, software) = productive
        # Was SIC 27 "Printing and Publishing" (Manufacturing)
        if c.startswith("5111") or c.startswith("5112"):
            return "productive"
        # Motion pictures, sound recording = productive (physical media creation)
        if c.startswith("512"):
            return "productive"
        # Broadcasting, cable programming = productive (content production)
        # Was SIC 484x (Cable/pay TV) within SIC 48 (Communications)
        if c.startswith("5151") or c.startswith("5152"):
            return "productive"
        # Telecommunications = productive
        # Was SIC 48 (Communications) = PRODUCTIVE in book
        if c.startswith("517"):
            return "productive"
        # Internet publishing/broadcasting = productive (content creation)
        if c.startswith("5191"):
            return "productive"
        # Data processing, hosting (SIC 737 = business services = unproductive)
        if c.startswith("518"):
            return "unproductive"
        # Other information services = unproductive
        return "unproductive"

    # Finance and insurance (52xxxx)
    if c.startswith("52"):
        return "unproductive"

    # Real estate (53xxxx)
    if c.startswith("53"):
        return "unproductive"

    # Professional, scientific, technical services (54xxxx)
    if c.startswith("54"):
        return "unproductive"

    # Management of companies (55xxxx)
    if c.startswith("55"):
        return "unproductive"

    # Administrative and support services (56xxxx)
    if c.startswith("56"):
        # Waste management and remediation = productive (physical transformation)
        if c.startswith("562"):
            return "productive"
        # All other admin = unproductive
        return "unproductive"

    # Educational services (61xxxx)
    if c.startswith("61"):
        return "productive"

    # Health care and social assistance (62xxxx)
    if c.startswith("62"):
        return "productive"

    # Arts, entertainment, recreation (71xxxx)
    if c.startswith("71"):
        return "productive"

    # Accommodation and food services (72xxxx)
    if c.startswith("72"):
        return "productive"

    # Other services (81xxxx)
    if c.startswith("81"):
        return "productive"

    # Owner-occupied and tenant-occupied housing (special BEA codes)
    if "housing" in desc_lower or c.startswith("531HS"):
        return "unproductive"

    # Catch-all for BEA composite codes
    if "real estate" in desc_lower or "rental" in desc_lower:
        return "unproductive"
    if "wholesale" in desc_lower:
        return "trading"
    if "retail" in desc_lower:
        return "trading"
    if "insurance" in desc_lower or "financial" in desc_lower or "banking" in desc_lower:
        return "unproductive"
    if "legal" in desc_lower or "accounting" in desc_lower:
        return "unproductive"
    if "management" in desc_lower and "waste" not in desc_lower:
        return "unproductive"

    # Manufacturing composite codes
    if "manufacturing" in desc_lower or "products" in desc_lower:
        return "productive"

    # Default: productive (conservative - includes anything creating use values)
    print(f"  WARNING: Unclassified industry {c}: {desc} -> defaulting to productive")
    return "productive"


def main():
    print("Building detail-level NAICS classification (412 industries)...")
    records = fetch_2017_detail()
    print(f"  Fetched {len(records)} records for 2017")

    classification = {}
    descriptions = {}
    for r in records:
        ind = r.get("Industry", "").strip()
        desc = r.get("IndustrYDescription", r.get("IndustryDescription", "")).strip()
        if not ind:
            continue
        descriptions[ind] = desc
        classification[ind] = classify_industry(ind, desc)

    # Summary
    counts = {}
    for v in classification.values():
        counts[v] = counts.get(v, 0) + 1
    print(f"\n  Classification summary:")
    for k, v in sorted(counts.items()):
        print(f"    {k}: {v} industries")
    print(f"    TOTAL: {sum(counts.values())}")

    # Compute GO shares
    go_by_class = {"productive": 0, "trading": 0, "unproductive": 0, "government": 0}
    total_go = 0
    for r in records:
        ind = r.get("Industry", "").strip()
        val_str = str(r.get("DataValue", "")).replace(",", "").strip()
        if not ind or not val_str:
            continue
        try:
            val = float(val_str)
        except ValueError:
            continue
        cls = classification.get(ind, "unknown")
        if cls in go_by_class:
            go_by_class[cls] += val
        total_go += val

    print(f"\n  2017 Gross Output by class (billions $):")
    for cls, go in sorted(go_by_class.items()):
        pct = 100 * go / total_go if total_go > 0 else 0
        print(f"    {cls}: ${go:,.1f}B ({pct:.1f}%)")
    print(f"    TOTAL: ${total_go:,.1f}B")

    tp_star = go_by_class["productive"] + go_by_class["trading"]
    gdp_2017 = 19485.4  # BEA GDP 2017 in billions
    print(f"\n  TP* (productive + trading GO): ${tp_star:,.1f}B")
    print(f"  GDP (2017): ${gdp_2017:,.1f}B")
    print(f"  TP*/GDP ratio: {tp_star / gdp_2017:.3f}")
    print(f"  Book TP*/GDP (1989): ~1.62")

    # Save classification
    out_path = ROOT / "config" / "naics_detail_classification.json"
    output = {
        "_doc": "412-industry NAICS detail classification from UnderlyingGDPbyIndustry TableID=237. Appendix F rules.",
        "_source": "Shaikh & Tonak (1994) Appendix F: Production = creation/transformation of use values",
        "classification": classification,
        "descriptions": descriptions,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\n  [SAVED] {out_path}")

    # Also print some diagnostic: which unproductive industries have highest GO?
    print(f"\n  Top 15 UNPRODUCTIVE industries by GO:")
    unprod = []
    for r in records:
        ind = r.get("Industry", "").strip()
        val_str = str(r.get("DataValue", "")).replace(",", "").strip()
        if not ind or not val_str:
            continue
        try:
            val = float(val_str)
        except ValueError:
            continue
        if classification.get(ind) == "unproductive":
            unprod.append((ind, val, descriptions.get(ind, "")))
    unprod.sort(key=lambda x: -x[1])
    for ind, val, desc in unprod[:15]:
        print(f"    {ind}: ${val:,.1f}B ({desc})")

    print(f"\n  Top 15 PRODUCTIVE industries by GO:")
    prod = []
    for r in records:
        ind = r.get("Industry", "").strip()
        val_str = str(r.get("DataValue", "")).replace(",", "").strip()
        if not ind or not val_str:
            continue
        try:
            val = float(val_str)
        except ValueError:
            continue
        if classification.get(ind) == "productive":
            prod.append((ind, val, descriptions.get(ind, "")))
    prod.sort(key=lambda x: -x[1])
    for ind, val, desc in prod[:15]:
        print(f"    {ind}: ${val:,.1f}B ({desc})")


if __name__ == "__main__":
    main()
