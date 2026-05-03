# Anu Review Checklist: Chapter 5

**Generated:** 2026-02-24
**Tool:** Anu Review v1.0
**Session:** AS2 Session 6

---

## Overview

| Metric | Value |
|--------|-------|
| Chapter | 5 |
| Title | An Accounting Framework for Empirical Estimates |
| Series | T501 - T516 |
| Total Series | 16 |
| Extended Series | 9 (T504, T505, T506, T511, T512, T513, T514, T515, T516) |
| Book-Period-Only Series | 7 (T501, T502, T503, T507, T508, T509, T510) |
| Figures | 8 (Fig 5.1 - 5.8) |

---

## 1. DPR Completeness (25%)

### Required Files

- [ ] All 16 series have DPR files in `docs/series/` -- **4/16 exist**

### Required Sections (per DPR)

- [x] Quick Reference table with series metadata
- [x] Shaikh context with actual book quotes
- [x] Subsource documentation (T5xxA, T5xxB, etc.)
- [x] Transformation chain (XFORM identifiers)
- [x] Validation record with date and status
- [x] HDARP linkage (Knowledge_Base/ references)

### Series DPR Status

| Series | Name | DPR Exists | Complete | Notes |
|--------|------|------------|----------|-------|
| T501 | Total Product (TP*) | [ ] | [ ] | Missing |
| T502 | Constant Capital (C*_m) | [ ] | [ ] | Missing |
| T503 | Value Added (VA*) | [ ] | [ ] | Missing |
| T504 | Variable Capital (V*) | [x] | [x] | Quick Ref, Context, Subsources, Transforms, Validation, Known Issues |
| T505 | Surplus Value (S*) | [ ] | [ ] | Missing |
| T506 | Rate of Exploitation (e=S*/V*) | [x] | [x] | Quick Ref, Context (p.115 quote), Subsources (3), 7-step Transform, 8 Validation checks, Appendix refs |
| T507 | Surplus Ratio (S*/Y) | [ ] | [ ] | Missing |
| T508 | Productive Consumption (CON*) | [ ] | [ ] | Missing |
| T509 | Productive Investment (IG*) | [ ] | [ ] | Missing |
| T510 | Value Composition (C*/V*) | [ ] | [ ] | Missing |
| T511 | Productive Labor Share (Lp/L) | [x] | [x] | Quick Ref, Context (p.130 quote), Subsources (2), 4-step Transform, 7 Validation, Extension Doc |
| T512 | Productive Wage Share (V*/W) | [x] | [x] | Quick Ref, Context, Subsources (2), 3-step Transform, 6 Validation, Extension Doc, DIV-002 ref |
| T513 | Marxian Profit Rate (r*) | [ ] | [ ] | Missing |
| T514 | Capacity-Adjusted Profit Rate | [ ] | [ ] | Missing |
| T515 | Productive Employment (Lp) | [ ] | [ ] | Missing |
| T516 | Unproductive Employment (Lu) | [ ] | [ ] | Missing |

**Score Calculation**: 4 DPRs exist, all 4 are complete (all 6 weighted components present).
- Existing DPR quality: 100% (all have Quick Ref, Context, Subsources, Transforms, Validation, HDARP/KB linkage)
- Coverage: 4/16 = 25%
- **Dimension Score: 25%**

---

## 2. EPR Completeness (22%)

### Required Files

- [ ] All 9 extendable series have EPR files -- **2/9 exist**

### Required Sections (per EPR)

- [x] Agent understanding statement
- [x] Book context with Shaikh quotes
- [x] Original methodology documentation
- [x] Current methodology documentation
- [x] Methodology changes assessment
- [x] Transition analysis with metrics
- [x] Faithfulness score (percentage)
- [x] Certification status

### Series EPR Status

| Series | Name | Extended? | EPR Exists | Faith. Score | Certification |
|--------|------|-----------|------------|--------------|---------------|
| T504 | Variable Capital (V*) | Yes | [ ] | -- | -- |
| T505 | Surplus Value (S*) | Yes | [ ] | -- | -- |
| T506 | Rate of Exploitation | Yes | [ ] | -- | -- |
| T511 | Productive Labor Share | Yes | [x] | 78% | CERTIFIED WITH NOTES |
| T512 | Productive Wage Share | Yes | [x] | 76% | CERTIFIED WITH NOTES |
| T513 | Marxian Profit Rate | Yes | [ ] | -- | -- |
| T514 | Capacity-Adjusted Rate | Yes | [ ] | -- | -- |
| T515 | Productive Employment | Yes | [ ] | -- | -- |
| T516 | Unproductive Employment | Yes | [ ] | -- | -- |

**Non-extended series (N/A for EPR)**:
T501, T502, T503, T507, T508, T509, T510 -- book-period-only, depend on IO benchmark tables (Wave 2)

**Score Calculation**: 2 EPRs exist out of 9 extendable series, both complete (all 13 sections populated).
- Existing EPR quality: 100% (Agent Understanding, Book Context, Original/Current Methodology, Changes Assessment, Transition Analysis, Faithfulness Score, Certification)
- Coverage: 2/9 = 22.2%
- **Dimension Score: 22%**

---

## 3. Data File Integrity (65%)

### Required Files

| File | Exists | Rows | Columns | Period | Notes |
|------|--------|------|---------|--------|-------|
| Table5_7_KeyRatios.csv | [x] | 42 | 6 | 1948-1989 | T506A, T511A, T512A + working copies |
| Table5_7_Extended.csv | [x] | 77 | 9 | 1948-2024 | A/EXT/COMBINED for T506, T511, T512 |
| TableE2_RevenueAccounts.csv | [x] | 14 | 26 | 1948-1961 | Revenue accounts (partial period) |
| TableE3_LaborStatistics.csv | [x] | 17 | -- | 1948-1961 | Employment decomposition (partial period) |
| Table5_14_Comparison.csv | [x] | 10 | -- | -- | Marxian vs orthodox ratios |
| Employment_1948_1989.csv | [x] | 42 | -- | 1948-1989 | T515, T516 |
| ExploitationComposition_1948_1989.csv | [x] | 42 | -- | 1948-1989 | Exploitation + composition ratios |

### Data Quality Checks

- [x] File existence: 7/7 expected Chopped CSVs present
- [x] Extended CSV exists: Table5_7_Extended.csv (1948-2024) with A/EXT/COMBINED columns
- [ ] Column coverage for all 16 series: T504, T505 not in explicit columns (derived); T513, T514 only in ShinyApp/data/ (not in Chopped format)
- [x] Year range match: Book period files cover 1948-1989; TableE2/E3 cover 1948-1961 only (partial)
- [x] Header format: Anu Chopped 3-row header (metadata, subseries IDs, data)
- [x] Spot-check validated: e(1948)=1.70, e(1989)=2.44 confirmed

### Coverage Analysis

| Series | In Chopped File | Column Coverage |
|--------|-----------------|-----------------|
| T501 (TP*) | TableE2 | Partial (1948-1961 only) |
| T502 (C*_m) | TableE2 | Partial (1948-1961 only) |
| T503 (VA*) | TableE2 | Partial (1948-1961 only) |
| T504 (V*) | ExploitationComposition | Indirect (via ratio) |
| T505 (S*) | ExploitationComposition | Indirect (via ratio) |
| T506 (e=S*/V*) | Table5_7_KeyRatios, Table5_7_Extended | Full coverage |
| T507 (GFP*) | TableE2 | Partial (1948-1961 only) |
| T508 (CON*) | TableE2 | Partial (1948-1961 only) |
| T509 (IG*) | TableE2 | Partial (1948-1961 only) |
| T510 (C*/V*) | ExploitationComposition | 1948-1989 |
| T511 (Lp/L) | Table5_7_KeyRatios, Table5_7_Extended | Full coverage |
| T512 (V*/W) | Table5_7_KeyRatios, Table5_7_Extended | Full coverage |
| T513 (r*) | -- | NOT in Chopped (only in ShinyApp/data/) |
| T514 (r*_adj) | -- | NOT in Chopped (only in ShinyApp/data/) |
| T515 (Lp) | Employment_1948_1989 | 1948-1989 |
| T516 (Lu) | Employment_1948_1989 | 1948-1989 |

**Known Gaps**:
- TableE2/TableE3 only cover 1948-1961 (HDARP extraction partial period)
- T513, T514 profit rate data not in Anu Chopped format
- T504, T505 present only as ratios, not absolute values in Chopped CSVs

**Score Calculation**:
- File existence: 7/7 = 100% (+30 points)
- Extended CSV: exists with correct structure (+15 points)
- Column coverage: 13/16 series have some representation (+10 points)
- Year range completeness: partial (TableE2/E3 only 1948-1961) (+5 points)
- Missing profit rate Chopped CSVs: -10 points
- Partial-period files: -5 points
- Anu Chopped format compliance: correct 3-row headers (+10 points)
- **Dimension Score: 65%**

---

## 4. Series Mapping (0%)

### Required Code

- [ ] `CH5_SERIES_MAPPING` defined in `data_loader.R` -- **file does not exist**
- [ ] `get_series_data()` checks this mapping -- **N/A**

### Per-Series Requirements

- [ ] `data_patterns` defined for each series -- **N/A**
- [ ] `subsources` listed for each series -- **N/A**
- [ ] `description` present for each series -- **N/A**
- [ ] `shaikh_finding` documented for each series -- **N/A**
- [ ] Special flags set correctly -- **N/A**

### Current State

The ShinyApp uses `server_logic.R` with inline data loading (reactive filters on pre-loaded data frames). There is no modular `data_loader.R` with `CH5_SERIES_MAPPING`. The T_SERIES_CATALOG.json provides metadata for all 16 series, but this is not integrated into the Shiny app code.

**Dimension Score: 0%**

---

## 5. Chart Builder Integration (0%)

### Required Code

- [ ] Helper function `is_chapter5_series()` exists -- **No**
- [ ] Specialized chart builders exist -- **No chart_builder.R**
- [ ] Error handling for missing data -- **N/A**
- [ ] Plotly configuration complete -- **N/A**

### Builder Coverage

| Series Type | Builder | Exists |
|-------------|---------|--------|
| Exploitation rate | `build_exploitation_chart()` | [ ] |
| Employment decomposition | `build_employment_chart()` | [ ] |
| Profit rate | `build_profit_rate_chart()` | [ ] |
| Revenue-side | `build_revenue_chart()` | [ ] |

### Current State

The ShinyApp has plot generation in `server_logic.R` but no modular `chart_builder.R`. Plotly charts exist inline in the server logic but are not organized as chapter-specific builders.

**Dimension Score: 0%**

---

## 6. Test Coverage (0%)

### Required Files

- [ ] `tests/test_chapter_05.R` exists -- **directory exists but is empty**

### Required Test Sections

- [ ] CHAPTER_METADATA tests -- **N/A**
- [ ] CH5_SERIES_MAPPING tests -- **N/A**
- [ ] Data file existence tests -- **N/A**
- [ ] DPR file existence tests -- **N/A**
- [ ] EPR file existence tests -- **N/A**
- [ ] FIGURE_SERIES_CATALOG tests -- **N/A**
- [ ] Helper function tests -- **N/A**
- [ ] Thematic tests (e.g., e(1948)=1.70) -- **N/A**

**Dimension Score: 0%**

---

## 7. Catalog Consistency (0%)

### Required Entries

- [ ] All 8 chapter figures in `FIGURE_SERIES_CATALOG.json` -- **file does not exist**

### Expected Figure Entries

| Figure | Type | Series IDs | In Catalog |
|--------|------|------------|------------|
| Fig 5.1 | conceptual | None | [ ] |
| Fig 5.2 | time_series | T511, T515, T516 | [ ] |
| Fig 5.3 | time_series | T506 | [ ] |
| Fig 5.4 | time_series | T501-T505 | [ ] |
| Fig 5.5 | time_series | T513, T514 | [ ] |
| Fig 5.6 | time_series | T501, T515 | [ ] |
| Fig 5.7 | time_series | T511, T515, T516 | [ ] |
| Fig 5.8 | cross_sectional | All T5xx | [ ] |

**Dimension Score: 0%**

---

## 8. Knowledge Base Integration (40%)

### Documentation Requirements

- [x] Web research documented for key series -- T511 EPR has 4 search queries + 4 key findings; T512 EPR has 2 queries + 3 findings
- [x] Source quotes extracted and cited -- All 4 DPRs and 2 EPRs contain blockquotes with page references (pp. 60, 113, 115, 130, 140, 240, 340)
- [x] Data source URLs documented -- BLS API v2 endpoint, BEA API endpoint, FRED API documented in EPRs
- [x] Methodology changes researched -- SIC-NAICS transition (2003), CES redesign (2011), COVID-19 impact (2020), NIPA 6.2D availability
- [x] API endpoints documented -- BLS CES series IDs (CES0500000006, CES0500000001), BEA NIPA tables
- [ ] Complete coverage across all 16 series -- only 4/16 DPRs and 2/9 EPRs have KB integration

### Per-Series KB Status

| Series | Has DPR KB | Has EPR KB | Web Research | Source Quotes | API Docs |
|--------|-----------|-----------|--------------|---------------|----------|
| T504 | [x] | -- | Partial | [x] p.115 | [x] BEA/BLS |
| T506 | [x] | -- | Partial | [x] pp.113,115 | [x] BEA/BLS |
| T511 | [x] | [x] | [x] 4 queries | [x] pp.60,130,140,240,340 | [x] BLS API v2 |
| T512 | [x] | [x] | [x] 2 queries | [x] pp.113,130,140,340 | [x] BEA/BLS |
| T501-T503, T505, T507-T510, T513-T516 | [ ] | [ ] | [ ] | [ ] | [ ] |

**Score Calculation**: 4/16 series have DPR KB integration (100% quality each), 2/9 have EPR KB (100% quality). Average across all series: ~40%.

**Dimension Score: 40%**

---

## Summary

| Dimension | Weight | Score | Weighted | Status |
|-----------|--------|-------|----------|--------|
| DPR Completeness | 15% | 25% | 3.75% | FAIL |
| EPR Completeness | 15% | 22% | 3.30% | FAIL |
| Data File Integrity | 15% | 65% | 9.75% | FAIL |
| Series Mapping | 15% | 0% | 0.00% | FAIL |
| Chart Builder Integration | 10% | 0% | 0.00% | FAIL |
| Test Coverage | 10% | 0% | 0.00% | FAIL |
| Catalog Consistency | 10% | 0% | 0.00% | FAIL |
| Knowledge Base Integration | 10% | 40% | 4.00% | FAIL |

**Integration Score: 20.80%**

**Overall Status: INCOMPLETE**

---

## Next Steps

1. [ ] Create 12 missing DPRs (T501-T503, T505, T507-T510, T513-T516)
2. [ ] Create 7 missing EPRs (T504, T505, T506, T513, T514, T515, T516)
3. [ ] Create `data_loader.R` with `CH5_SERIES_MAPPING`
4. [ ] Create `chart_builder.R` with chapter-specific builders
5. [ ] Create `test_chapter_05.R` with all 8 test sections
6. [ ] Create `FIGURE_SERIES_CATALOG.json` with all 8 figures
7. [ ] Add T513/T514 to Anu Chopped format
8. [ ] Re-run `/anu-review 5` to recalculate scores
9. [ ] Achieve COMPLETE or EXEMPLARY status

---

*Generated by Anu Review v1.0 | Part of the Anu Suite*
