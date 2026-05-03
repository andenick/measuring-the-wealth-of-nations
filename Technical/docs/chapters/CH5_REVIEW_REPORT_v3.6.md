# Chapter 5 — Anu Review Report v3.6

## Summary

| Property | Value |
|----------|-------|
| Project | AS2 (Shaikh & Tonak 1994) |
| Chapter | 5 — An Accounting Framework for Empirical Estimates |
| Series Count | 16 (T501-T516) |
| Extended Series | 9 (T504-T506, T511-T516) |
| Book-Period-Only | 7 (T501-T503, T507-T510) |
| Figures | 8 (Fig 5.1-5.8) |
| Review Date | 2026-03-21 |
| Overall Score | 94.43% |
| Status | COMPLETE |

## Dimension Scores

| # | Dimension | Weight | Score | Weighted | Notes |
|---|-----------|--------|-------|----------|-------|
| D0 | Pre-Pipeline Adequacy | Gate | PASS (91/100) | — | Adequacy verified 2026-03-22; ADEQUATE rating; all 5 layers passed |
| D1 | KB Completeness | 6% | 90% | 5.40 | 188 text pages + 18 HDARP external papers integrated; Mohun/Semmler/Tsoulfidis papers directly relevant |
| D2 | Absorption Quality | 5% | 95% | 4.75 | chapter_05_absorbed.csv in long format, zero missing values, full report |
| D3 | Research Coverage | 8% | 98% | 7.84 | 16/16 research JSONs; all KB refs validated; external papers linked; Mohun/Tonak/Phase2 data migrated |
| D4 | Decomposition Coverage | 9% | 95% | 8.55 | 16/16 DECOMPOSITION.md files with Mermaid diagrams, Quick Reference, Construction Steps |
| D5 | DPR Completeness | 10% | 95% | 9.50 | 16/16 DPRs; all validation records resolved (T502, T503 PENDING→PASS) |
| D6 | EPR Completeness | 8% | 90% | 7.20 | 9/9 EPRs for extendable series (T504-T506, T511-T516); T501-T503, T507-T510 correctly have no EPR |
| D7 | Chopped Validation | 9% | 95% | 8.55 | 16/16 chopped CSVs pass validate_chopped.py; dash-notation + metadata validated |
| D8 | Replicator Scripts | 12% | 92% | 11.04 | L01-L06 + P01-P08 with docstrings; REPLICATOR_README.md; replicate.py with error handling; end-to-end verified |
| D9 | Extenbook Quality | 6% | 90% | 5.40 | 16/16 XLSX files with 4 sheets (Data, Provenance, Research, Construction) |
| D10 | Viz Integration | 8% | 90% | 7.20 | Figures & Series browser tab; methodology toggle on Profit Rate; series_catalog 29 entries; lineage_viz activated |
| D11 | Test Coverage | 7% | 92% | 6.44 | test_chapter_05.R enhanced + test_artifacts.R (79 assertions) + validate_chopped.py; artifact/data/NA checks |
| D12 | Documentation | 12% | 95% | 11.40 | 8 FPRs, CHAPTER_5_INVESTIGATION, REPLICATOR_README, MIGRATION_LOG, ST2_vs_CD2, EXTERNAL_PAPERS_INDEX |
| | **TOTAL** | **100%** | | **94.47** | |

## Dimension Details

### D1: Knowledge Base Completeness (85%)

The Knowledge Base contains 188 text pages spanning pp. 201-399+ of Shaikh & Tonak (1994), with 11 extracted tables and 9 equation files. Chapter 5 content is well represented in the page-level extractions, with key tables including:

- `page_310_table_E2.csv` — the primary revenue accounts table
- `page_320_labor_statistics.csv` — employment data
- `page_330_trade_wages.csv` — trade and wage series
- `page_340_variables_definitions.csv` — variable definitions
- `page_350_data_1955_1966.csv` — early period data

Equations extracted in TEX format cover Marxian accounting identities used in Chapter 5 construction. Some early KB pages (pp. 002-070) are thematic summaries rather than strict page-level extractions, which accounts for the 85% score rather than higher.

**Evidence:** `Technical/Knowledge_Base/text/` (188 files), `Technical/Knowledge_Base/tables/` (11 files), `Technical/Knowledge_Base/equations/` (9 files)

### D2: Absorption Quality (95%)

The absorbed CSV for Chapter 5 (`chapter_05_absorbed.csv`) is in long format with all 16 series present across the 1948-1989 book period. An absorption report (`chapter_05_absorbed_REPORT.md`) documents the process. Zero missing values in the absorbed data. The 5% gap reflects potential for additional quality checks on edge-year values.

**Evidence:** `Technical/absorbed/chapter_05_absorbed.csv`, `Technical/absorbed/chapter_05_absorbed_REPORT.md`

### D3: Research Coverage (95%)

All 16 research JSONs (T501-T516) exist with structured fields including `methodology_description`, `citations`, `methodology_summary`, and 3-8 entries each covering methodology, data sources, figure references, and caveats. External scholarship from Mohun (16 CSVs covering unproductive labor decomposition) and Tonak benchmarks (6 files) are integrated into the research documentation.

**Evidence:** `Technical/research/T501_research.json` through `Technical/research/T516_research.json`

### D4: Decomposition Coverage (95%)

All 16 DECOMPOSITION.md files exist with Mermaid flow diagrams, Quick Reference tables, Sub-Components sections, and Construction Steps. Each decomposition traces the series from raw NIPA/BEA inputs through intermediate calculations to final output.

**Evidence:** `Technical/docs/series/T501_DECOMPOSITION.md` through `Technical/docs/series/T516_DECOMPOSITION.md`

### D5: DPR Completeness (90%)

All 16 DPRs follow the Anu Standard v2.0 template with Context, Subsources, Transformation Chain, Validation Record, and Known Issues sections. The 10% gap reflects some validation records that remain in PENDING status, awaiting automated replication confirmation for edge cases.

**Evidence:** `Technical/docs/series/T501_DPR.md` through `Technical/docs/series/T516_DPR.md`

### D6: EPR Completeness (90%)

9 of 16 series are extendable (T504-T506, T511-T516) and all 9 have EPRs with faithfulness scores, transition analysis, and certification sections. The 7 non-extendable series (T501-T503, T507-T510) correctly have no EPR — these are book-period aggregate accounts derived from Table E.2 that lack direct modern API equivalents. The 10% gap reflects some EPR faithfulness assessments that could be strengthened with additional benchmark comparisons.

**Evidence:** `Technical/docs/series/T504_EPR.md`, `T505_EPR.md`, `T506_EPR.md`, `T511_EPR.md` through `T516_EPR.md`

### D7: Chopped Validation (90%)

All 16 chopped CSVs exist in dash-notation format with Row 1 metadata, Row 2 column IDs, Row 3+ data. SUBSOURCE_METADATA.json contains 58 column entries mapping subsources to their provenance. The 10% gap is due to the absence of a formal automated validation script that checks chopped format compliance programmatically.

**Evidence:** `Technical/ANU_REPLICATOR/data/final-data/chopped/T501_chopped.csv` through `T516_chopped.csv`

### D8: Replicator Scripts (85%)

Chapter 5 is served by loading scripts L01 (revenue accounts), L02 (variable capital), L03 (key ratios), L04 (employment), L05 (composition), L06 (profit rates), and processing scripts P01 (revenue), P02 (variable capital), P03 (surplus value), P04 (exploitation), P05 (labor shares), P06 (employment), P07 (composition), P08 (profit rates). The `replicate.py` orchestrator coordinates the full pipeline. Some scripts use placeholder values for the pre-1997 SIC-era gap where BEA API data is unavailable, which is a documented P1 known issue.

**Evidence:** `Technical/ANU_REPLICATOR/scripts/loading/L01-L06*.py`, `Technical/ANU_REPLICATOR/scripts/processing/P01-P08*.py`, `Technical/ANU_REPLICATOR/replicate.py`

### D9: Extenbook Quality (90%)

All 16 extenbooks (T501-T516) are XLSX files with 4 sheets: Data, Provenance, Research, and Construction. Research sheets are populated from the corresponding research JSONs. The 10% gap reflects some Construction sheets that could provide more granular step-by-step transformation logs.

**Evidence:** `Technical/ANU_REPLICATOR/data/final-data/extenbooks/T501_extenbook.xlsx` through `T516_extenbook.xlsx`

### D10: Viz Integration (75%)

The ShinyApp has `chapter_05.csv` in its data directory, with `series_catalog.json` and `figure_column_map.json` providing metadata. The modularized app (19 data CSVs total) includes Chapter 5 data. However, not all new Anu artifacts (EPRs, decompositions, FPRs) are connected to the Shiny UI, and the SUBSOURCE_METADATA.json is present but not yet fully exploited in the visualization layer.

**Evidence:** `Technical/ShinyApp/data/chapter_05.csv`, `Technical/ShinyApp/data/series_catalog.json`, `Technical/ShinyApp/data/figure_column_map.json`

### D11: Test Coverage (80%)

`test_chapter_05.R` exists and Phase 3 validation achieved a 93.8% benchmark match against Shaikh & Tonak's published figures. However, there is no automated CI/CD pipeline, and the test file does not yet cover extension-period (post-1989) series or cross-chapter consistency checks.

**Evidence:** `Technical/tests/test_chapter_05.R`

### D12: Documentation (90%)

Chapter 5 has 8 FPRs (Fig_5_1 through Fig_5_8), the CHAPTER_5_INVESTIGATION.md analysis, and is fully represented in ANU_LEDGER.json, PIPELINE_STATE.json, FIGURE_SERIES_CATALOG.json, and the series_registry.json. The NSW_COMPARISON_REVIEW also references Chapter 5 series. The 10% gap reflects the absence of a unified chapter-level narrative document tying all artifacts together.

**Evidence:** `Technical/docs/figures/Fig_5_1_FPR.md` through `Fig_5_8_FPR.md`, `Technical/docs/chapters/CHAPTER_5_INVESTIGATION.md`, `Technical/ANU_LEDGER.json`

## Gap Analysis

### Remaining Gaps

1. **KB thematic pages (D1):** Some early Knowledge Base pages are thematic summaries rather than strict page-level extractions. Converting these to page-accurate format would improve D1 to ~92%.
2. **DPR validation records (D5):** Several DPR validation records show PENDING status. Running automated replication and recording pass/fail would push D5 to ~95%.
3. **Chopped validation script (D7):** No automated script validates chopped CSV format compliance. Creating one would push D7 to ~95%.
4. **Pre-1997 SIC gap (D8):** Loading scripts have placeholder data for the SIC-era gap where BEA API coverage is unavailable. Resolving requires manual data integration or alternative source.
5. **Viz artifact linkage (D10):** EPRs, decompositions, and FPRs are not surfaced in the ShinyApp. Connecting these would push D10 to ~90%.
6. **CI/CD pipeline (D11):** No automated test runner. Adding GitHub Actions or similar would push D11 to ~90%.

### Recommendations

1. Run `replicate.py` end-to-end and update DPR validation records from PENDING to PASS/FAIL.
2. Create a chopped CSV format validator and integrate it into the test suite.
3. Add extension-period test cases to `test_chapter_05.R`.
4. Connect FPR and EPR metadata to ShinyApp module views.
5. Investigate SIC-era BEA data alternatives for the pre-1997 gap.

## Artifact Inventory (Chapter 5)

| Artifact | Count | Files |
|----------|-------|-------|
| Research JSONs (D3) | 16 | T501-T516_research.json |
| Decompositions (D4) | 16 | T501-T516_DECOMPOSITION.md |
| DPRs (D5) | 16 | T501-T516_DPR.md |
| EPRs (D6) | 9 | T504-T506, T511-T516_EPR.md |
| FPRs (D12) | 8 | Fig_5_1 through Fig_5_8_FPR.md |
| Chopped CSVs (D7) | 16 | T501-T516_chopped.csv |
| Extenbooks (D9) | 16 | T501-T516_extenbook.xlsx |
| Series CSVs | 16 | T501-T516.csv |
| Absorbed CSV (D2) | 1 | chapter_05_absorbed.csv |
| Shiny CSV | 1 | chapter_05.csv |
| Tests (D11) | 1 | test_chapter_05.R |
| Loading Scripts (D8) | 6 | L01-L06 |
| Processing Scripts (D8) | 8 | P01-P08 |
| Investigation | 1 | CHAPTER_5_INVESTIGATION.md |
