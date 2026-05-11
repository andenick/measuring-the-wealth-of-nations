# ST2 Remaining Investigations Plan

**Date**: 2026-05-07
**Context**: Post-methodology-review. 10 code fixes implemented, pipeline passing. This plan covers issues that need deeper investigation — not simple code fixes or Wave 2 blocked items.

---

## Investigation 1: T702/T703 Labor Value Regression (R² = 0.003–0.035)

### Problem
The book reports R² = 0.98 for the labor-value/price-of-production regression (1958 data). Our pipeline produces R² = 0.003–0.035 across all benchmark years (1997–2017), even with A06's "corrected" formula. The README claims 0.70–0.98 but no output file substantiates this.

### Why A06 Still Fails
A06 applies the correct formula (c_j = λ* @ A, λ_m conversion, sector-specific V_j) but only runs on NAICS-era data (1997–2017). The book's R² = 0.98 was computed on 1958 SIC data with 85 sectors. Possible explanations for the gap:

1. **Aggregation**: NAICS-era BEA GDP-by-Industry data has ~71 sectors vs 85 SIC sectors. Aggregation reduces variation and deflates R².
2. **Concordance noise**: The `io_85_to_nipa_13_concordance.csv` mapping between SIC and NAICS introduces misclassification.
3. **Data era**: The labor theory of value predicts tighter price-value correspondence in economies with less financialization. 1958 (manufacturing-heavy) vs 2017 (services-heavy) may genuinely diverge.
4. **Hours data quality**: L12 computes `hp*` (hours per unit output) from employment × average hours. If employment is headcount and output is gross output in dollars, the ratio depends on the unit of output (dollars vs physical units).
5. **Regression specification**: A06 regresses `log(λ*)` on `log(pp*)` — but the book regresses `log(market prices)` on `log(labor values)`. These are different: pp* is a theoretical construct, not observed market prices.

### Investigation Steps

1. **Reproduce book's 1958 result**: Run P14/A06 specifically on the 1958 SIC IO matrices (which exist — L11 loads them). Verify R² ≈ 0.98 for 1958. If it works for 1958 but not 1997+, the issue is era-specific.
2. **Check regression variables**: The book regresses observed sector prices (p_j = GO_j/x_j in dollars per physical unit) on computed labor values (λ_j in hours per physical unit). Verify that P14/A06 use the same variables, not transformed versions.
3. **Compare sector counts**: How many sectors have valid data (positive λ*, positive pp*) per benchmark year? If only 20-30 survive filtering, R² will be low from insufficient variation.
4. **Test with 1977 SIC data**: The last pre-NAICS year. If R² is reasonable (>0.70), the problem is the concordance/NAICS transition.
5. **Read the book's Ch7 methodology carefully**: KB chunks 10-11 should describe exactly which prices are regressed on which values. The key is whether it's `log(p)` on `log(λ)` (market price on labor value) or `log(pp)` on `log(λ)` (price of production on labor value) — these have fundamentally different expected R².

### Expected Outcome
Either: (a) 1958 reproduces R² ≈ 0.98 and the NAICS-era divergence is documented as a real empirical finding, or (b) a specification error is identified and fixed.

### Effort: 2–3 hours (dedicated session)

---

## Investigation 2: T609 — NI Denominator Identity

### Problem
T609 (NSW/NI) is loaded from a pre-computed column in `Table6_3_Extended.csv`. The denominator "NI" (National Income) is never identified as an independent series. No validator checks whether T609 = T607 / (some NI series). The concept could be:
- NIPA National Income (Table 1.7.5)
- Personal Income (Table 2.1)
- NDP (Net Domestic Product)
- Employee compensation only

### Investigation Steps

1. **Read book Ch6 Table N.2**: KB chunk 37 should define NSW/NI precisely. What does Shaikh & Tonak mean by "NI" in this context?
2. **Reverse-engineer from data**: T609 = T607 / X. We have T607 and T609 for 1952-1989. Compute X = T607/T609 for each year and compare against known NIPA aggregates (GDP, NI, PI, EC) to identify which one matches.
3. **Check source CSV metadata**: `Table6_3_Extended.csv` may have a header row identifying the denominator.
4. **Create the NI series**: Once identified, load the denominator independently and verify T609 = T607/NI. Add V05 identity check.

### Expected Outcome
NI denominator identified, T609 verdict upgraded from UNKNOWN to MATCH or JUSTIFIED_DEVIATION.

### Effort: 30 minutes

---

## Investigation 3: N1201 — ST 2002 GDP Source Substitution

### Problem
N1201 (NSW/GDP from Shaikh & Tonak 2002) uses BEA GDP-by-Industry gross output as a fallback GDP denominator via P19. The paper uses NIPA GDP (Table 1.1.5). This is a silent source substitution — gross output ≠ GDP (gross output includes intermediate inputs, GDP does not).

### Investigation Steps

1. **Read P19**: Confirm the fallback logic. Is NIPA GDP available and just not used? Or is there a code path that tries NIPA first?
2. **Check data availability**: L17 loads NIPA T1.1.5 (GDP). Is this data accessible to P19? If so, the fix is trivial: use L17's GDP instead of the GDP-by-Industry fallback.
3. **Verify magnitude**: Gross output is ~2× GDP. N1201 = NSW/GO would be ~half of what N1201 = NSW/GDP should be.
4. **Fix**: Route P19's N1201 denominator to the NIPA T1.1.5 GDP series (already loaded by L17 for the Moos replication).

### Expected Outcome
Trivial fix (point P19 to correct GDP source). N1201 upgraded to MATCH.

### Effort: 15 minutes

---

## Investigation 4: Table5_7_Extended.csv Replacement Strategy

### Problem
`Table5_7_Extended.csv` is a hand-constructed file (Feb 2026, Session 5) that serves as the source for T506, T511, T512 extension values. It contains piecewise-linear interpolation, not real BLS data. T506 and T512 are now recomputed from components (P04, M01), but T511 still reads from this file. The file's column headers falsely claim "BLS CES" provenance.

### Investigation Steps

1. **Audit current dependency**: After the P02/P04 fixes, does any series still depend on Table5_7_Extended.csv? Check which L03 outputs are actually consumed downstream.
2. **T511 specifically**: M01 adjusts T512 using BLS ec_u/ec_p data. Does it also adjust T511? If M01 produces a corrected T511, the Table5_7_Extended.csv dependency may already be dead code.
3. **If T511 still depends on it**: Can T511 be derived from T515/T516? T511 = Lp/L = T515/(T515+T516). Both T515 and T516 are extended via BLS CES with scale factors (P06). This would be Principle 3 compliant.
4. **Deprecate the file**: If no series depends on it after M01 adjustments, remove it from the pipeline and document in DECISION_LOG.

### Expected Outcome
Either Table5_7_Extended.csv is deprecated (no remaining consumers) or T511 is recomputed from T515/(T515+T516).

### Effort: 1 hour

---

## Investigation 5: T516 total_scale = 1.307 Scope Mismatch

### Problem
P06 computes `total_scale = (lp_book[1989] + lu_book[1989]) / bls_total[1989]`. The book's total employment (Lp+Lu = 117,819) is 31% larger than BLS total private employment (90,120). This is definitionally impossible unless the book includes government workers or uses a different employment universe.

### Investigation Steps

1. **Read book's employment definitions**: What universe does the book use? Total nonfarm? Total civilian? Including government?
2. **Check BLS series**: CES0500000001 is "All employees, total private." If the book includes government, the correct BLS series is CES0000000001 ("All employees, total nonfarm" which includes government).
3. **Test alternative**: Compute total_scale with CES0000000001 (total nonfarm, ~109M in 1989). Does it produce a scale closer to 1.0?
4. **Impact assessment**: If total_scale drops from 1.307 to ~1.08, T516 extension values change by ~20%. How does this affect downstream (T511 if derived from T515/T516)?

### Expected Outcome
Correct BLS series identified; P06 updated if needed. Likely fixes the scope mismatch.

### Effort: 30 minutes

---

## Investigation 6: Moos Structural Shift Calibration (N1305)

### Problem
A03 reports the post-2000 structural shift as +0.054 (our data) vs Moos's +0.030. This is an 80% overstatement. While DEC-013 attributes the 0.002 mean gap to NIPA vintage, the shift magnitude difference (0.054 vs 0.030) is much larger and may indicate a formula or data issue in the post-2000 period.

### Investigation Steps

1. **Decompose the shift**: Compute pre-2000 mean and post-2000 mean separately. Which period diverges more from Moos?
2. **Check NIPA revision impact**: The 2018 and 2023 comprehensive NIPA revisions significantly affected social benefit series. Was the post-2000 period more affected than pre-2000?
3. **Compare with Moos's actual data**: If Moos's Working Paper has a table of annual NSW/GDP values, compare year-by-year in the overlap (1959-2014).
4. **E2 sensitivity**: DEC-013 excluded E2 (govt consumption). Test: what shift does including E2 at α=0.5 produce? If closer to 0.030, the E2 exclusion may be wrong for the shift calculation.

### Expected Outcome
Either NIPA vintage fully explains the shift gap, or an E2 allocation fraction is identified that better calibrates to Moos.

### Effort: 1 hour

---

## Priority Order

| # | Investigation | Effort | Impact |
|---|--------------|--------|--------|
| 3 | N1201 GDP source | 15 min | Fixes 1 UNJUSTIFIED verdict |
| 2 | T609 NI denominator | 30 min | Resolves 1 UNKNOWN verdict |
| 5 | T516 scale mismatch | 30 min | Improves T515/T516 faithfulness |
| 4 | Table5_7_Extended.csv | 1 hr | May deprecate problematic artifact |
| 6 | Moos shift calibration | 1 hr | Improves N1305 accuracy |
| 1 | T702/T703 labor values | 2-3 hr | Most complex; may require theoretical insight |

**Total estimated effort**: 5-6 hours across 2-3 sessions.

---

*Plan authored 2026-05-07 following methodology review fix implementation.*
