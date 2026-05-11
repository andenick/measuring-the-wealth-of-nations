# ST2 Investigations and Improvements — What's Left to Explore

**Date**: 2026-05-09
**Pipeline state**: PASS, idempotent (3 consecutive runs), 59 series + 3 analytical, 0 FAIL
**Methodology**: 28 MATCH / 29 JUSTIFIED / 0 UNJUSTIFIED / 0 UNKNOWN
**Analytical**: Social burden rate, unproductive exploitation, Marxian productivity, Khanjian cross-validation, Ochoa regression — all operational 1948-2024

---

## Category I: Empirical Investigations (New Findings)

These produce RESULTS, not just replications — publishable findings about the post-1989 US economy.

### I-1. What Happened to the Social Burden Rate After 1989?

**Question**: The book shows b (social burden rate = unproductive expenses / surplus value) rose from 0.56 to 0.66 during 1948-1989. Our A07 extension shows P+/S* ranges 0.42-0.80 for the full 1948-2024 period. What's the trajectory?

**Specific sub-questions**:
- Did neoliberalism (1989-2000) reverse the rising b?
- Did financialization (2000-2008) accelerate it?
- What did the GFC (2008-2010) do to the surplus decomposition?
- Is the COVID-era (2020-2022) NSW spike visible in b?
- Did the Reagan-era profit rate recovery (1980-1989) continue under Clinton/Bush/Obama?

**Method**: Plot A07 series for full 1948-2024 period. Compute period means for 1948-1973, 1973-1980, 1980-1989, 1989-2000, 2000-2008, 2008-2020, 2020-2024. Test for structural breaks at each boundary.

**Data**: Already computed in A07. Just needs analysis + figures.

**Output**: Time-series figure with annotated phases. Table of period means. Structural break test results.

**Effort**: 2 hours

### I-2. Has the Exploitation Rate Convergence Continued?

**Question**: The book shows eu/ep converging from 0.80 to 0.97 (1948-1989). A09 extends to 2024. Has convergence continued, reversed, or reached parity?

**Specific sub-questions**:
- Did eu surpass ep permanently after the 1978 crossover noted in the book?
- What does the gig economy / platform labor do to the productive/unproductive wage differential?
- Is there a structural break around 2008 or 2020?

**Method**: Plot A09 eu, ep, eu/ep for 1948-2024. Check if eu > ep consistently post-1989.

**Effort**: 1 hour

### I-3. The Productivity Slowdown — Does the Marxian Measure Also Slow?

**Question**: The book shows q* (Marxian) grows 2-3x faster than y (orthodox) through 1989. Our A10 extends to 2024 with real 1982$ values. Does this pattern continue?

**Specific sub-questions**:
- The "new economy" productivity surge (1995-2005): is it visible in q* or only in y?
- The post-2005 productivity slowdown: does q* also slow, or is it an artifact of rising unproductive employment?
- COVID productivity spike (2020-2021): real or compositional?

**Method**: Plot q*, y*, y for 1948-2024 in real 1982$. Compute growth rates by period. Decompose q*/y ratio into TP*/GDP and L/Lp components.

**Effort**: 2 hours

### I-4. The NAICS-Era Price-Value Regression Decline

**Question**: SIC-era R² ≈ 0.72-0.93 (across 6 benchmarks). NAICS-era R² ≈ 0.44-0.60 (across 5 benchmarks). Is this decline real structural change or data artifact?

**Specific sub-questions**:
- Is the R² decline monotonic? Or does it fluctuate across NAICS years?
- Does the number of sectors matter? SIC has 80-83 valid sectors, NAICS only 58.
- If we aggregate NAICS to match SIC sector count (~30 sectors), does R² improve?
- Is the decline concentrated in specific sectors (FIRE, tech, healthcare)?

**Method**: Run Ochoa regression at multiple aggregation levels. Identify which sectors contribute most to price-value deviation. Compare SIC and NAICS sector counts.

**Effort**: 3 hours

### I-5. Sensitivity Analysis on Key Assumptions

**Question**: How much do results change under different assumptions?

**Tests**:
1. **VA*/W**: constant 1.238 vs year-varying from M01 → impact on T506 extension
2. **IO productive ratio**: output ratio (~0.55) vs employment ratio (~0.60) → impact on T511 extension
3. **Total K vs K***: full K vs K×0.567 → impact on r* level
4. **NSW methodology**: old 40% defense exclusion vs Appendix N 3-group → impact on T607 extension
5. **T504 splice anchor**: H.1 V*=1206.4 vs old Phase 3 V*=11007 → impact on exploitation chain

**Method**: For each assumption, run the pipeline twice with different parameter values, compare output series. Report max absolute deviation, mean deviation, and whether the TREND changes.

**Output**: Sensitivity matrix showing which assumptions matter most.

**Effort**: 3-4 hours

### I-6. Structural Break Tests

**Question**: Where are the regime changes in the Marxian series?

**Break points to test**:
- 1973 (oil shock, end of golden age)
- 1980 (Volcker/Reagan)
- 1996 (welfare reform, PRWORA)
- 2001 (dot-com crash)
- 2008 (GFC)
- 2020 (COVID)

**Series to test**: T506 (exploitation rate), T511 (productive labor share), T607 (NSW), r* (profit rate), b (social burden rate), q* (productivity)

**Method**: Chow test or Bai-Perron at each candidate break point. Report F-statistic and p-value. Identify endogenous breaks if any.

**Effort**: 3 hours (requires statsmodels)

---

## Category II: Data Quality Improvements

### II-1. Full Table H.1 Digitization Verification

**What**: The 1965-1969 values in our digitized Table H.1 were partially interpolated from Table I.1 row 23 where the H.1 PDF columns were garbled. These 5 years should be re-verified against the original PDF with more careful reading.

**Method**: Re-read chunk_35 PDF pages 4-5 (the 1965-1969 columns) with maximum attention. Cross-check each value against the S* = VA* - V* identity and the S*/V* ratio.

**Effort**: 1 hour

### II-2. Read Remaining 23 KB Chunks

**What**: 23 of 40 HDARP chunks remain unread. These cover:
- Chunks 1-5: Chapters 1-2 (theoretical foundations)
- Chunks 6-9: Chapter 3 (sectoral structure, IO-Marxian mapping)
- Chunks 20-21: Chapter 6 (international comparisons, Wolff data)
- Chunks 25-30: Chapters 7-9 (conclusions, appendices A-D)
- Chunk 34: Appendix G completion

**Priority**: Chunks 6-9 (sector classification rules for Wave 2) > Chunks 25-30 (conclusions for LaTeX paper) > Chunks 1-5 (theory for paper intro) > Chunks 20-21 (international for N-series)

**Effort**: 4-6 hours across 2 sessions

### II-3. 1992 IO Benchmark Bridge

**What**: The 1978-1996 gap in the IO framework is the weakest interpolation zone. The 1992 BEA benchmark (published in dual SIC/NAICS format) would narrow it.

**Method**: Check BEA archive for 1992 benchmark IO tables. If available, download, parse, and incorporate into L11/L11b as a bridge point.

**Effort**: 2-3 hours

### II-4. BLS Sector-Level Production Worker Ratios

**What**: P02b uses a hardcoded 0.60 production worker fraction. The BLS CES data has sector-level ratios (CES*0006/CES*0001) for mining, construction, manufacturing that are more accurate (~0.65-0.71).

**Method**: Parse bls_ces_production_workers.csv for sector-level ratios. Compute weighted average across productive sectors. Replace hardcoded 0.60 with data-driven fraction.

**Effort**: 1 hour

### II-5. T504 Splice Quality Improvement

**What**: T504 connection ratio at 1989/1990 = 1.109 (10.9% jump). This is the largest splice discontinuity in the pipeline.

**Method**: Instead of anchoring at the 1989 book value (1206.4), try anchoring at a computed 1989 value from BEA data to ensure continuity. Or use level-matching at 1998 (first NAICS year with good EC data) and interpolate 1990-1997.

**Effort**: 1-2 hours

---

## Category III: Extension and Generalization

### III-1. International Comparisons Update

**What**: The book covers Mage (US), Wolff (Puerto Rico), Gouverneur (Belgium), Aglietta (France), and our N-series replicate Turkey, NZ, and several US studies. Could extend with modern international data.

**Specific possibilities**:
- Turkey: extend N1601/N1602 beyond 2006 using World Bank or OECD data
- NZ: update Cronin data with Stats NZ modern releases
- New country: China or India using Penn World Table labor share data

**Effort**: 4-8 hours per country

### III-2. Post-2024 Projection

**What**: The pipeline extends to 2024. Could add simple projections to 2025-2030 based on trend extrapolation and/or economic scenarios.

**Method**: Use exponential smoothing or AR(1) on key series. Three scenarios: baseline, recession, acceleration.

**Effort**: 2-3 hours

### III-3. Interactive Dashboard

**What**: The Shiny app exists but needs updating with all the new analytical series (A07-A10). Could also build a Python-based dashboard (Streamlit/Dash).

**Effort**: 4-6 hours

---

## Category IV: Documentation and Publication

### IV-1. LaTeX Methodology Paper

**What**: Every formula with book page reference, KB verification status, and data provenance. This is the publication vehicle.

**Structure**:
1. Introduction: Shaikh & Tonak (1994) contribution, our replication scope
2. Data: Table H.1 digitization, BEA/BLS/FRED sources, IO framework
3. Methodology: Chapter-by-chapter series construction, Principle 3 compliance
4. Results: 59 series replicated, 4 analytical series, cross-validations
5. Extensions: Post-1989 trends (social burden, exploitation, productivity)
6. Discussion: Price-value regression decline, Moos shift, structural breaks

**Effort**: 8-12 hours

### IV-2. GitHub Repository Polish

**What**: README update, requirements.txt verification, .gitignore for API keys, clean commit history.

**Effort**: 1-2 hours

### IV-3. Replication Documentation

**What**: Step-by-step guide for anyone to reproduce our results from scratch. Including: which API keys to get, which files to download, in what order to run scripts.

**Effort**: 2-3 hours

---

## Priority Matrix

| # | Item | Type | Effort | Impact | Priority |
|---|------|------|--------|--------|----------|
| I-1 | Social burden rate post-1989 | Finding | 2h | Very high | 1 |
| I-3 | Productivity slowdown 1948-2024 | Finding | 2h | Very high | 2 |
| I-2 | Exploitation convergence | Finding | 1h | High | 3 |
| I-5 | Sensitivity analysis | Rigor | 3-4h | High | 4 |
| II-4 | BLS sector production worker ratios | Quality | 1h | Medium | 5 |
| I-4 | Price-value regression decline | Finding | 3h | High | 6 |
| II-5 | T504 splice quality | Quality | 1-2h | Medium | 7 |
| I-6 | Structural break tests | Rigor | 3h | High | 8 |
| II-1 | Table H.1 1965-69 verification | Quality | 1h | Low | 9 |
| IV-1 | LaTeX paper | Publication | 8-12h | Very high | 10 |
| II-2 | Remaining KB chunks | Research | 4-6h | Medium | 11 |
| II-3 | 1992 IO benchmark | Quality | 2-3h | Medium | 12 |
| IV-2 | GitHub polish | Delivery | 1-2h | Medium | 13 |
| IV-3 | Replication documentation | Delivery | 2-3h | Medium | 14 |
| III-1 | International comparisons | Extension | 4-8h | Medium | 15 |
| III-2 | Post-2024 projection | Extension | 2-3h | Low | 16 |
| III-3 | Interactive dashboard | Extension | 4-6h | Low | 17 |

---

## Suggested Session Plan

### Next session: "The Findings" (4-5 hours)
- I-1: Social burden rate post-1989 (2h)
- I-3: Productivity slowdown full period (2h)
- I-2: Exploitation convergence (1h)
- Output: 3 publication-quality time-series figures with annotated phases

### Following session: "The Rigor" (4-5 hours)
- I-5: Sensitivity analysis (3-4h)
- II-4: BLS sector ratios (1h)
- II-5: T504 splice improvement (1h)

### Third session: "The Deep Dive" (4-5 hours)
- I-4: Price-value regression decline (3h)
- I-6: Structural break tests (3h)

### Fourth session: "The Paper" (8-12 hours across 2 sessions)
- IV-1: LaTeX methodology paper
- IV-2: GitHub polish
- IV-3: Replication documentation

---

*Plan authored 2026-05-09. Based on complete pipeline (59 series, 3 analytical, all validators passing, idempotent across runs) and comprehensive KB review (17/40 chunks).*
