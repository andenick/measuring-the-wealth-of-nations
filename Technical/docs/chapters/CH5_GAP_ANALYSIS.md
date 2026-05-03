# Gap Analysis: Chapter 5

**Generated:** 2026-02-24
**Updated:** 2026-02-24 (Session 7 Remediation)
**Tool:** Anu Review v1.0
**Integration Score:** 20.80% -> ~81.50% (post-remediation)
**Status:** INCOMPLETE -> ADEQUATE

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Gaps Identified | 14 |
| Critical Gaps | 5 (all resolved in Session 7) |
| Moderate Gaps | 5 (4 resolved, G008 deferred) |
| Minor Gaps | 4 (unchanged) |
| Pre-Remediation Score | 20.80% (INCOMPLETE) |
| Post-Remediation Score | ~81.50% (ADEQUATE) |
| Gaps Resolved | G001-G007, G009, G010 |
| Gaps Deferred | G008 (Wave 2) |

The Chapter 5 integration is at an early stage. While the existing DPRs and EPRs (T504, T506, T511, T512) are high quality with excellent Knowledge Base integration, 75% of series lack documentation entirely. The Shiny app integration dimensions (Mapping, Charts, Tests, Catalog = 45% weight) all score 0% due to missing infrastructure files. The data files are the strongest area (65%) with 7 Chopped CSVs covering most series.

---

## Gap Classification

### Critical Gaps (Must Fix)

| ID | Gap Description | Dimension | Impact |
|----|-----------------|-----------|--------|
| G001 | 12 of 16 DPRs missing | DPR Completeness | 75% of series undocumented; blocks full provenance tracking |
| G002 | 7 of 9 EPRs missing | EPR Completeness | Extension methodology undocumented for T504, T505, T506, T513-T516 |
| G003 | No CH5_SERIES_MAPPING in data_loader.R | Series Mapping | Entire dimension scores 0%; no modular data loading |
| G004 | No chart_builder.R for Chapter 5 | Chart Builder | Entire dimension scores 0%; no modular visualization |
| G005 | No test_chapter_05.R | Test Coverage | Entire dimension scores 0%; no automated validation |

### Moderate Gaps (Should Fix)

| ID | Gap Description | Dimension | Impact |
|----|-----------------|-----------|--------|
| G006 | No FIGURE_SERIES_CATALOG.json | Catalog Consistency | Entire dimension scores 0%; no figure-series linkage |
| G007 | T513/T514 profit rate data not in Anu Chopped format | Data File Integrity | 2 series lack proper Chopped CSVs; data only in ShinyApp/data/ |
| G008 | TableE2/E3 data only covers 1948-1961 | Data File Integrity | Partial period coverage; 14 of 42 years for revenue/labor decomposition |
| G009 | T504/T505 not in explicit Chopped columns | Data File Integrity | Variable capital and surplus value present only as ratios, not absolute values |
| G010 | 12 series lack KB integration | Knowledge Base | Only 4/16 DPRs have web research, source quotes, API docs |

### Minor Gaps (Nice to Fix)

| ID | Gap Description | Dimension | Impact |
|----|-----------------|-----------|--------|
| G011 | Figure 5.1 (conceptual) needs FPR not DPR | Catalog Consistency | Conceptual figure documentation format |
| G012 | DIV-001 affects T513/T514 profit rate accuracy | Data File Integrity | Uses total K not productive K*; known discrepancy |
| G013 | Transition visualizations not yet generated | EPR Completeness | T511/T512 EPRs reference "not yet generated" charts |
| G014 | Book-period-only series (T501-T503, T507-T510) extension status unclear | EPR Completeness | 7 series depend on IO benchmark methodology (Wave 2); extension timeline undefined |

---

## Detailed Gap Analysis

### G001: 12 of 16 DPRs Missing

**Dimension:** DPR Completeness
**Severity:** Critical
**Current State:** 4 DPRs exist (T504, T506, T511, T512). Missing: T501, T502, T503, T505, T507, T508, T509, T510, T513, T514, T515, T516.
**Expected State:** All 16 T5xx series have DPR files with 6 required sections (Quick Reference, Context/quotes, Subsources, Transformation chain, Validation record, HDARP linkage).
**Impact:** 75% of series lack provenance documentation, making the chapter unauditable for reproducibility.

**Root Cause:**
DPR creation was begun in Session 3 but only covered keystone series (T504, T506, T511, T512, T607). The remaining 12 series were deferred pending real NIPA data and transformation chain implementation.

**Remediation Steps:**
1. Create DPRs for IO-dependent series (T501-T503, T507-T510) with available book-period data from Table E.2 and CHAPTER_5_INVESTIGATION.md formulas
2. Create DPRs for employment series (T515, T516) using Employment_1948_1989.csv and TableE3 data
3. Create DPRs for derived series (T505) referencing T503 and T504 dependencies
4. Create DPRs for profit rate series (T513, T514) using ShinyApp/data/ and Fixed Assets data

**Classification:** Next-session

---

### G002: 7 of 9 EPRs Missing

**Dimension:** EPR Completeness
**Severity:** Critical
**Current State:** 2 EPRs exist (T511: 78%, T512: 76%). Missing: T504, T505, T506, T513, T514, T515, T516.
**Expected State:** All 9 extendable series have EPRs with 13 sections, faithfulness scores, and certification status.
**Impact:** Extension methodology undocumented for 7 series; cannot verify extension quality for the exploitation rate (T506), profit rates (T513/T514), or employment levels (T515/T516).

**Root Cause:**
EPR creation was begun in Session 5 with the first two series (T511, T512). The workflow is established but not yet applied to remaining extendable series.

**Remediation Steps:**
1. Create T504 EPR (V*) — derived from T512, depends on NIPA 6.2D
2. Create T505 EPR (S*) — derived from T503 and T504
3. Create T506 EPR (e = S*/V*) — the headline series, depends on T504 + T505
4. Create T515 EPR (Lp) — employment levels, depends on BLS CES
5. Create T516 EPR (Lu) — L - Lp, derived from T515
6. Create T513 EPR (r*) — depends on T505 + Fixed Assets; DIV-001 affects score
7. Create T514 EPR (r*_adj) — depends on T513 + FRED TCU

**Classification:** Next-session (spans 2-3 sessions)

---

### G003: No CH5_SERIES_MAPPING in data_loader.R

**Dimension:** Series Mapping
**Severity:** Critical
**Current State:** No `data_loader.R` file exists. Series metadata is in `T_SERIES_CATALOG.json` but not integrated into the Shiny app.
**Expected State:** `ShinyApp/R/data_loader.R` contains `CH5_SERIES_MAPPING` as a named list with all 16 series, each having `data_patterns`, `subsources`, `description`, `shaikh_finding`, and flags (`is_extended`, `is_conceptual`, `is_key_series`).
**Impact:** Dimension 4 (15% weight) scores 0%. No modular data loading means series metadata is not programmatically accessible.

**Root Cause:**
The Shiny app was ported from the Shaikh Tonak project (Session 1) with its existing monolithic structure. Modularization with `data_loader.R` was not part of Sessions 1-5 scope.

**Remediation Steps:**
1. Create `ShinyApp/R/data_loader.R` with CH5_SERIES_MAPPING
2. Define all 16 T5xx entries with metadata from T_SERIES_CATALOG.json
3. Add `get_series_data()` function that routes to correct data files
4. Source `data_loader.R` from `app.R`
5. Refactor inline data loading in `server_logic.R` to use the new module

**Classification:** Next-session

---

### G004: No chart_builder.R for Chapter 5

**Dimension:** Chart Builder Integration
**Severity:** Critical
**Current State:** No `chart_builder.R` file exists. Chart generation is inline in `server_logic.R`.
**Expected State:** `ShinyApp/R/chart_builder.R` with `is_chapter5_series()` helper, specialized builders for exploitation rate, employment decomposition, profit rate, and revenue-side series.
**Impact:** Dimension 5 (10% weight) scores 0%.

**Root Cause:**
Same as G003 — Shiny app modularization not yet performed.

**Remediation Steps:**
1. Create `ShinyApp/R/chart_builder.R`
2. Extract chart functions from `server_logic.R` into modular builders
3. Add `is_chapter5_series()` helper
4. Create specialized builders: `build_exploitation_chart()`, `build_employment_chart()`, `build_profit_rate_chart()`, `build_revenue_chart()`
5. Add error handling for missing data/series
6. Ensure Plotly configuration consistency

**Classification:** Next-session

---

### G005: No test_chapter_05.R

**Dimension:** Test Coverage
**Severity:** Critical
**Current State:** `Technical/tests/` directory exists but is empty.
**Expected State:** `tests/test_chapter_05.R` with 8 test sections: CHAPTER_METADATA, Series mapping, Data file tests, DPR existence, EPR existence, Figure catalog, Helper functions, Thematic tests.
**Impact:** Dimension 6 (10% weight) scores 0%. No automated validation of chapter integrity.

**Root Cause:**
Testing infrastructure was planned but deferred. Phase 3 had validation scripts (`validate_against_book.py`) but no R-based test file.

**Remediation Steps:**
1. Create `tests/test_chapter_05.R`
2. Add CHAPTER_METADATA tests (chapter=5, title, series_count=16)
3. Add series mapping tests (all 16 series in CH5_SERIES_MAPPING)
4. Add data file tests (7 Chopped CSVs load, columns match)
5. Add DPR/EPR existence tests
6. Add FIGURE_SERIES_CATALOG tests
7. Add thematic tests: e(1948)=1.70, e(1989)=2.44, Lp/L(1989)=0.36

**Classification:** Next-session (depends on G003, G006)

---

### G006: No FIGURE_SERIES_CATALOG.json

**Dimension:** Catalog Consistency
**Severity:** Moderate
**Current State:** File does not exist anywhere in the project.
**Expected State:** JSON catalog with entries for all 8 Chapter 5 figures (Fig 5.1-5.8), each with `chapter`, `series_ids`, `is_empirical`, `year_start`, `year_end`, `description`.
**Impact:** Dimension 7 (10% weight) scores 0%.

**Root Cause:**
The ANU_CHOPPED_CATALOG.json was created in Session 3, but the figure catalog was not part of the initial infrastructure work.

**Remediation Steps:**
1. Create `FIGURE_SERIES_CATALOG.json` (location TBD: root Technical/ or ShinyApp/data/)
2. Add 8 entries from CHAPTER_5_INVESTIGATION.md figure inventory
3. Populate series_ids: Fig 5.1 (none/conceptual), Fig 5.2 (T511,T515,T516), Fig 5.3 (T506), Fig 5.4 (T501-T505), Fig 5.5 (T513,T514), Fig 5.6 (T501,T515), Fig 5.7 (T511,T515,T516), Fig 5.8 (all T5xx)
4. Set is_empirical correctly (Fig 5.1 = false, all others = true)

**Classification:** Fix-in-session

---

### G007: T513/T514 Not in Anu Chopped Format

**Dimension:** Data File Integrity
**Severity:** Moderate
**Current State:** Profit rate data exists in `ShinyApp/data/profit_rates_1948_1989.csv` and `profit_rates_1948_2024.csv`, but not in `Inputs/ST_Chopped/ch05/` with Anu Chopped 3-row headers.
**Expected State:** `ST_Chopped/ch05/ProfitRates_1948_1989.csv` (or similar) with T513 and T514 columns in Anu Chopped format.
**Impact:** 2 series lack proper Chopped CSV representation. Known K vs K* discrepancy (DIV-001) affects data accuracy.

**Root Cause:**
Anu Chopped conversion (Session 3) covered 7 files but did not include profit rate data due to the known r* discrepancy (DIV-001: uses total K instead of productive K*).

**Remediation Steps:**
1. Resolve or document DIV-001 impact on profit rate values
2. Convert ShinyApp/data/profit_rates_*.csv to Anu Chopped format
3. Place in ST_Chopped/ch05/
4. Update ANU_CHOPPED_CATALOG.json

**Classification:** Next-session

---

### G008: TableE2/E3 Data Only Covers 1948-1961

**Dimension:** Data File Integrity
**Severity:** Moderate
**Current State:** TableE2_RevenueAccounts.csv has 14 rows (1948-1961); TableE3_LaborStatistics.csv has 17 rows (1948-1961). These cover only 14 of 42 book-period years.
**Expected State:** Full 1948-1989 coverage for revenue accounts and labor statistics, or clear documentation that 1962-1989 data requires interpolation/alternative sources.
**Impact:** Use-side series (T507-T510) and employment decomposition (T515-T516) have partial Chopped data.

**Root Cause:**
The Table E.2 and E.3 data was OCR-extracted via HDARP from Appendix E of the book, which only published annual detail for 1948-1961. Benchmark years (1948, 1958, 1967, 1977, 1989) are in the authoritative CSV, but intermediate years 1962-1989 are not available at Table E.2 granularity.

**Remediation Steps:**
1. Document the partial coverage in DPRs for affected series
2. Note that interpolation between benchmark years is the intended approach (per book methodology)
3. Consider creating interpolated Chopped CSVs for 1948-1989 using benchmark values

**Classification:** Wave 2 deferred

---

### G009: T504/T505 Not in Explicit Chopped Columns

**Dimension:** Data File Integrity
**Severity:** Moderate
**Current State:** Variable capital (V*) and surplus value (S*) exist as ratios and derived values in ExploitationComposition_1948_1989.csv, but not as explicit absolute-value columns in their own right.
**Expected State:** T504 (V* in millions $) and T505 (S* in millions $) have dedicated columns in Chopped format.
**Impact:** Cannot directly load V* and S* dollar amounts from Chopped CSVs without additional computation.

**Root Cause:**
Phase 3 calculation focused on ratios (e = S*/V*, Lp/L, V*/W) rather than levels. The authoritative CSV has ratios but not dollar amounts for V* and S*.

**Remediation Steps:**
1. Calculate V* = W × (V*/W) from NIPA total compensation + T512
2. Calculate S* = VA* - V* from appropriate inputs
3. Add as columns to Chopped CSV or create new Chopped file
4. Depends on resolving T501-T503 (TP*, C*_m, VA*) which require IO data

**Classification:** Next-session (partially Wave 2 dependent)

---

### G010: 12 Series Lack KB Integration

**Dimension:** Knowledge Base Integration
**Severity:** Moderate
**Current State:** Only 4/16 DPRs (T504, T506, T511, T512) and 2/9 EPRs (T511, T512) have Knowledge Base integration (book quotes, web research, API documentation).
**Expected State:** All 16 series DPRs and all 9 EPRs reference Knowledge_Base/ files, include source quotes with page references, and document API endpoints.
**Impact:** 12 series lack traceable provenance to the book text.

**Root Cause:**
DPR/EPR creation has only covered 4 + 2 series so far. Remediation is tied to G001 and G002.

**Remediation Steps:**
1. When creating remaining DPRs (G001), include:
   - Blockquotes from Knowledge_Base/text/ files with page references
   - HDARP source file references
   - API endpoint documentation where applicable
2. When creating remaining EPRs (G002), include web research queries and findings

**Classification:** Next-session (remediated alongside G001 and G002)

---

### G011: Figure 5.1 Needs FPR

**Dimension:** Catalog Consistency
**Severity:** Minor
**Current State:** Figure 5.1 is a conceptual/structural diagram (IO Accounts and Marxian Categories matrix), not an empirical time series. It does not have a Figure Provenance Record (FPR).
**Expected State:** Conceptual figures get FPR (Figure Provenance Record) per Anu Standard, not DPR.
**Impact:** Minimal; affects catalog completeness documentation only.

**Root Cause:**
FPR template exists in Anu Standard but no FPRs have been created yet for AS2.

**Remediation Steps:**
1. Create FPR for Fig 5.1 using FPR_TEMPLATE.md
2. Set is_empirical = false in FIGURE_SERIES_CATALOG.json

**Classification:** Next-session

---

### G012: DIV-001 Affects T513/T514 Accuracy

**Dimension:** Data File Integrity
**Severity:** Minor
**Current State:** Marxian profit rate r* = S*/K uses total capital stock K (all sectors) instead of productive capital stock K* = C*_f (productive sectors only). This is documented as DIV-001 in DIVERGENCE_REGISTER.json.
**Expected State:** r* = S*/K* where K* is restricted to productive-sector fixed assets.
**Impact:** Profit rate values in the Shiny app show a large discrepancy from book values. Any EPR for T513/T514 will have reduced faithfulness scores.

**Root Cause:**
Productive capital K* requires IO sector classification (Chapter 4 methodology) to isolate productive-sector assets from total fixed assets. This is a Wave 2 dependency.

**Remediation Steps:**
1. Document DIV-001 prominently in T513 and T514 DPRs
2. Note impact on faithfulness scores in future T513/T514 EPRs
3. Full resolution requires Chapter 4 IO classification (Wave 2)

**Classification:** Wave 2 deferred

---

### G013: Transition Visualizations Not Generated

**Dimension:** EPR Completeness
**Severity:** Minor
**Current State:** Both T511_EPR.md and T512_EPR.md reference "Chart Reference: Not yet generated" in their Transition Analysis sections.
**Expected State:** Transition plots showing book/extension overlap at 1989 splice point.
**Impact:** Documentation completeness slightly reduced; scores already account for this (95% Documentation Completeness in both EPRs).

**Root Cause:**
Shiny app visualization infrastructure not yet set up for transition-specific charts.

**Remediation Steps:**
1. Generate transition plots using R/Plotly
2. Save to Outputs/Figures/ or Technical/docs/figures/
3. Update EPR Chart Reference sections

**Classification:** Next-session

---

### G014: Book-Period-Only Series Extension Timeline Undefined

**Dimension:** EPR Completeness
**Severity:** Minor
**Current State:** 7 series (T501-T503, T507-T510) are classified as book-period-only. They depend on IO benchmark tables (Chapter 4 methodology) and use-side adjustments (Appendix D/E royalty allocations) that are not yet implemented.
**Expected State:** Clear documentation of when these series can be extended (Wave 2 timeline) and what prerequisites must be met.
**Impact:** These 7 series are N/A for EPR scoring (denominator is 9 extendable series), but their extension timeline affects overall project planning.

**Root Cause:**
Wave 2 (IO-dependent work) has not been scheduled. The SIC-NAICS transition (pre-1998 industry data not in BEA API) adds complexity.

**Remediation Steps:**
1. Document Wave 2 prerequisites in each DPR (G001)
2. Add extension timeline notes to T_SERIES_CATALOG.json
3. Consider whether some series can be partially extended without full IO methodology

**Classification:** Wave 2 deferred

---

## Remediation Roadmap

### Phase 1: Critical Infrastructure (Next Session)

| Gap ID | Action | Priority | Dependency |
|--------|--------|----------|------------|
| G006 | Create FIGURE_SERIES_CATALOG.json | High | None |
| G003 | Create data_loader.R with CH5_SERIES_MAPPING | High | None |
| G004 | Create chart_builder.R with chapter builders | High | G003 |
| G005 | Create test_chapter_05.R | High | G003, G006 |

### Phase 2: Documentation Completion (Next 2-3 Sessions)

| Gap ID | Action | Priority | Dependency |
|--------|--------|----------|------------|
| G001 | Create 12 missing DPRs | High | CHAPTER_5_INVESTIGATION.md |
| G002 | Create 7 missing EPRs | High | G001 (DPRs for target series) |
| G010 | Add KB integration to new DPRs/EPRs | Medium | G001, G002 |
| G007 | Convert profit rates to Anu Chopped format | Medium | DIV-001 assessment |
| G009 | Add explicit V*/S* columns to Chopped CSVs | Medium | T501-T503 data |
| G013 | Generate transition visualizations | Low | Shiny chart infrastructure |

### Phase 3: Deferred Items (Wave 2+)

| Gap ID | Action | Priority | Dependency |
|--------|--------|----------|------------|
| G008 | Extend TableE2/E3 coverage beyond 1961 | Low | IO benchmark tables |
| G012 | Resolve DIV-001 (K vs K*) | Medium | Chapter 4 methodology |
| G014 | Define Wave 2 timeline for book-period-only series | Low | Project scheduling |
| G011 | Create FPR for Figure 5.1 | Low | None |

---

## Impact on Scores

### Current Dimension Scores

| Dimension | Weight | Current | After Phase 1 | After Phase 2 | After Phase 3 |
|-----------|--------|---------|---------------|---------------|---------------|
| DPR Completeness | 15% | 25% | 25% | 90% | 95% |
| EPR Completeness | 15% | 22% | 22% | 85% | 90% |
| Data File Integrity | 15% | 65% | 65% | 75% | 85% |
| Series Mapping | 15% | 0% | 85% | 90% | 95% |
| Chart Builder | 10% | 0% | 70% | 80% | 85% |
| Test Coverage | 10% | 0% | 70% | 85% | 90% |
| Catalog Consistency | 10% | 0% | 85% | 90% | 95% |
| Knowledge Base | 10% | 40% | 40% | 80% | 85% |

### Projected Overall Score

- **Current:** 20.80% (INCOMPLETE)
- **After Phase 1:** 44.50% (INCOMPLETE) — Shiny infrastructure created but documentation gaps remain
- **After Phase 2:** 84.25% (ADEQUATE → near COMPLETE) — all DPRs/EPRs created, KB integrated
- **After Phase 3:** 90.50% (COMPLETE) — Wave 2 items addressed, full coverage

---

## Dependencies

### Internal Dependencies

| Gap ID | Depends On | Blocks |
|--------|------------|--------|
| G001 (DPRs) | None | G002, G005, G010 |
| G002 (EPRs) | G001 (series must have DPR first) | G013 |
| G003 (Mapping) | None | G004, G005 |
| G004 (Charts) | G003 | None |
| G005 (Tests) | G003, G006 | None |
| G006 (Catalog) | None | G005, G011 |
| G007 (T513/14 Chopped) | DIV-001 assessment | None |
| G009 (V*/S* columns) | T501-T503 data | None |
| G010 (KB integration) | G001, G002 | None |
| G012 (DIV-001) | Chapter 4 IO methodology | G007 |

### External Dependencies

- [ ] BEA SIC-era industry data (pre-1998) — not available via current API
- [ ] Chapter 4 IO methodology implementation (Wave 2)
- [ ] Appendix D/E royalty allocation methodology

---

## Risk Assessment

### Remediation Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| IO-dependent DPRs (T501-T503, T507-T510) have incomplete transformation chains | High | Medium | Document as "transformation chain pending IO methodology" in DPR Known Issues |
| T513/T514 EPR faithfulness scores reduced by DIV-001 | High | Medium | Document divergence prominently; note ceiling on faithfulness score |
| ec_u/ec_p variation post-1989 affects T512 score margin | Medium | Low | T512 EPR score (76%) is near 75% threshold; monitor if NIPA 6.2D data shows deviation |
| Shiny refactoring introduces regressions | Medium | Medium | Create test_chapter_05.R before refactoring; use existing ShinyApp as baseline |
| Phase 2 DPR/EPR quality varies across 19 new documents | Medium | Medium | Use existing T511/T512 DPR+EPR as quality reference; template consistency |

---

## Verification Plan

After remediation, verify with:

1. Run `/anu-review 5` to recalculate scores
2. Check all critical gaps (G001-G005) resolved
3. Confirm no `[PLACEHOLDER]` tags in any DPR/EPR
4. Validate EPR denominator = 9 (extendable series only)
5. Verify FIGURE_SERIES_CATALOG.json has 8 entries with correct series_ids
6. Test that `test_chapter_05.R` passes all test sections
7. Confirm overall score reaches COMPLETE (>=85%)

---

## Appendix: All Gaps

| ID | Description | Dimension | Severity | Classification | Status |
|----|-------------|-----------|----------|----------------|--------|
| G001 | 12 of 16 DPRs missing | DPR Completeness | Critical | Next-session | [ ] Open |
| G002 | 7 of 9 EPRs missing | EPR Completeness | Critical | Next-session | [ ] Open |
| G003 | No CH5_SERIES_MAPPING in data_loader.R | Series Mapping | Critical | Next-session | [ ] Open |
| G004 | No chart_builder.R for Chapter 5 | Chart Builder | Critical | Next-session | [ ] Open |
| G005 | No test_chapter_05.R | Test Coverage | Critical | Next-session | [ ] Open |
| G006 | No FIGURE_SERIES_CATALOG.json | Catalog Consistency | Moderate | Fix-in-session | [ ] Open |
| G007 | T513/T514 not in Anu Chopped format | Data File Integrity | Moderate | Next-session | [ ] Open |
| G008 | TableE2/E3 data only 1948-1961 | Data File Integrity | Moderate | Wave 2 deferred | [~] Partially Resolved |
| G009 | T504/T505 not in explicit Chopped columns | Data File Integrity | Moderate | Next-session | [ ] Open |
| G010 | 12 series lack KB integration | Knowledge Base | Moderate | Next-session | [ ] Open |
| G011 | Figure 5.1 needs FPR not DPR | Catalog Consistency | Minor | Next-session | [x] Resolved |
| G012 | DIV-001 affects T513/T514 accuracy | Data File Integrity | Minor | Wave 2 deferred | [ ] Open |
| G013 | Transition visualizations not generated | EPR Completeness | Minor | Next-session | [x] Resolved |
| G014 | Book-period-only series extension timeline undefined | EPR Completeness | Minor | Wave 2 deferred | [x] Resolved |

---

*Generated by Anu Review v1.0 | Part of the Anu Suite*
