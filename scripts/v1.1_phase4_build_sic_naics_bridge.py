"""
v1.1 Phase 4: Best-effort SIC<->NAICS bridge for RMWND.

CONTEXT: The project has no direct sector-level SIC<->NAICS concordance file.
Available concordances are:
  - io_85_to_nipa_13_concordance.csv : 85 BEA IO sectors -> NIPA 13 industries
    with SIC two-digit ranges per row and Shaikh-Tonak productive/unproductive
    classification.
  - naics_71_to_classification.csv   : 71 BEA-summary NAICS sector codes with
    Shaikh-Tonak productive/unproductive/trading/govt classification.
  - classification_crosswalks.xlsx   : ISIC3/ISIC4 -> NAICS (NOT SIC).

This bridge is therefore a CLASSIFICATION-LEVEL bridge: it joins the SIC-era
85 sector index with the NAICS-era 71 sector index via the shared
Shaikh-Tonak productive/unproductive taxonomy. It is NOT a sector-to-sector
crosswalk; building a true SIC->NAICS sector concordance is a multi-week
data-sourcing task (BEA NDP-87 to NAICS bridge tables).

Output: Technical/data/source/concordances/sic_naics_bridge.csv with columns:
  bea_io_85_code, bea_io_85_name, sic_range, st_classification,
  bea_naics_71_code, naics_71_st_classification,
  bridge_quality, notes
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path("D:/Arcanum/Projects/RMWND")
SRC1 = ROOT / "Inputs/ST2/Inputs/Concordances/io_85_to_nipa_13_concordance.csv"
SRC2 = ROOT / "Inputs/ST2/Inputs/Concordances/naics_71_to_classification.csv"
OUT_DIR = ROOT / "Technical/data/source/concordances"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "sic_naics_bridge.csv"


# Hand-curated SIC 2-digit range -> BEA NAICS-71 summary code mapping.
# Derived from BEA's published NDP-87 to NAICS bridge documentation
# (BEA "Concordance Between SIC-Based and NAICS-Based Industry Categories",
# https://www.bea.gov/industry/concordances). Coverage is best-effort and
# coarse: a single SIC range can map to multiple NAICS summary sectors.
SIC2_TO_NAICS71: dict[str, list[str]] = {
    "01":     ["111CA", "113FF"],            # ag, forestry
    "01-02":  ["111CA", "113FF"],
    "02":     ["111CA"],
    "07":     ["111CA"],
    "08":     ["113FF"],
    "09":     ["113FF"],
    "10":     ["212"],                       # metal mining
    "11-12":  ["212"],                       # coal mining
    "13":     ["211"],                       # oil & gas
    "14":     ["212", "213"],                # nonmetallic mining + support
    "15-17":  ["23"],                        # construction
    "19":     ["332"],                       # ordnance -> fab metal
    "20":     ["311FT"],                     # food
    "21":     ["311FT"],                     # tobacco
    "22-23":  ["313TT", "315AL"],            # textiles + apparel
    "24":     ["321"],                       # lumber/wood
    "25":     ["337"],                       # furniture
    "26":     ["322"],                       # paper
    "27":     ["323", "511"],                # printing/publishing -> print + info
    "28":     ["325"],                       # chemicals
    "29":     ["324"],                       # petroleum refining
    "30":     ["326"],                       # rubber/plastics
    "31":     ["316"],                       # leather (in 332 NAICS-71 lacks 316; fall back)
    "32":     ["327"],                       # stone/clay/glass
    "33":     ["331"],                       # primary metals
    "34":     ["332"],                       # fabricated metal
    "35":     ["333"],                       # industrial machinery
    "35-36":  ["333", "334", "335"],         # office computing + electrical
    "36":     ["335", "334"],                # electrical
    "37":     ["3361MV", "3364OT"],          # transport equip
    "38":     ["334"],                       # instruments
    "39":     ["339"],                       # misc mfg
    "40-47":  ["481", "482", "483", "484", "485", "486", "487OS", "493"],
    "48":     ["513", "514", "511"],         # comm/info
    "49":     ["22"],                        # utilities
    "50-51":  ["42"],                        # wholesale
    "52-59":  ["441", "445", "452", "4A0"],  # retail
    "58":     ["722"],                       # eating/drinking (NAICS reclass)
    "60-67":  ["521CI", "523", "524"],       # FIRE
    "65":     ["532RL", "ORE"],              # real estate
    "70":     ["721"],                       # hotels
    "73":     ["5411", "5412OP", "5415", "55", "561"],  # bus services
    "75":     ["811"],                       # auto repair (NAICS 811 -> 81 summary)
    "79":     ["711AS", "713"],              # amusements
    "80":     ["621", "622", "623", "624", "61"],  # health + ed
    "gov":    ["GFE", "GSLE"],               # government enterprises
    "import": [],
    "special":[],
}


def load_85() -> list[dict]:
    with SRC1.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_naics_class() -> dict[str, str]:
    out: dict[str, str] = {}
    with SRC2.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            out[row["naics_code"].strip()] = row["classification"].strip()
    return out


def main() -> None:
    rows85 = load_85()
    naics_class = load_naics_class()
    out_rows: list[dict] = []
    for r in rows85:
        sic_range = r["sic_range"].strip()
        targets = SIC2_TO_NAICS71.get(sic_range, [])
        if not targets:
            out_rows.append({
                "bea_io_85_code": r["io_sector"],
                "bea_io_85_name": r["io_sector_name"],
                "sic_range": sic_range,
                "st_classification": r["classification"],
                "bea_naics_71_code": "",
                "naics_71_st_classification": "",
                "bridge_quality": "unmapped",
                "notes": "no direct SIC<->NAICS mapping; classification only",
            })
            continue
        for t in targets:
            naics_c = naics_class.get(t, "unknown")
            agree = "agree" if (
                (naics_c == r["classification"]) or
                (naics_c == "trading" and r["classification"] == "unproductive") or
                (naics_c in ("govt_enterprise", "govt_admin") and r["classification"] in ("productive", "mixed"))
            ) else "disagree"
            out_rows.append({
                "bea_io_85_code": r["io_sector"],
                "bea_io_85_name": r["io_sector_name"],
                "sic_range": sic_range,
                "st_classification": r["classification"],
                "bea_naics_71_code": t,
                "naics_71_st_classification": naics_c,
                "bridge_quality": "coarse_aggregation",
                "notes": f"classification_{agree}",
            })
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print(f"Wrote {len(out_rows)} bridge rows to {OUT}")
    # Coverage report
    mapped = sum(1 for r in out_rows if r["bea_naics_71_code"])
    unmapped85 = {r["bea_io_85_code"] for r in out_rows if not r["bea_naics_71_code"]}
    print(f"Mapped rows: {mapped} / {len(out_rows)}")
    print(f"Unmapped IO-85 sectors: {sorted(unmapped85, key=int)}")


if __name__ == "__main__":
    main()
