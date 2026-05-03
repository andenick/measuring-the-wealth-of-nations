# Chapter 6 Gap Analysis -- Net Social Wage

**Generated**: 2026-02-25
**Source**: Anu Review v1.1 Audit
**Integration Score**: 77.3% (ADEQUATE)
**Target Score**: 85% (COMPLETE certification)
**Gap to Target**: 7.7 percentage points

---

## Executive Summary

Chapter 6 achieves ADEQUATE certification (77.3%) with strong infrastructure across DPRs, series mappings, chart builders, tests, and catalogs. The chapter is held back from COMPLETE certification by two primary factors:

1. **Zero EPR files** (0% on a 12%-weighted dimension) despite having extended data through 2025 already computed
2. **Data integrity issues** including an empty T608 ratio column and an inaccurate claim that NSW is universally negative

Closing the EPR gap alone would add approximately 10-12 weighted points, pushing the score above 85% and achieving COMPLETE certification. The data integrity issues, while not as impactful on the score, are more consequential for scientific accuracy and should be addressed as a P0 priority.

---

## Gap Classification

### Critical Gaps (Must fix for COMPLETE certification)

| ID | Gap | Dimension | Current | Target | Impact (weighted) | Effort |
|----|-----|-----------|---------|--------|-------------------|--------|
| G6-001 | No EPR files exist | EPR Completeness | 0% | 80%+ | +9.6 points | Medium (4-6h) |
| G6-002 | T608 NSW/V* column empty | Data File Integrity | Column empty | Populated | +1.5 points | Low (1h) |
| G6-003 | NSW sign claim incorrect | Data File + Tests + KB | 3 positive years | Accurate documentation | +2.0 points | Low (2h) |

### Moderate Gaps (Should fix for quality)

| ID | Gap | Dimension | Current | Target | Impact (weighted) | Effort |
|----|-----|-----------|---------|--------|-------------------|--------|
| G6-004 | DPR validation all PENDING | DPR Completeness | 0 checks executed | All checks run | +0.9 points | Medium (3h) |
| G6-005 | Column naming inconsistency | Data File Integrity | Mismatched names | Standardized | +0.75 points | Low (1h) |
| G6-006 | Table6_3_Extended.csv misnaming | Data File Integrity | Misleading name | Corrected | +0.45 points | Trivial (15m) |
| G6-007 | Test failures on NSW sign | Test Coverage | Will fail | Corrected assertions | +0.5 points | Low (30m) |

### Minor Gaps (Nice to have)

| ID | Gap | Dimension | Current | Target | Impact (weighted) | Effort |
|----|-----|-----------|---------|--------|-------------------|--------|
| G6-008 | DPR quotes mostly paraphrased | DPR + KB | "Derived from" prefix | Direct verbatim | +0.3 points | Low (2h) |
| G6-009 | T609 not marked as extended | Series Mapping | is_extended = FALSE | is_extended = TRUE | +0.12 points | Trivial (5m) |
| G6-010 | Tonak benchmarks not parsed | KB Integration | Unparsed DOCX | Structured data | +0.5 points | High (6h) |
| G6-011 | Test column name mismatches | Test Coverage | Tests will SKIP | Tests pass | +0.25 points | Low (30m) |

---

## Detailed Gap Analysis

### G6-001: No EPR Files Exist [CRITICAL]

**Current State**: Zero EPR files in `docs/series/` for any T6xx series. The extended dataset (nsw_1952_2025.csv, 74 rows covering 1952-2025) demonstrates that extension calculations have been performed, but no Extension Provenance Records document the methodology, data sources, or validation of the 1990-2025 period.

**What Exists**:
- nsw_1952_2025.csv: 74 rows with T601-T609 columns (except T608 which is empty)
- T607 entry in T_SERIES_CATALOG.json has `period_extended: "1952-2025"` and `api_data_files` listing NIPA tables 2.1, 3.1, 3.2, 3.3
- api_config.json documents all Ch6 NIPA tables with coverage through 2025
- data_coverage_matrix.csv shows NIPA 2.1/3.1/3.2/3.3 availability through 2025

**What Is Missing**:
- T607_EPR.md: Extension methodology for the keystone NSW series
- T601_EPR.md through T606_EPR.md: Individual component extension documentation
- T609_EPR.md: Extension documentation for the NSW/NI ratio
- Documentation of any methodology differences between book period (1952-1989) and extension period (1990-2025)
- Validation of extension data against post-1989 Tonak publications (2002 paper covers through 1997)

**Remediation**:
1. Create T607_EPR.md as the primary EPR documenting full extension methodology
2. Create T601_EPR.md through T606_EPR.md for individual components
3. Create T609_EPR.md for the NSW/NI extension
4. T608_EPR.md can be deferred until T608 data is computed
5. Each EPR should document: extension data sources, methodology continuity/changes, NIPA revision handling, validation against 2002 Tonak paper values

**Impact**: Creating EPRs for 7-8 series would move this dimension from 0% to ~85%, adding approximately 10.2 weighted points. This single remediation would push the Integration Score from 77.3% to approximately 87.5% -- achieving COMPLETE certification.

---

### G6-002: T608 NSW/V* Column Empty [CRITICAL]

**Current State**: The `T608_nsw_v_star_ratio` column exists in both nsw_1952_1989.csv and nsw_1952_2025.csv but contains no values (empty cells) for all 74 rows.

**Root Cause**: The T608 ratio requires dividing T607 (NSW) by T504 (V*, Variable Capital from Chapter 5). The Chapter 5 data has not been joined with the Chapter 6 data to compute this ratio.

**Data Available**:
- T607 (NSW): Available in all Shiny data files
- T504 (V*): Available in `ShinyApp/data/exploitation_composition_1948_1989.csv` and `exploitation_composition_1948_2024.csv`
- The join key is `year`

**Remediation**:
1. Load T504 values from Chapter 5 exploitation composition data
2. Align time periods (T607 starts 1952; T504 starts 1948; intersection is 1952-1989 for book, 1952-2024 for extended)
3. Compute T608 = T607 / T504 for each year
4. Populate the T608 column in both Shiny data files
5. Verify the ratio is negative for the book period (matching sign of NSW)
6. Update DPR validation record with computed values

**Impact**: Directly addresses a data completeness gap and makes the T608 series functional for visualization and analysis.

---

### G6-003: NSW Sign Claim Incorrect [CRITICAL]

**Current State**: Multiple documents state "NSW < 0 throughout 1952-1989":
- CHAPTER_6_INVESTIGATION.md (line 26): "NSW has been negative throughout the postwar period (1952-1989)"
- T607_DPR.md (line 72): "Key Finding: NSW < 0 for all years 1952-1989"
- data_loader.R (line 465): "NSW < 0 throughout 1952-1989; workers are net payers to the state"
- test_chapter_06.R (line 306): `expect_true(all(nsw_values < 0))`

**Actual Data**: NSW is positive for 3 of 38 years in the book period:

| Year | NSW (millions $) | Context |
|------|-----------------|---------|
| 1975 | +19,653.3 | Deep recession; benefits spiked (UI, food stamps) |
| 1976 | +4,928.2 | Recession aftermath; benefits still elevated |
| 1983 | +8,991.9 | Early recovery from 1981-82 recession |

NSW is negative for 35/38 years (92.1% of the book period).

**Analysis**: The positive NSW years correspond to deep recessions when unemployment insurance and other countercyclical benefits temporarily exceeded the tax burden. This is actually an interesting finding that enriches the narrative -- the "net social wage" flips positive only during economic crises, and only temporarily. Shaikh & Tonak's finding should be stated as: NSW is predominantly negative, with temporary reversals during severe recessions.

**Note**: It is possible that the data in the CSV files contains calculation errors or uses a different methodology than the book. The original Shaikh & Tonak (1994) finding was universal negativity. If the data here uses a different allocation methodology, this discrepancy needs investigation and documentation rather than simply accepting the CSV values as correct.

**Remediation**:
1. Investigate whether the 3 positive years are methodological artifacts or genuine results
2. Cross-check against Tonak 1987/2002 published values for those years
3. Update CHAPTER_6_INVESTIGATION.md with nuanced finding
4. Update T607_DPR.md to note the exceptions
5. Update data_loader.R shaikh_finding to be accurate
6. Fix test_chapter_06.R line 306 to test the appropriate condition (e.g., `expect_true(sum(nsw_values >= 0) <= 3)` or document the expected exceptions)
7. Add a known issue to T607_DPR.md about the 1975/1976/1983 positive years

---

### G6-004: DPR Validation All PENDING [MODERATE]

**Current State**: All 9 DPRs have Validation Record tables where every non-trivial check has status "PENDING" or "To be verified." Only the year coverage checks show "PASS."

**Example** (T601_DPR.md):
- T601 > 0 for all years: PENDING
- T601 < total personal tax: PENDING
- Worker share declining: PENDING

**Remediation**:
1. For each DPR, execute all validation checks against actual data
2. Update each check with Actual value and PASS/FAIL status
3. Document any FAIL results with explanation
4. This is a mechanical exercise once data files are confirmed correct

---

### G6-005: Column Naming Inconsistency [MODERATE]

**Current State**:
- Chopped CSV `Table6_1_TaxAccounts.csv` uses: `personal_income_tax_workers`, `social_insurance_workers`, `sales_excise_tax_workers`, `property_tax_workers`
- Shiny data `nsw_1952_1989.csv` uses: `T601_total_tax_workers`, `T602_social_insurance`, `T603_income_tax_workers`, `T604_indirect_tax_workers`
- The mapping T601<->total_tax is confusing: T601 should be personal tax, but `T601_total_tax_workers` suggests it is the total

**Specific Inconsistency**: In the Shiny data header, `T601_total_tax_workers` appears to contain total tax values (matching T604's semantics), while `T603_income_tax_workers` appears to contain personal income tax values (matching T601's semantics in the DPR). The T-series ID assignments in the column names may be swapped.

**Remediation**:
1. Audit actual column values against DPR definitions
2. Verify the T601 column in Shiny data is truly personal tax (not total tax)
3. Standardize naming convention across all files
4. Update data_loader.R `data_patterns` if file formats change

---

### G6-006: Table6_3_Extended.csv Misnaming [MODERATE]

**Current State**: `ST_Chopped/ch06/Table6_3_Extended.csv` contains 38 rows (1952-1989) -- identical to the book period. Despite the "Extended" name, it does not contain data beyond 1989. The actual extended data lives in `ShinyApp/data/nsw_1952_2025.csv`.

**Remediation**: Either:
- (a) Populate Table6_3_Extended.csv with actual 1952-2025 data, or
- (b) Rename it to `Table6_3_ShinyFormat.csv` or similar to distinguish its purpose (book data in T-series column format)

---

### G6-007: Test Failures on NSW Sign [MODERATE]

**Current State**: `test_chapter_06.R` line 306 asserts `all(nsw_values < 0)` which will FAIL given 3 positive values. Additionally, THEMATIC_BENCHMARKS tests for `tax_rate` and `benefit_rate` columns (lines 315, 337) that do not exist in the Shiny data format -- these will SKIP. TONAK_VALIDATION test for `worker_share` (line 404) will also SKIP.

**Remediation**:
1. Fix NSW sign test to match actual data (or investigate data correctness first)
2. Add `tax_rate_T_EC` column reference as alternative in tax rate test
3. Consider adding worker_share computation from available data
4. Run full test suite to verify all 30 tests pass or skip appropriately

---

### G6-008: DPR Quotes Mostly Paraphrased [MINOR]

**Current State**: Only T601_DPR.md and T607_DPR.md contain direct verbatim quotes from Shaikh & Tonak (1994). The remaining 7 DPRs use "Derived from Shaikh & Tonak" prefix on paraphrased context.

**Remediation**: Add specific page references and direct quotations from the book for each DPR's Context section. This requires access to the book text.

---

### G6-009: T609 Not Marked as Extended [MINOR]

**Current State**: In data_loader.R, T609 has `is_extended = FALSE`, but nsw_1952_2025.csv contains T609_nsw_ni_share values through 2025.

**Remediation**: Change `is_extended = FALSE` to `is_extended = TRUE` in the T609 entry of CH6_SERIES_MAPPING.

---

### G6-010: Tonak Benchmarks Not Parsed [MINOR]

**Current State**: CHAPTER_6_INVESTIGATION.md references Tonak benchmark files (NSWComparisons-EAT_NA.docx, Appendix N_Sources.docx) as "AVAILABLE -- not yet systematically extracted/parsed."

**Remediation**: Extract structured benchmark values from DOCX files into CSV or JSON format for automated cross-validation. This would enable validation of computed NSW values against the book author's own data.

---

### G6-011: Test Column Name Mismatches [MINOR]

**Current State**: Several tests reference column names (`tax_rate`, `benefit_rate`, `worker_share`) that do not exist in the current Shiny data files. These tests will SKIP rather than FAIL.

**Remediation**: Either:
- (a) Add these columns to the Shiny data files, or
- (b) Update tests to use existing column names (e.g., `tax_rate_T_EC` from the chopped CSVs)

---

## Remediation Roadmap

### Phase 1: Score to COMPLETE (Target: 85%+)

**Estimated effort**: 8-10 hours

| Step | Action | Gaps Addressed | Score Impact |
|------|--------|---------------|--------------|
| 1 | Create T607_EPR.md (keystone NSW extension) | G6-001 | +4.0 |
| 2 | Create T601-T606_EPR.md (component extensions) | G6-001 | +5.0 |
| 3 | Create T609_EPR.md (ratio extension) | G6-001 | +1.2 |
| 4 | Compute and populate T608 column | G6-002 | +1.5 |
| 5 | Investigate and document NSW sign exceptions | G6-003 | +2.0 |
| 6 | Fix test assertions for NSW sign | G6-007 | +0.5 |
| | **Subtotal** | | **+14.2** |
| | **Projected Score** | | **~87-89%** |

### Phase 2: Score to EXEMPLARY (Target: 95%+)

**Estimated effort**: 10-15 additional hours

| Step | Action | Gaps Addressed | Score Impact |
|------|--------|---------------|--------------|
| 7 | Execute all DPR validation checks | G6-004 | +0.9 |
| 8 | Standardize column naming | G6-005 | +0.75 |
| 9 | Fix Table6_3_Extended naming/content | G6-006 | +0.45 |
| 10 | Add direct book quotes to all DPRs | G6-008 | +0.3 |
| 11 | Mark T609 as extended | G6-009 | +0.12 |
| 12 | Parse Tonak benchmark files | G6-010 | +0.5 |
| 13 | Fix test column name references | G6-011 | +0.25 |
| | **Subtotal** | | **+3.27** |
| | **Projected Score** | | **~90-92%** |

**Note**: Reaching 95% (EXEMPLARY) would likely require additional work beyond the identified gaps, such as creating separate benefit decomposition charts, adding more granular validation tests, and fully reconciling with published Tonak benchmarks.

---

## Impact on Scores (Projected After Phase 1)

| # | Dimension | Weight | Current | After Phase 1 | Change |
|---|-----------|--------|---------|---------------|--------|
| 1 | DPR Completeness | 15% | 94% | 94% | -- |
| 2 | EPR Completeness | 12% | 0% | 85% | +85% |
| 3 | Data File Integrity | 15% | 80% | 92% | +12% |
| 4 | Series Mapping | 12% | 97% | 97% | -- |
| 5 | Chart Builder Integration | 8% | 100% | 100% | -- |
| 6 | Test Coverage | 10% | 95% | 98% | +3% |
| 7 | Catalog Consistency | 8% | 95% | 95% | -- |
| 8 | Knowledge Base Integration | 10% | 85% | 90% | +5% |
| | **Weighted Total** | | **77.3%** | **~88%** | **+10.7%** |

Phase 1 would move the certification from **ADEQUATE** to **COMPLETE**.

---

## Data Integrity Advisory

The finding that NSW is positive for 3 years in the book period (1975, 1976, 1983) warrants special attention. There are two possible explanations:

1. **The data is correct and the book's claim of universal negativity was wrong or used a different methodology**: The 1994 book may have used different tax allocation coefficients or benefit attribution methods that yielded universally negative NSW. The current data may use slightly different NIPA line items or allocation shares.

2. **The data contains computational errors**: The NSW values may be miscalculated due to incorrect NIPA line mapping, allocation coefficient errors, or data transcription issues.

**Recommended action**: Before modifying the test assertions, compare the 1975/1976/1983 values against:
- Shaikh & Tonak (1987) published Table 3 (covers 1952-1985)
- Shaikh & Tonak (2002) published values
- NSWComparisons-EAT_NA.docx benchmark data
- Phase 1 original LaTeX outputs

If the book and benchmark sources show negative NSW for these years, the current data has errors that need correction. If they also show positive values, the documentation should be updated to reflect the nuanced finding.

---

*Gap Analysis Complete -- Anu Review v1.1*
*Chapter 6: The Net Social Wage*
