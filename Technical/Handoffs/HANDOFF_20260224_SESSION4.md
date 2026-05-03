# HANDOFF — Session 4 (February 24, 2026)

## What Was Done

Executed all 5 API pull scripts with live API keys (BEA, BLS, FRED). Pulled real government data to replace placeholder data. Validated outputs. Updated infrastructure.

### Files Created (20)
- **13 BEA CSVs** in `Inputs/API_Data/BEA/`:
  - `nipa_1_7_5_gross_output_by_industry.csv` (3,254 rows, 1929-2025) — actually "Relation of GDP, GNI, NNP, NI, PI"
  - `nipa_6_2D_compensation_by_industry.csv` (2,673 rows, 1998-2024)
  - `nipa_6_4D_ftpt_by_industry.csv` (2,619 rows, 1998-2024)
  - `nipa_6_5D_fte_by_industry.csv` (2,619 rows, 1998-2024)
  - `nipa_6_10D_employer_contributions.csv` (540 rows, 1998-2024)
  - `nipa_2_1_personal_income.csv` (4,074 rows, 1929-2025)
  - `nipa_3_1_govt_receipts_expenditures.csv` (3,815 rows, 1929-2025)
  - `nipa_3_2_federal_govt.csv` (4,235 rows, 1929-2025)
  - `nipa_3_3_state_local_govt.csv` (3,886 rows, 1929-2025)
  - `fixed_assets_4_1_net_stock.csv` (7,600 rows, 1925-2024)
  - `gdp_by_industry_gross_output.csv` (2,800 rows, 1997-2024)
  - `gdp_by_industry_value_added.csv` (2,800 rows, 1997-2024)
  - `gdp_by_industry_va_components.csv` (11,088 rows, 1997-2024)
- **3 BEA provenance files**: `provenance.json`, `provenance_ch06.json`, `provenance_fixed_assets.json`
- **1 BLS CSV**: `bls_ces_production_workers.csv` (77 rows, 1948-2024) + `provenance.json`
- **1 FRED CSV**: `fred_tcu_capacity_utilization.csv` (59 rows, 1967-2025) + `provenance.json`

### Files Modified (8)
- `.env` — added BLS_API_KEY and FRED_API_KEY
- `pull_bea_nipa_ch05.py` — dotenv loading + corrected table names (B→D variants)
- `pull_bea_nipa_ch06.py` — dotenv loading
- `pull_bea_fixed_assets.py` — dotenv loading
- `pull_bls_ces.py` — dotenv loading + rewrote to compute annual averages from monthly data
- `pull_fred_ch05.py` — dotenv loading
- `TRANSFORMATION_LOG.json` — added XLOG-009
- `T_SERIES_CATALOG.json` — updated series with api_data_files, api_coverage fields

## Critical Finding: BEA API Coverage Gap

**Industry-level NIPA tables (6.2D, 6.4D, 6.5D, 6.10D) and GDP-by-Industry only go back to 1997/1998.** The pre-1998 SIC-based industry data has been retired from the current BEA API.

This means:
- **Book replication period (1948-1989)**: Industry-level data must come from other sources
- **Extension period (1997-2024)**: Full NAICS industry detail available via API
- **Aggregate NIPA tables (1.7.5, 2.1, 3.1-3.3)**: Cover 1929-2025 — fully usable for Ch 6 NSW calculations
- **Fixed Assets**: 1925-2024 — fully usable for profit rate calculations
- **BLS CES**: 1948-2024 — fully usable for Lp/L ratio calculations
- **FRED TCU**: 1967-2025 — starts when expected (capacity utilization wasn't measured earlier)

### Implications for Next Session
The Ch 6 (Net Social Wage) pipeline has **full data coverage** (NIPA 2.1, 3.1-3.3 all back to 1929). This should be the priority for Session 5 — it's the lowest-hanging fruit.

For Ch 5 industry-level calculations, the approach should be:
1. Use existing authoritative data (from book) for 1948-1989
2. Use API data for 1997-2024 extension
3. The 1990-1997 gap needs splice methodology (already documented in METHOD_CONTRACT)

## Validation Summary

| Metric | Value | Expected | Status |
|--------|-------|----------|--------|
| BLS Lp/L (1970) | 0.826 | ~0.80 | OK (aggregate private, not sectoral) |
| BLS Lp/L (2020) | 0.814 | ~0.65 declining | NOTE: aggregate vs book's productive-sector ratio |
| FRED TCU mean | 79.8% | ~80% | PASS |
| FRED TCU recession dips | 68.4-75.7% | <80% at recessions | PASS |
| GDP (1967) | $860B | hundreds of billions | PASS |
| NI (1989) | $4,760B | trillions | PASS |
| Placeholder confirmed | 546 rows, all "template" | - | Confirmed real API data differs |

**Note on BLS Lp/L**: The aggregate CES0500000006/CES0500000001 ratio stays ~0.81-0.83 across all decades. This differs from the book's declining Lp/L because the book uses a productive/unproductive sector decomposition, not the raw CES production worker numbers. The CES data will need sector-level decomposition before matching book values.

## What Comes Next (Session 5)

1. **Ch 6 NSW pipeline** — NIPA 2.1, 3.1-3.3 have full coverage; implement tax decomposition and NSW formula
2. **Baseline validation scripts** — Automate the spot-checks done manually in this session
3. **Pre-1998 industry data strategy** — Decide: (a) manual download from BEA interactive tables, (b) use book-period authoritative data, or (c) accept API-only for extension period
4. **BLS sector decomposition** — Transform raw CES ratios into the productive/unproductive decomposition the book uses

## API Keys Location

All in `Technical/scripts/ingest/.env` (gitignored):
- `BEA_API_KEY=857E9ADD-656E-43ED-9598-4EA83299418F`
- `BLS_API_KEY=44ebd49f0bc54feb83b2e452e6b123b2`
- `FRED_API_KEY=22896375f58f5dd747eaf30b32df94d3`
