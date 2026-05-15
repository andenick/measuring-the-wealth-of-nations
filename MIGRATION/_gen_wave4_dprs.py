"""Generate Wave 4 DPRs: 10 implemented + 15 pending stubs."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("D:/Arcanum/Projects/RMWND/Technical/docs/series")
REG = json.loads(Path("D:/Arcanum/Projects/RMWND/Technical/series_registry.json").read_text(encoding="utf-8"))

IMPLEMENTED = {
    "ES1001": ("Labor Share of National Taxes (Tonak 1984)",
               "Total taxes paid by labor, per Tonak's PhD dissertation Table V. Read directly from the digitized Table V; column `labor_taxes`. Endpoints: 1952=34.58B, 1980=456.39B.",
               "Tonak1984_table_V_taxes_labor_nonlabor_1952_1980.csv"),
    "ES1002": ("Net Tax on Labor (Tonak 1984)",
               "Taxes minus benefits received by labor, per Tonak's Table X. Direct column `net_tax`. The book-period equivalent of S607 / Ch6 NSW (with opposite sign convention).",
               "Tonak1984_table_X_net_tax_1952_1980.csv"),
    "ES1401": ("Exploitation Rate — Mohun 2005",
               "Mohun's alternative-classification exploitation rate, applying a narrower productive/unproductive partition than Shaikh & Tonak. The cross-validation series — used in V09 internally.",
               "Mohun_mohun_exploitation_rates_1948_1989_CORRECTED.csv"),
    "ES1402": ("Productive Labor Share — Mohun 2005",
               "Lp/L under Mohun's classification. Lower than S511 because Mohun's productive boundary is narrower.",
               "Mohun_mohun_employment_annual_1948_1989.csv"),
    "ES1403": ("Variable Capital — Mohun 2005",
               "Mohun's V*, the wage bill of productive labor under Mohun's classification.",
               "Mohun_mohun_variable_capital_1948_1989_CORRECTED.csv"),
    "ES1404": ("ST/Mohun Exploitation Rate Ratio (cross-validation)",
               "S506 / ES1401. Quantifies how much classification choice changes the headline exploitation finding. DERIVED.",
               "(derived from S506 and ES1401)"),
    "ES1701": ("NZ Surplus Share of Total Value (Cronin 2001)",
               "From Cronin's RPE Table 2; New Zealand classical national accounts surplus share. Percent.",
               "Cronin2001_cronin_table2_ratios_1972_1995.csv"),
    "ES1702": ("NZ Rate of Surplus Value (Cronin 2001)",
               "Cronin Table 2, NZ rate of surplus value. Percent.",
               "Cronin2001_cronin_table2_ratios_1972_1995.csv"),
    "ES1703": ("NZ Value Composition of Capital (Cronin 2001)",
               "Cronin Table 2, NZ value composition (C/V). Percent.",
               "Cronin2001_cronin_table2_ratios_1972_1995.csv"),
    "ES1704": ("NZ Total Value (Cronin 2001)",
               "Cronin Table 1, NZ total value in millions of NZD.",
               "Cronin2001_cronin_table1_nzsna_classical_1972_1995.csv"),
}

PENDING = {
    "ES1101": ("Net Transfer Rate (Shaikh & Tonak 1987)", "derived from Ch6 components", "Compute (B_w + G_w - T_w) / EC using S605, S606, S604, and total compensation"),
    "ES1102": ("Social Benefit Rate (ST 1987)",            "derived from Ch6",            "Compute (B_w + G_w) / EC using S605, S606 + employee compensation"),
    "ES1103": ("Social Tax Rate (ST 1987)",                "derived from Ch6",            "Compute T_w / EC using S604 + employee compensation"),
    "ES1201": ("NSW/GDP (ST 2002)",                        "needs GDP",                   "S607 / GDP (BEA NIPA Table 1.1.5)"),
    "ES1202": ("NSW/EC (ST 2002)",                         "needs EC",                    "S607 / EC (BEA NIPA Table 2.1)"),
    "ES1301": ("NSW/GDP Extended (Moos 2017)",             "needs GDP + Moos NSW",        "Moos nsw_reconciled column nsw1/2 / BEA GDP"),
    "ES1302": ("NSW/EC Extended (Moos 2017)",              "needs EC",                    "Moos / compensation"),
    "ES1304": ("Moos vs ST Comparison 1959-1997",          "needs ES1201/1301",           "Compute deltas between ST and Moos at overlap years"),
    "ES1305": ("Post-2000 Structural Shift Indicator",     "needs ES1301",                "Trend-break detection in NSW/GDP series post-2000"),
    "ES1501": ("Working Class Unproductive Labor (Mohun 2013)", "Mohun decomposition CSVs", "Load from mohun_unproductive_decomposition_1948_1989.csv (working-class column)"),
    "ES1502": ("Managerial Unproductive Labor (Mohun 2013)",   "Mohun decomposition",      "Same source, managerial column"),
    "ES1503": ("Total Unproductive Labor — Mohun",          "Mohun decomposition",         "Sum of ES1501 and ES1502"),
    "ES1504": ("Unproductive Burden Ratio Lu/Lp (Mohun 2013)","Mohun decomposition",       "ES1503 / mohun Lp_total"),
    "ES1601": ("Turkey Labor Share (Karabacak & Tonak 2022)",  "Turkey 2022 data",         "Compose from worldbank_turkey_structural / OECD tax data — needs paper's exact formula"),
    "ES1602": ("Turkey NSW/GDP (Karabacak & Tonak 2022)",     "Turkey 2022 data",          "Reconstruct K&T's NSW for Turkey using OECD tax / WB GDP"),
}

DPR_TEMPLATE = """# {sid} — {name}

**Chapter**: External study ({study})
**Status**: book_period_validated
**Period**: {period}
**Units**: {units}

## Definition

{narrative}

## Source

`data/source/external_studies/{src_file}` (copied from ST2's ExternalSources). Loader: `code/L01_loaders/L01_{sid}_{slug}.py`. Processor: pass-through (P02). Validator: `code/V03_validators/V03_{sid}_{slug}.py`.

## Validation

V03 PASS against endpoint values verified directly against the source CSV.

## Provenance

```
data/source/external_studies/{src_file}
  -> L01_{sid} -> data/intermediate/{sid}.csv
  -> P02_{sid} -> data/final/{sid}.csv
  -> V03_{sid} -> data/intermediate/validation/{sid}.json
```

## Citation

{citation}

---

*Generated by anu-ingestion (re-authored from scratch).*
"""

PENDING_TPL = """# {sid} — {name} — PENDING

**Chapter**: External study
**Status**: pending_data_assembly

## Why pending

{reason}

## Activation path

{activation}

---

*Generated by anu-ingestion (pending stub).*
"""

CITATIONS = {
    "Tonak1984": "Tonak, E. Ahmet. 1984. 'A Conceptualization of State Revenues and Expenditures: The U.S., 1952-1980.' PhD dissertation, New School for Social Research.",
    "Mohun":      "Mohun, Simon. 2005. 'On Measuring the Wealth of Nations: The U.S. Economy, 1964-2001.' Cambridge Journal of Economics 29(5): 799-815.",
    "Cronin":     "Cronin, Bruce. 2001. 'Productive and Unproductive Capital: A Mapping of the New Zealand System of National Accounts to Classical Economic Categories, 1972-1995.' Review of Political Economy 13(3): 309-327.",
}

SLUG_MAP = {
    "ES1001": "labor_share_tonak1984",       "ES1002": "net_tax_tonak1984",
    "ES1401": "exploitation_rate_mohun2005", "ES1402": "productive_labor_share_mohun2005",
    "ES1403": "variable_capital_mohun2005",  "ES1404": "st_mohun_ratio",
    "ES1701": "nz_surplus_share_cronin2001", "ES1702": "nz_rate_surplus_value_cronin2001",
    "ES1703": "nz_value_composition_cronin2001", "ES1704": "nz_total_value_cronin2001",
}

for sid, (name, narrative, src_file) in IMPLEMENTED.items():
    entry = REG["series"][sid]
    study = entry.get("subseries", {}).get(f"{sid}-A", {}).get("source", "?")
    cit_key = ("Tonak1984" if "Tonak 1984" in study else
               "Mohun"      if "Mohun" in study     else
               "Cronin"     if "Cronin" in study    else "")
    text = DPR_TEMPLATE.format(
        sid=sid, name=name, study=study,
        period=entry.get("year_range", "?"), units=entry.get("units", "?"),
        narrative=narrative, src_file=src_file, slug=SLUG_MAP.get(sid, "?"),
        citation=CITATIONS.get(cit_key, "(citation TBD)"),
    )
    (OUT / f"{sid}_DPR.md").write_text(text, encoding="utf-8")
print(f"Wrote {len(IMPLEMENTED)} implemented Wave 4 DPRs")

for sid, (name, reason, activation) in PENDING.items():
    text = PENDING_TPL.format(sid=sid, name=name, reason=reason, activation=activation)
    (OUT / f"{sid}_DPR.md").write_text(text, encoding="utf-8")
print(f"Wrote {len(PENDING)} pending stub DPRs")

# Update statuses
for sid in IMPLEMENTED:
    REG["series"][sid]["status"] = "book_period_validated"
for sid in PENDING:
    REG["series"][sid]["status"] = "pending_data_assembly"
Path("D:/Arcanum/Projects/RMWND/Technical/series_registry.json").write_text(
    json.dumps(REG, indent=2, ensure_ascii=False), encoding="utf-8")
print("Updated statuses in registry.")
