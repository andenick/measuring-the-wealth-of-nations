# ST2 Fix and Sharpen List

**Date**: 2026-05-09
**Pipeline state**: FAIL (1 failure: V02 range checks), 59-61 series, 15 validators
**Current score**: 28 MATCH / 29 JUSTIFIED / 0 UNJUSTIFIED / 0 UNKNOWN
**Goal**: Fix all issues, sharpen all methodologies, pass all validators

---

## Category A: Pipeline Failures (Must Fix)

### A1. V02 Range Check Failures (5 FAIL)
The V02 range bounds are calibrated to the old (wrong-unit) T504/T505 levels. After DEC-020 corrected V* from 1,294 to 88.41, the range bounds need updating. Also, the corrected T506 (1958: 2.01 vs old 1.83) may exceed old bounds.

**Fix**: Read V02 code, find the RANGE_BOUNDS and SERIES_RANGE_OVERRIDES dicts, update to match corrected data ranges. Specifically:
- T504: old range probably [0, 15000], new should be [0, 5000] (billions)
- T505: old range probably [0, 30000], new should be [0, 10000] (billions)
- T506: may need wider range if 2.01 exceeds old bounds
- T513/T514: K*-based values may differ from old pre-extended values

**Effort**: 30 minutes

### A2. P04 Stale Benchmark Comment
P04 docstring still says `Benchmark: {1948: 1.70, 1958: 1.83, ...}` — the 1958 value should be 2.01 per Table H.1. The benchmark dict in the code may also be stale.

**Fix**: Update P04 docstring and any hardcoded benchmarks to match Table H.1 actual values.

**Effort**: 10 minutes

---

## Category B: Dead Code and Deprecated Artifacts

### B1. Table5_7_Extended.csv Still Referenced
Three files still reference this fabricated artifact: L03, P04, P05. T511 and T512 now bypass it (IO-extended and V*/W components respectively), but L03 still loads it and P04/P05 docstrings reference it.

**Fix**: 
- L03: Remove the ext_src / EXT_COLS code path for T506 (already uses H.1), T511 (already IO-extended), T512 (already V*/W)
- P04: Remove docstring reference, verify no code path uses it
- P05: Already bypassed, clean up docstring
- Move Table5_7_Extended.csv to `Technical/_archive/deprecated/` with deprecation note

**Effort**: 30 minutes

### B2. VariableCapital_SurplusValue.csv Legacy Fallback
L02 has a fallback path to the old wrong-unit CSV. Since the reconstructed H.1 data is now the primary source, the fallback should be removed or marked with a strong warning.

**Fix**: Remove fallback or add `print("WARNING: Using legacy wrong-unit source (DEC-020)")` if the primary fails.

**Effort**: 10 minutes

### B3. ExploitationComposition_1948_1989.csv
This file contains NIPA-derived P+/EC ratios (T506_NIPA) and log-encoded T510. T510 is still read from this file by L05. With T506 now from H.1, the T506_NIPA column is unused. T510 is still needed.

**Fix**: Document in L05 that T510 comes from this file. No code change needed, just a docstring update.

**Effort**: 5 minutes

---

## Category C: Validator Warnings (Investigate and Resolve or Document)

### C1. V03 Continuity: 6 WARN
Continuity warnings flag years where a series jumps more than expected. Likely at the 1989/1990 splice point for several series. After the V* and T506 corrections, some splice discontinuities may have changed.

**Fix**: Run V03 in detail mode, identify which series and years warn, document whether each is expected (e.g., 1996 welfare reform in T605/T606) or needs fixing.

**Effort**: 30 minutes

### C2. V06 Splice Quality: 14 WARN (up from 7)
Splice quality warnings flag series where the growth-rate splice has CR < 1.0 (connection ratio not perfect). The increase from 7 to 14 WARNs suggests the V* correction changed splice quality for several series.

**Fix**: Run V06 in detail mode, identify each warning, document whether the splice quality degraded or improved after corrections. Update splice parameters if needed.

**Effort**: 1 hour

### C3. V08 Hash Integrity: 13 WARN (up from 1)
Hash warnings mean output files changed since last verified run. Expected after all our modifications — just need to re-baseline.

**Fix**: Run V08 in "reset" or "update" mode to re-baseline hashes.

**Effort**: 10 minutes

### C4. V09 Mohun Cross-validation: 6 WARN
Mohun's exploitation rates use a different methodology (different productive/unproductive boundary). Warnings are expected divergence, not errors.

**Fix**: Document each warning. The A08 Khanjian cross-validation (ratio=0.801) already validates our methodology.

**Effort**: 15 minutes

### C5. V10 IO Consistency: 8 WARN
IO consistency checks probably flag the SIC-NAICS transition and benchmark interpolation issues.

**Fix**: Run V10 detail mode, document each warning.

**Effort**: 15 minutes

### C6. V11 External Benchmarks: 3 WARN
External benchmark comparisons likely show small deviations from published values.

**Fix**: Investigate each. May be NIPA vintage differences (our 2026 data vs published sources from 2015-2020).

**Effort**: 15 minutes

### C7. V14 Unit Consistency: 1 WARN
One series has a unit inconsistency flag. Need to identify which and fix.

**Fix**: Run V14 detail, identify the warning.

**Effort**: 10 minutes

---

## Category D: Data Quality Sharpening

### D1. K* Industry Classification Fix
L06b fetches BEA FAAt403 but this table only has broad categories (Manufacturing, Farms, Financial, Nonfarm nonmanufacturing), not detailed industry breakdown. K*/K = 1.0 because the classification matching is wrong.

**Fix**: Either (a) use a different BEA table with industry detail (FAAt301 = Current-Cost Net Stock by Industry may have better breakdown), or (b) approximate K* = K × IO_productive_output_ratio (~0.55) using the L11b ratios already computed. Option (b) is simpler and defensible.

**Effort**: 1 hour

### D2. P02b Sector V* Production Worker Fraction
P02b uses a hardcoded 0.60 production worker fraction. Should use actual BLS sector-level production worker ratios (CES*0006 / CES*0001 for each sector).

**Fix**: Load BLS CES production worker ratios by sector from `bls_ces_production_workers.csv`. Compute (Lp/L)_j for each sector. Apply to sector EC to get V*_j = EC_j × (Lp/L)_j per sector.

**Effort**: 1-2 hours

### D3. T511 IO Extension Bridging Logic
P05's T511 IO-extension uses the productive OUTPUT ratio (~0.55) as proxy for productive EMPLOYMENT ratio. Now that L11b computes a proper employment ratio (~0.60 from NIPA 6.5), the T511 extension should use the employment ratio.

**Fix**: Update P05 to prefer `ratio_productive_employment` over `ratio_productive_output` from IO_productive_ratios.csv.

**Effort**: 15 minutes

### D4. Real Productivity Measures (GNP Deflator)
A10 computes nominal q* and y (not real). The book uses 1982=100 GNP deflator. Need to fetch the GDP deflator from FRED (GDPDEF) and apply.

**Fix**: Fetch FRED GDPDEF, rebase to 1982=100, divide nominal TP* and GDP by deflator to get real values. Recompute q* = TPr/Hp and y = GDPr/H.

**Effort**: 1 hour

### D5. Extend Analytical Series to 2024
A07 (social burden rate), A09 (unproductive exploitation), A10 (productivity) only cover book period (1948-1989). Should extend to 2024 using pipeline T-series extension data.

**Fix**: A07: compute P+/S* and Eu_share for 1990-2024 using extended T505 (S*) and NIPA P+ data. A09: use extended T506 for ep, extrapolate ecu/ecp from M01 data. A10: use extended TP* (T501) and GFP* (T503).

**Effort**: 2-3 hours

---

## Category E: Documentation and Governance

### E1. Update ASSUMPTIONS.md
ASM-D-002 (Total K) is still "Open" but DEC-017 confirmed the formula is correct and L06b fetches industry data. Should be updated to "Partially resolved."

ASM-D-003 (BLS CES proxy) is "Accepted" but T511 now uses IO ratio. Should be updated.

**Fix**: Update each assumption's status and cross-references.

**Effort**: 15 minutes

### E2. Update CHECKLIST.md
The checklist has stale V01/V02 counts and doesn't reflect the analytical series (A07-A10).

**Fix**: Update validation counts, add analytical series checklist items.

**Effort**: 15 minutes

### E3. DECISION_LOG Stale References
DEC-002 references "Wave 2 IO framework" as future work, but it's now partially implemented. DEC-005 says "78% faithfulness" for T511 but T511 is now IO-extended.

**Fix**: Add status updates to relevant DEC entries.

**Effort**: 15 minutes

### E4. Series Registry Stale Metadata
Several series_registry.json entries have stale metadata: T504 still says `"source_file": "ch05/VariableCapital_SurplusValue.csv"` (wrong), T506 still lists old benchmarks.

**Fix**: Update source_file, validation reference_values, and status fields for corrected series.

**Effort**: 30 minutes

---

## Category F: Methodological Investigations

### F1. Moos Structural Shift (+0.054 vs +0.030)
Investigation 6 from the original plan. Our post-2000 NSW/GDP shift is 0.054 vs Moos's 0.030. Is this NIPA vintage, E2 exclusion, or labor share methodology?

**Fix**: Decompose: compute pre-2000 and post-2000 NSW/GDP means separately, test E2 sensitivity at alpha=0.05-0.50, check NIPA vintage impact on benefit series.

**Effort**: 1-2 hours

### F2. T504 Splice Quality (CR=0.81)
DEC-009 documented that the T504 growth-rate splice has CR=0.81. With the corrected V* levels from Table H.1, this may have changed.

**Fix**: Check the new splice quality at the 1989/1990 boundary. If CR improved, update DEC-009.

**Effort**: 15 minutes

### F3. 1990-1997 Gap Quality
The IO framework starts at 1997 (first NAICS benchmark). The 1990-1997 gap uses log-linear interpolation for ec_u/ec_p and GDP growth-rate proxy for T502/T501. These 8 years are the weakest link in the extension.

**Fix**: Check if BEA has any data for this period that could improve coverage. NIPA 6.2D starts at 1998 — could any earlier NIPA tables help?

**Effort**: 30 minutes

---

## Priority Order

### Immediate (< 1 hour, fix pipeline PASS):
1. A1 (V02 ranges)
2. A2 (P04 benchmark)
3. B1 (Table5_7_Extended cleanup)
4. C3 (V08 hash re-baseline)

### Short (1-3 hours, sharpen data quality):
5. D1 (K* classification fix)
6. D3 (T511 employment ratio)
7. D4 (real productivity deflator)
8. B2 (legacy fallback cleanup)
9. C1/C2 (continuity + splice warnings)

### Medium (3-6 hours, extend and investigate):
10. D5 (extend A07/A09/A10 to 2024)
11. D2 (sector V* production worker fraction)
12. F1 (Moos shift investigation)
13. E1-E4 (documentation updates)

### Lower priority (can be deferred):
14. C4-C7 (remaining validator warnings)
15. F2 (splice quality check)
16. F3 (1990-1997 gap investigation)

---

## Total Effort Estimate

| Category | Items | Hours |
|----------|-------|-------|
| A: Pipeline failures | 2 | 0.5 |
| B: Dead code cleanup | 3 | 0.75 |
| C: Validator warnings | 7 | 2.0 |
| D: Data quality | 5 | 5.5 |
| E: Documentation | 4 | 1.25 |
| F: Investigations | 3 | 2.0 |
| **Total** | **24 items** | **~12 hours** |

---

*List compiled 2026-05-09 from pipeline output analysis, code audit, decision log review, and KB findings cross-reference.*
