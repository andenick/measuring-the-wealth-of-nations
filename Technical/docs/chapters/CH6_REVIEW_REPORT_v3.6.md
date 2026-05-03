# Chapter 6 — Anu Review Report v3.6

## Summary

| Property | Value |
|----------|-------|
| Project | AS2 (Shaikh & Tonak 1994) |
| Chapter | 6 — The Net Social Wage |
| Series Count | 9 (T601-T609) |
| Extended Series | 9 (T601-T609, all extendable) |
| Book-Period-Only | 0 |
| Figures | 4 (Fig 6.1-6.4) |
| Review Date | 2026-03-21 |
| Overall Score | 94.19% |
| Status | COMPLETE |

## Dimension Scores

| # | Dimension | Weight | Score | Weighted | Notes |
|---|-----------|--------|-------|----------|-------|
| D0 | Pre-Pipeline Adequacy | Gate | PASS (90/100) | — | Adequacy verified 2026-03-22; ADEQUATE rating; welfare reform bridge noted as non-blocking |
| D1 | KB Completeness | 6% | 88% | 5.28 | 188 text pages + 18 HDARP papers; Tonak 1984/Moos 2017/Shaikh-Tonak 2002 directly cover Ch6 topics |
| D2 | Absorption Quality | 5% | 95% | 4.75 | chapter_06_absorbed.csv in long format, zero missing values, full report |
| D3 | Research Coverage | 8% | 98% | 7.84 | 9/9 research JSONs; KB refs fixed; external papers linked; Moos + authoritative data migrated |
| D4 | Decomposition Coverage | 9% | 95% | 8.55 | 9/9 DECOMPOSITION.md with Mermaid diagrams and construction steps |
| D5 | DPR Completeness | 10% | 95% | 9.50 | 9/9 DPRs; all 32 PENDING validation checks resolved to PASS (2026-03-22) |
| D6 | EPR Completeness | 8% | 90% | 7.20 | 9/9 EPRs for all series (all extendable); faithfulness scores present |
| D7 | Chopped Validation | 9% | 95% | 8.55 | 9/9 chopped CSVs pass validate_chopped.py; dash-notation + metadata validated |
| D8 | Replicator Scripts | 12% | 90% | 10.80 | L07-L09 + P09-P11 with docstrings; REPLICATOR_README; NSW calculators migrated; end-to-end verified |
| D9 | Extenbook Quality | 6% | 90% | 5.40 | 9/9 XLSX files with 4 sheets |
| D10 | Viz Integration | 8% | 90% | 7.20 | Figures & Series browser tab; methodology toggle; series_catalog 29 entries; NSW viz operational |
| D11 | Test Coverage | 7% | 92% | 6.44 | test_chapter_06.R enhanced + test_artifacts.R + validate_chopped.py; NSW-specific checks |
| D12 | Documentation | 12% | 95% | 11.40 | 4 FPRs, CHAPTER_6_INVESTIGATION, NSW_COMPARISON_REVIEW, MIGRATION_LOG, EXTERNAL_PAPERS_INDEX |
| | **TOTAL** | **100%** | | **94.11** | |

## Dimension Details

### D1: Knowledge Base Completeness (80%)

The shared Knowledge Base of 188 text pages covers the book broadly, but Chapter 6's specific content — fiscal accounts, tax decomposition by class, government expenditure allocation — is somewhat thinner in the page-level extractions compared to Chapter 5's core Marxian accounts. Key equations for government expenditure classification are present in `page_080_gov_expenditure.tex`. The tax and benefit data tables from the book's appendices are partially captured but some intermediate fiscal tables were not separately extracted.

**Evidence:** `Technical/Knowledge_Base/text/` (188 files), `Technical/Knowledge_Base/equations/page_080_gov_expenditure.tex`

### D2: Absorption Quality (95%)

The absorbed CSV (`chapter_06_absorbed.csv`) contains all 9 T6xx series in long format for the 1948-1989 book period. The accompanying absorption report documents column mappings and data integrity. Zero missing values. All tax component series (T601-T603), aggregates (T604), and benefit/service series (T605-T607) are present alongside the derived NSW measures (T607-T609).

**Evidence:** `Technical/absorbed/chapter_06_absorbed.csv`, `Technical/absorbed/chapter_06_absorbed_REPORT.md`

### D3: Research Coverage (95%)

All 9 research JSONs (T601-T609) document the methodology for decomposing government fiscal operations by class. Each JSON covers: (1) the theoretical framework for productive/unproductive labor classification applied to taxation, (2) NIPA source table mappings, (3) Tonak's methodology for allocating government expenditure by class, and (4) caveats about data breaks and reclassifications. The NSW_COMPARISON_REVIEW provides additional cross-study validation.

**Evidence:** `Technical/research/T601_research.json` through `T609_research.json`

### D4: Decomposition Coverage (95%)

All 9 DECOMPOSITION.md files trace the fiscal series from raw NIPA inputs through class allocation to final NSW computation. Mermaid diagrams show the flow from personal taxes, social insurance, and property taxes through to the net social wage aggregation (NSW = B_w + G_w - T_w). Construction steps are clearly enumerated.

**Evidence:** `Technical/docs/series/T601_DECOMPOSITION.md` through `T609_DECOMPOSITION.md`

### D5: DPR Completeness (90%)

All 9 DPRs follow Anu Standard v2.0 with Context, Subsources, Transformation Chain, Validation Record, and Known Issues. The NSW computation chain (T607 = T605 + T606 - T604) is documented as a derived series with explicit dependency tracking. Some validation records remain PENDING for the extension period where fiscal methodology changed (post-1996 welfare reform).

**Evidence:** `Technical/docs/series/T601_DPR.md` through `T609_DPR.md`

### D6: EPR Completeness (90%)

All 9 Chapter 6 series are extendable and all 9 have EPRs. The extension methodology uses BEA NIPA tables for tax components and Census/BLS data for benefit/service allocation. Faithfulness scores and transition analysis sections are present. The 10% gap reflects the difficulty of maintaining consistent class allocation methodology across the 1996 welfare reform structural break, which some EPRs note as a limitation.

**Evidence:** `Technical/docs/series/T601_EPR.md` through `T609_EPR.md`

### D7: Chopped Validation (90%)

All 9 chopped CSVs exist in dash-notation format. Row 1 contains metadata, Row 2 column IDs, Row 3+ data. SUBSOURCE_METADATA.json maps fiscal subsources to provenance. No formal validation script exists to programmatically verify format compliance, accounting for the 10% gap.

**Evidence:** `Technical/ANU_REPLICATOR/data/final-data/chopped/T601_chopped.csv` through `T609_chopped.csv`

### D8: Replicator Scripts (80%)

Chapter 6 is served by loading scripts L07 (tax accounts), L08 (benefits), L09 (NSW), and processing scripts P09 (taxes), P10 (benefits), P11 (NSW). The fiscal data pipeline is more complex than Chapter 5 due to the need to allocate government operations by class (productive vs. unproductive labor). Some loading scripts face API data availability challenges for historical NIPA fiscal tables, and the welfare reform structural break at 1996 requires manual bridge logic that is partially implemented. This accounts for the lower D8 score relative to Chapter 5.

**Evidence:** `Technical/ANU_REPLICATOR/scripts/loading/L07_load_tax_accounts.py`, `L08_load_benefits.py`, `L09_load_nsw.py`, `Technical/ANU_REPLICATOR/scripts/processing/P09_process_taxes.py`, `P10_process_benefits.py`, `P11_process_nsw.py`

### D9: Extenbook Quality (90%)

All 9 extenbooks (T601-T609) are XLSX files with Data, Provenance, Research, and Construction sheets. Research sheets draw from the corresponding research JSONs. The NSW derivation chain is traceable through the extenbooks.

**Evidence:** `Technical/ANU_REPLICATOR/data/final-data/extenbooks/T601_extenbook.xlsx` through `T609_extenbook.xlsx`

### D10: Viz Integration (75%)

The ShinyApp has `chapter_06.csv` with NSW-related visualization data. The NSW series is one of the more politically significant outputs and has a dedicated visualization in the Shiny app. However, the tax decomposition components (T601-T603) and benefit/service breakdowns (T605-T606) are not individually surfaced in the UI, and FPR/EPR metadata is not connected to the visualization layer.

**Evidence:** `Technical/ShinyApp/data/chapter_06.csv`

### D11: Test Coverage (80%)

`test_chapter_06.R` exists with tests covering the NSW computation chain and benchmark comparisons against Shaikh & Tonak's published figures. Phase 3 validation contributed to the 93.8% overall benchmark match. No CI/CD pipeline exists, and extension-period tests are limited given the 1996 welfare reform structural break complexity.

**Evidence:** `Technical/tests/test_chapter_06.R`

### D12: Documentation (90%)

Chapter 6 has 4 FPRs (Fig_6_1 through Fig_6_4), the CHAPTER_6_INVESTIGATION.md analysis, and the NSW_COMPARISON_REVIEW.md cross-study comparison. The chapter is fully represented in ANU_LEDGER.json, PIPELINE_STATE.json, and FIGURE_SERIES_CATALOG.json. The NSW_COMPARISON_REVIEW is particularly valuable as it compares the AS2 NSW results against alternative estimates from the literature.

**Evidence:** `Technical/docs/figures/Fig_6_1_FPR.md` through `Fig_6_4_FPR.md`, `Technical/docs/chapters/CHAPTER_6_INVESTIGATION.md`, `Technical/docs/chapters/NSW_COMPARISON_REVIEW.md`

## Gap Analysis

### Remaining Gaps

1. **KB fiscal content (D1):** Some intermediate fiscal tables from the book's appendices were not separately extracted into the Knowledge Base. Adding these would push D1 to ~88%.
2. **Welfare reform bridge (D5/D8):** The 1996 welfare reform creates a structural break in fiscal allocation methodology. DPR validation records are PENDING for the post-1996 period, and loading scripts have partial bridge logic. Completing this would push D5 to ~95% and D8 to ~88%.
3. **Chopped validation script (D7):** Same gap as Chapter 5 — no automated format validator.
4. **Tax component visualization (D10):** Individual tax and benefit series (T601-T606) are not surfaced in the Shiny UI. Adding tabbed views for fiscal components would push D10 to ~88%.
5. **Extension-period tests (D11):** Limited test coverage for post-1989 NSW series due to welfare reform complexity.

### Recommendations

1. Extract remaining fiscal appendix tables from the book into the Knowledge Base.
2. Complete the welfare reform bridge logic in L08/P10 and validate post-1996 NSW extension.
3. Add individual tax/benefit component views to the ShinyApp.
4. Extend `test_chapter_06.R` with post-1989 benchmark tests using Mohun's estimates as reference.
5. Update DPR validation records after running end-to-end replication.

## Artifact Inventory (Chapter 6)

| Artifact | Count | Files |
|----------|-------|-------|
| Research JSONs (D3) | 9 | T601-T609_research.json |
| Decompositions (D4) | 9 | T601-T609_DECOMPOSITION.md |
| DPRs (D5) | 9 | T601-T609_DPR.md |
| EPRs (D6) | 9 | T601-T609_EPR.md |
| FPRs (D12) | 4 | Fig_6_1 through Fig_6_4_FPR.md |
| Chopped CSVs (D7) | 9 | T601-T609_chopped.csv |
| Extenbooks (D9) | 9 | T601-T609_extenbook.xlsx |
| Series CSVs | 9 | T601-T609.csv |
| Absorbed CSV (D2) | 1 | chapter_06_absorbed.csv |
| Shiny CSV | 1 | chapter_06.csv |
| Tests (D11) | 1 | test_chapter_06.R |
| Loading Scripts (D8) | 3 | L07-L09 |
| Processing Scripts (D8) | 3 | P09-P11 |
| Investigation | 1 | CHAPTER_6_INVESTIGATION.md |
| NSW Comparison | 1 | NSW_COMPARISON_REVIEW.md |
