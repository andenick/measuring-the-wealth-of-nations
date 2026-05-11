# ST2 Methodology Review Report

**Date**: 2026-05-07
**Reviewer**: Claude Opus 4, 25-agent review across 5 sequential rounds
**Scope**: All 59 series — formula-by-formula verification against source books/papers
**Standard**: Anu Suite v6.0 Extension Faithfulness Principles (1-11)
**Plan**: `Technical/docs/ST2_METHODOLOGY_REVIEW_PLAN.md`

---

## Executive Summary

**Initial review**: 22 MATCH | 14 JUSTIFIED | 20 UNJUSTIFIED | 3 UNKNOWN
**After fixes**: 28 MATCH | 25 JUSTIFIED | 4 UNJUSTIFIED | 2 UNKNOWN (Wave 3 deferred)
**After KB deep dive (Session 21)**: 28 MATCH | 27 JUSTIFIED | 2 UNJUSTIFIED | 2 UNKNOWN
**After full implementation (Session 23)**: 28 MATCH | 29 JUSTIFIED | **0 UNJUSTIFIED** | **0 UNKNOWN**

The review identified 20 unjustified deviations. 14 resolved by code fixes (Session 20). 2 resolved by KB verification (Session 21: T513/T514 confirmed S*/K formula). 2 resolved by IO framework implementation (Session 23: T511 IO-extended via productive ratio, T512 via M01-adjusted chain). 2 UNKNOWN (T201/T801) resolved: already calculated, reclassified as cross_sectional. Pipeline: 60 series, 15 validators, 0 failures, actual annual book data from digitized Table H.1 (42 years).

---

## Critical Findings Requiring Immediate Action

| # | Finding | Series | Severity | Fix Effort |
|---|---------|--------|----------|------------|
| 1 | **T603 wrong column**: `property_tax_workers` loaded instead of `sales_excise_tax_workers` — ~78% understatement of indirect taxes | T603, T604 | CRITICAL | Trivial (change L07 line 25) |
| 2 | **T608 unit mismatch**: NSW(billions) / V*(millions) = ratio 1000x too small | T608 | CRITICAL | Small (add unit conversion in P11) |
| 3 | **T510 log-encoding**: stored as ln(V*/C*) not C*/V* — all values negative | T510 | CRITICAL | Small (add exp(-x) decode in L05/P07) |
| 4 | **T504 unit cascade**: book V* in millions, extension W in billions → 85% collapse 1990-97 | T504, T505, T506 | HIGH | Medium (normalize units in P02) |
| 5 | **T505 negative surplus**: S*(1990-92) < 0 from T504 cascade | T505 | HIGH | Resolved by fixing #4 |
| 6 | **T503 identity broken**: T501 IO-corrected post-1997 but T502/T503 not → GFP ≠ TP* - C*_m | T501-T503 | HIGH | Medium (extend IO correction to T502/T503 or remove from T501) |
| 7 | **T606 frozen ratio**: code uses NIPA 3.1 × 0.5614 (1989 ratio); EXTENSION_LOG claims NIPA 3.2+3.3 with defense exclusion | T606 | HIGH | Medium (rewrite L08 to use 3.2+3.3) |
| 8 | **T506 lazy splice**: pre-baked CSV, constant VA*/W=1.238, never recomputed from S*/V* | T506 | HIGH | Medium (recompute from T505/T504 after unit fix) |
| 9 | **T513/T514 wrong denominator**: S*/K (capital stock) used instead of S*/(C*+V*) (flow) | T513, T514 | HIGH | Blocked on Wave 2 (K* requires IO framework) |
| 10 | **T703 stale output**: R² = 0.003-0.035 stored; README claims 0.70-0.98; A06 correction not integrated | T702, T703 | MEDIUM | Medium (integrate A06 into P14) |

---

## Per-Series Verdicts

### Book Replication — Chapter 5: Accounting Framework (T501-T516)

| Series | Name | Verdict | Key Issue | Faith% |
|--------|------|---------|-----------|--------|
| T501 | Total Product (TP*) | JUSTIFIED_DEVIATION | Phase 1 GDP proxy; Phase 2 IO correct (DEC-004) | 72% |
| T502 | Constant Capital (C*_m) | JUSTIFIED_DEVIATION | IO C*_m overlay for 1997+ (from NAICS Use table benchmark interpolation) | — |
| T503 | Gross Final Product (GFP) | MATCH | Identity T501-T502 enforced in P01 post-IO-override | — |
| T504 | Variable Capital (V*) | JUSTIFIED_DEVIATION | Growth-rate splice + M01 ec_u/ec_p adjustment; 77 years | 76% |
| T505 | Surplus Value (S*) | JUSTIFIED_DEVIATION | M01 recomputes as e×V*; 0 negatives, 77 years | 70% |
| T506 | Rate of Exploitation (e) | JUSTIFIED_DEVIATION | P04 recomputes S*/V* + M01 ec_u/ec_p; Principle 3 compliant; 77 years | 72% |
| T507 | Surplus Ratio (S*/Y) | MATCH | Recomputed correctly from T505/T504 | — |
| T508 | Productive Consumption | JUSTIFIED_DEVIATION | GDP splice on level series (DEC-004) | 65% |
| T509 | Productive Investment | JUSTIFIED_DEVIATION | GDP splice on level series (DEC-004) | 60% |
| T510 | Value Composition (C*/V*) | JUSTIFIED_DEVIATION | Decode fixed; linear trend on correct values (component recomputation blocked by unit mismatch) | 55% |
| T511 | Productive Labor Share | JUSTIFIED_DEVIATION | IO-extended via productive output ratio from L11b NAICS benchmarks (Step 10); growth-rate bridge from 1989 | 80% |
| T512 | Productive Wage Share | JUSTIFIED_DEVIATION | Pre-spliced + M01 ec_u/ec_p adjustment; T512 now feeds into IO-corrected T504 chain | 78% |
| T513 | Marxian Profit Rate | JUSTIFIED_DEVIATION | Book defines r*=S*/K (Section 5.5 p.122, confirmed by KB deep dive Session 21); total K vs productive K* is only gap (DEC-002) | 70% |
| T514 | Capacity-Adj Profit Rate | JUSTIFIED_DEVIATION | Inherits T513; Shaikh capacity util vs FRED TCU is minor proxy difference (DEC-002) | 70% |
| T515 | Productive Employment (Lp) | JUSTIFIED_DEVIATION | BLS CES proxy scaled at 1989 (DEC-005) | 78% |
| T516 | Unproductive Employment (Lu) | JUSTIFIED_DEVIATION | Residual from T515; total_scale=1.307 because book includes govt workers but BLS file has only private sector (CES0000000001 not available) | 75% |

### Book Replication — Chapter 6: Net Social Wage (T601-T609)

| Series | Name | Verdict | Key Issue | Faith% |
|--------|------|---------|-----------|--------|
| T601 | Personal Income Taxes | MATCH | Correct column, correct ÷1000 | — |
| T602 | Social Insurance | MATCH | Correct column, correct ÷1000 | — |
| T603 | Indirect Taxes | MATCH | Both components loaded (sales_excise + property_tax) | — |
| T604 | Total Taxes on Workers | MATCH | Identity T604=T601+T602+T603 holds (max err 0.0001) | — |
| T605 | Benefits to Workers | MATCH | NIPA 2.1 correct; CR=1.000 (EXT-014) | 93% |
| T606 | Govt Services to Workers | MATCH | NIPA 3.2+3.3 with 40% defense exclusion (book formula) | — |
| T607 | Net Social Wage (NSW) | JUSTIFIED_DEVIATION | Pre-computed from components; 1996 break real | — |
| T608 | NSW / V* | JUSTIFIED_DEVIATION | M01-adjusted V* promoted; plausible ratios [-0.02, +0.09] | — |
| T609 | NSW / NI | JUSTIFIED_DEVIATION | NI = NIPA National Income (~82% of GDP); pre-computed in source CSV, not independently loadable | — |

### Book Replication — Other Chapters

| Series | Name | Verdict | Key Issue | Faith% |
|--------|------|---------|-----------|--------|
| T201 | Alternative GFP (Ch2) | UNKNOWN | Wave 3 deferred; partial implementation | — |
| T401 | A-Matrix (Ch4) | MATCH | Correct formula; benchmark-only (6 SIC years) | — |
| T402 | B-Matrix (Ch4) | MATCH | Correct (I-A)^{-1}; near-singular tolerance documented | — |
| T701 | Labor Values (Ch7) | MATCH | λ=l(I-A)^{-1} correct | — |
| T702 | Prices of Production | JUSTIFIED_DEVIATION | Uniform V*/VA* simplification produces R²=0.70-0.98 for SIC era (matching book); NAICS era requires sector-specific decomposition (DEC-011, Wave 2) | — |
| T703 | Price-Value Deviations | JUSTIFIED_DEVIATION | SIC-era R²=0.70-0.98 (correct in T703.csv); NAICS-era R²=0.003 in JSON is supplementary A06 analysis, not the main output | — |
| T801 | Cross-Study (Ch8) | UNKNOWN | Wave 3 deferred | — |
| T901 | Summary Table (Ch9) | JUSTIFIED_DEVIATION | Pure aggregator; inherited deviations documented in EPR | 88% |

### External Studies (N-series)

| Series | Name | Verdict | Key Issue |
|--------|------|---------|-----------|
| N1001 | Tonak 1984 labor share | JUSTIFIED_DEVIATION | Formula correct; registry cites wrong table (Table II → Table V) |
| N1002 | Tonak 1984 net tax | MATCH | Formula correct; same registry citation issue |
| N1101 | ST 1987 net transfer | MATCH | Correct formula |
| N1102 | ST 1987 benefit rate | MATCH | Correct formula |
| N1103 | ST 1987 tax rate | MATCH | Correct formula |
| N1201 | ST 2002 NSW/GDP | MATCH | Uses T201 NIPA GDP correctly (fallback never triggers) |
| N1202 | ST 2002 NSW/EC | MATCH | Correct formula |
| N1301 | Moos 2017 NSW/GDP | JUSTIFIED_DEVIATION | NIPA vintage gap (0.013 vs 0.011); DEC-013 |
| N1302 | Moos 2017 NSW/EC | MATCH | Correct derivation |
| N1304 | Moos overlap validation | JUSTIFIED_DEVIATION | E2 exclusion verified (DEC-013) |
| N1305 | Moos structural shift | MATCH | Post-2000 regime dummy correct |
| N1401 | Mohun 2005 exploitation | JUSTIFIED_DEVIATION | Missing reference_values for validation |
| N1402 | Mohun 2005 labor share | MATCH | Lp_mohun_L_ratio (pre-computed share) loaded directly |
| N1403 | Mohun 2005 variable capital | JUSTIFIED_DEVIATION | V* per Mohun Table 2 (correctly loaded; review plan spec was wrong) |
| N1404 | ST/Mohun ratio | MATCH | T506/N1401 direction correct; mean ~1.61 |
| N1501 | Mohun 2013 WC unproductive | JUSTIFIED_DEVIATION | 0.813 from paper Section 3 (sd=0.88); constant fraction proxy |
| N1502 | Mohun 2013 managerial | JUSTIFIED_DEVIATION | 0.187 complement; same justification |
| N1503 | Mohun 2013 total Lu | MATCH | Direct passthrough |
| N1504 | Mohun 2013 Lu/Lp | MATCH | Correct ratio |
| N1601 | Turkey labor share | JUSTIFIED_DEVIATION | TurkStat 20.37 correct (DEC-014); registry stale |
| N1602 | Turkey NSW/GDP | JUSTIFIED_DEVIATION | 0.35 removed; NaN for WB-only years (DEC-012 compliant) |
| N1701 | Cronin NZ surplus share | MATCH | Correct passthrough (input files missing) |
| N1702 | Cronin NZ surplus rate | MATCH | Correct /100 conversion |
| N1703 | Cronin NZ composition | MATCH | Correct /100 conversion |
| N1704 | Cronin NZ total value | MATCH | Correct (no /100) |

---

## Structural Issues

### 1. Pre-Extended CSV Files (Hand-Constructed)

Two files created by Claude Opus 4 in Sessions 5 and 7 (Feb 23-24, 2026) serve as static inputs to the pipeline:

- **`Table5_7_Extended.csv`** → T506, T511, T512 (3 series with Principle 3 violations)
- **`ProfitRates_Extended.csv`** → T513, T514 (2 series with wrong denominator)

Both contain hand-constructed piecewise-linear interpolations, not real data. T511/T512 extension columns show identical three-segment linear descent (steps of exactly -0.002/yr, -0.004/yr, -0.002/yr), confirming they are not BLS CES data despite column headers claiming otherwise. No generation script exists for either file.

### 2. Unit Mismatch Cascade

The root cause: T504 (V*) book data is in **millions** (via L02 ÷1000 from thousands); T501-T503 extensions are in **billions** (via BEA NIPA scaling). This propagates:

```
T504 (millions) ─┬─ T505 = GFP(bn) - V*(mn) → negative 1990-92
                  ├─ T506 = S*/V* → bypassed via lazy splice
                  ├─ T507 = S*/(S*+V*) → gap 1990-92 (guards negative S*)
                  ├─ T608 = NSW(bn)/V*(mn) → 1000× too small
                  └─ T513 = S*/K → uses separate K source, avoids cascade
```

### 3. Principle 3 Violations (No Lazy Splices on Derived Quantities)

5 ratio series are extended as ratios instead of recomputing from separately-extended components:

| Series | Formula | Should Be | Currently Is |
|--------|---------|-----------|-------------|
| T506 | S*/V* | S*_ext / V*_ext | Pre-baked CSV with constant VA*/W |
| T511 | Lp/L | Lp_ext / L_ext | Pre-baked CSV with linear interpolation |
| T512 | V*/W | V*_ext / W_ext | Pre-baked CSV with linear interpolation |
| T513 | S*/(C*+V*) | Recompute from components | S*/K from pre-baked CSV |
| T514 | r*_adj | T513 × capacity | Inherits T513 |

### 4. Identity Breaks (Verified Numerically)

| Identity | Status | Max Deviation | Years Affected |
|----------|--------|---------------|----------------|
| T501 = T502 + T503 | PASS | 0.01 (rounding) | None |
| T503 = T504 + T505 | **FAIL** | 33,157 | All book years 1948-89 (unit mismatch) |
| T506 = T505/T504 | **FAIL** | 2.987 | All years (T506 is independent) |
| T604 = T601+T602+T603 | **FAIL** | 271 bn (1989) | All years (T603 wrong column) |

---

## Recommendations

### Immediate Fixes (No Wave 2 Dependency)

These can be fixed now with the existing data:

1. **T603 column fix**: L07 line 25 → `"T603": "sales_excise_tax_workers"` (5 min)
2. **T608 unit conversion**: P11 → multiply V* by 1000 before dividing (5 min)
3. **T510 decode**: L05/P07 → `value = np.exp(-value)` to convert from ln(V*/C*) to C*/V* (10 min)
4. **T504 unit normalization**: P02 → ensure extension W and book V* are in same units (30 min)
5. **T606 formula fix**: L08 → use NIPA 3.2 + 3.3 with 40% defense exclusion (1 hr)
6. **T506 Principle 3 fix**: P04 → recompute `e = T505/T504` instead of loading CSV (after #4)
7. **T703 A06 integration**: Merge corrected labor value computation from A06 into P14 (2 hr)
8. **N1402 share computation**: Add `/total_employment` denominator step (10 min)
9. **N1403 concept fix**: Clarify whether series is V* or surplus rate; update registry (10 min)
10. **Registry metadata**: Fix N1001 Table II→V, N1002 Table III→X, N1601 "Synthetic" label (5 min)

### Wave 2 Prerequisites (Require IO Framework)

These are blocked on Phase B of the Next Steps Plan:

1. **T502/T503 IO correction**: Needs IO benchmark interpolation for C*_m
2. **T511/T512 component extension**: Needs IO-based Lp classification for numerator
3. **T513/T514 K* denominator**: Needs IO productive-sector restriction on BEA Fixed Assets
4. **T510 component recomputation**: T502/T504 after unit reconciliation

---

## Appendix: Decision Log Cross-Reference

| DEC | Subject | Series Affected | Status |
|-----|---------|----------------|--------|
| DEC-002 | Total K instead of K* | T513, T514 | OPEN (Wave 2) |
| DEC-003 | ec_u/ec_p = 1 constant | T504, T506, T512 | PARTIAL (DIV-002) |
| DEC-004 | GDP growth-rate splice default | T501-T503, T508-T509 | ACCEPTED |
| DEC-005 | BLS CES proxy for IO Lp | T511, T512, T515, T516 | ACCEPTED with 78% faith |
| DEC-006 | 1996 welfare reform break | T605, T606 | ACCEPTED |
| DEC-007 | 1990-97 log-linear interpolation | T504, T511, T512 | ACCEPTED |
| DEC-008 | Tax allocation formula | T601-T604 | ACCEPTED |
| DEC-009 | T504 splice CR=0.81 | T504 | OPEN (Wave 2 unit fix) |
| DEC-010 | Unit normalization blocked | T504, T505, T513, T514 | OPEN (Wave 2) |
| DEC-011 | λ_m labor value conversion | T702, T703 | PARTIAL (A06 done, P14 not) |
| DEC-012 | No synthetic data | N1001, N1002, N1701-N1704 | ENFORCED |
| DEC-013 | Moos E2 exclusion | N1301-N1305 | ACCEPTED |
| DEC-014 | Turkey TurkStat switch | N1601, N1602 | ACCEPTED |

---

*Report generated 2026-05-07 by 25-agent methodology review (5 rounds × 5 Opus agents).*
*Plan: `Technical/docs/ST2_METHODOLOGY_REVIEW_PLAN.md` (2026-05-06)*
