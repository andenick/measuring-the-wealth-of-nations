# ST2 Comprehensive Methodology Review Plan

**Date**: 2026-05-06
**Scope**: Every series, every extension, every formula — verify code matches the book exactly
**Standard**: Anu Suite v6.0 (Extension Faithfulness Principles 1-11, No-Proxy-Without-Justification, No-Lazy-Splices)

---

## Review Architecture

For each series: read the HDARP book chapter, read the P## script, compare formula-by-formula. Flag every deviation as MATCH / JUSTIFIED_DEVIATION / UNJUSTIFIED_DEVIATION / UNKNOWN.

**5 Opus agents per round, organized by dependency chain.**

---

## Round 1: Core Accounting Identity Chain (T501-T506)

The foundation: TP* = C* + V* + S*, and e = S*/V*. If any of these are wrong, everything downstream is wrong.

### Agent 1: T501-T503 Revenue Accounts
**Book methodology** (Ch5, App E Table E.2, pp.121-130 = chunks 13-14):
- T501 (TP*) = gross output of productive + trading sectors
- T502 (C*_m) = materials consumed by productive + trading sectors  
- T503 (GFP) = TP* - C*_m (Gross Final Product = value added in productive economy)

**Code to verify** (P01):
- Extension uses BEA GDPbyIndustry growth rates spliced at 1961. **CHECK**: Does BEA "gross output" map to ST's TP* definition? ST includes trading sectors; BEA may not.
- T501 has a secondary IO-based override at 1997. **CHECK**: Is the IO-based TV* consistent with the TP* definition?
- **CRITICAL**: The book's TP* includes trading sector gross output. If the BEA extension only uses productive sector gross output (excluding wholesale/retail), the extension systematically understates TP*.

**KB chunks to read**: chunk_13 (Ch5 methodology), chunk_14 (IO integration), chunk_26 (App A), chunk_32 (App F)

### Agent 2: T504-T505 Capital Categories
**Book methodology** (Table E.2, pp.131-140 = chunks 14-15):
- T504 (V*) = wages of productive workers = w_p × L_p (or ec_p × L_p in some formulations)
- T505 (S*) = GFP - V* = TP* - C*_m - V*

**Code to verify** (P02, P03):
- P02 extends V* as: `V* = W × (V*/W)` where W = BEA total compensation. **CHECK**: The book computes V* = productive worker wages directly, not as a ratio applied to total wages. Is this extension method faithful? The ratio V*/W (T512) is itself an approximation that assumes stable productive/unproductive composition.
- P03 extends S* as: `S* = GFP - V*`. **CHECK**: This is correct if GFP and V* extensions are correct. But if V* extension uses total-W × ratio, compounding errors propagate.
- **DEC-009 flag**: T504 splice CR = 0.81 (below the 0.95 target). Root cause: unit scaling mismatch between book V* (billions from Table E.2) and extension V* (derived from BEA compensation in millions). Has this been resolved?

**KB chunks to read**: chunk_15 (V* definitions), chunk_30 (App D wages), chunk_31 (App E capital stock)

### Agent 3: T506 Rate of Exploitation
**Book methodology** (Table 5.7, pp.141-150 = chunks 16-17):
- e = S*/V* — simple ratio of two previously computed series

**Code to verify** (P04):
- P04 is a passthrough — loads pre-computed extended values from L03. **CHECK**: Where does L03 compute the extended e? If it's `S*_ext / V*_ext`, this is correct. If it's spliced independently from the book ratio, that violates Principle 3 (No Lazy Splices on Derived Quantities).
- **Anu Standard**: For a ratio series, extend BOTH numerator and denominator separately, then recompute the ratio. If L03/P04 splice the ratio directly, this is a violation.
- Mohun benchmark validation: e values at [1948, 1958, 1967, 1977, 1989] should match Table 5.7.

**KB chunks to read**: chunk_16 (Table 5.7), chunk_17 (exploitation trends)

### Agent 4: T507, T510 Composition Ratios
**Book methodology**:
- T507 = S*/(S*+V*) — surplus share of value added
- T510 = C*/V* — value composition of capital (flow measure)

**Code to verify** (P07):
- T507 extension: `s / (s + v)` using T505 and T504. **MATCH** if T505 and T504 are correctly extended.
- T510 extension: **LINEAR TREND EXTRAPOLATION** from book data. **CHECK**: This is NOT faithful to the book. The book computes C*/V* from annual data. A linear trend is a statistical approximation, not a replication of the methodology. This should be flagged as a JUSTIFIED_DEVIATION or replaced with proper component extension.
- **Anu Principle 3**: T510 is a derived ratio — should extend C* and V* separately, then compute C*/V*.

**KB chunks to read**: chunk_15 (C* definition), chunk_31 (App E)

### Agent 5: T508-T509, T511-T516 Derived Series
**Book methodology**:
- T508 (CON*) = workers' consumption
- T509 (IG*) = productive investment
- T511 (Lp/L) = productive labor share
- T512 (V*/W) = productive wage share
- T513 (r*) = S*/(C*+V*) Marxian profit rate
- T514 (r*_adj) = capacity-adjusted profit rate
- T515 (Lp) = productive workers (thousands)
- T516 (Lu) = unproductive workers

**Code to verify**:
- T511/T512: Passthrough from pre-extended table. **CHECK**: What methodology was used to extend these ratios? If growth-rate splice on the ratio itself → violation of Principle 3.
- T513/T514: Passthrough from pre-extended table. **CHECK**: DEC-002 documents that total K is used instead of K*. How does the pre-extended table compute r*? Is it S*/K (wrong) or S*/(C*+V*) (book formula)?
- T515/T516: BLS CES extension with scale factor at 1989. **CHECK**: Does the book define Lp differently from BLS production workers? ST uses IO-based classification; BLS uses a different definition. DEC-005 documents this proxy (faithfulness 78%).

**KB chunks to read**: chunk_36 (App J productivity), chunk_33 (App G profit rates), chunk_34 (App I exploitation)

---

## Round 2: Net Social Wage Chain (T601-T609)

### Agent 1: T601-T604 Tax Components
**Book methodology** (Ch6, Table 6.3, pp.152-161 = chunks 18-19):
- T601 = personal income taxes paid by workers = total personal taxes × (W_p / PI)
- T602 = social insurance contributions = worker portion of payroll taxes
- T603 = indirect taxes borne by workers = consumption-proportional allocation
- T604 = T601 + T602 + T603 (total taxes on workers)

**Code to verify** (P09):
- P09 is passthrough (book data only, no extension). **CHECK**: Are the book values loaded correctly from the chopped CSVs? Unit verification (billions vs millions).

### Agent 2: T605-T606 Benefit Components
**Book methodology**:
- T605 = direct social benefits received by workers (social security, Medicare, unemployment)
- T606 = government consumption allocated to workers (education, health, transport) × worker share

**Code to verify** (P10):
- Extension via BEA NIPA 2.1/3.1. **CHECK**: Does L08 fetch the correct NIPA line items? The book's definition of "worker benefits" is specific — it's not all government transfers.
- **DEC-006**: 1996 welfare reform creates structural break. Is the continuity check (±15% at 1996) appropriate?

### Agent 3: T607-T609 NSW Aggregates
**Book methodology** (Table N.1-N.2, pp.342-351 = chunk 37):
- T607 (NSW) = T605 + T606 - T601 - T602 - T603 = Benefits - Taxes
- T608 = NSW / V*
- T609 = NSW / NI (national income)

**Code to verify** (P11):
- T607: Passthrough from parsed CSV. **CHECK**: Is the parsed CSV the correct Table N.1 data?
- T608 = T607 / T504. **CHECK**: Units must match (both in billions). Division by V* from P02.
- T609: Passthrough. **CHECK**: What is NI? Personal income? National income? The denominator matters.

### Agent 4: Moos Replication (N1301-N1305)
**Moos (2017) methodology** (Working Paper 2017-18, KB at `2017_Moos_NSW_21st_Century/`):
- NSW = E1 - (T1 + T2×LS) where E1 = direct social benefits, T1 = social insurance, T2 = personal taxes, LS = EC/PI

**Code to verify** (P21):
- **DEC-013**: E2 (govt consumption) excluded. **VERIFY**: Read the Moos paper transcript — does Moos explicitly exclude E2? Or does he include it at some fraction?
- LS = employee_compensation / personal_income from NIPA T2.1. **CHECK**: Does Moos use EC/PI or a different labor share measure?
- T1 from NIPA T3.7 (social insurance contributions). **CHECK**: Which line — total (line 1) or federal only?
- **CALIBRATION**: mean 0.013 vs Moos 0.011. The residual 0.002 gap — is it NIPA vintage or methodology?

### Agent 5: Turkey + NZ International (N1601-N1704)
**Karabacak & Tonak (2022) methodology** (KB at `2022_Karabacak_Tonak_NSW_Turkey/`):
- N1601: labor share = compensation of employees / GDP (from TurkStat national accounts)
- N1602: NSW/GDP using same ST formula adapted to Turkish fiscal data

**Code to verify** (P18):
- **DEC-014**: TurkStat Table 20.37 now used for labor share. **VERIFY**: Is the formula `NSW = (B - T) / GDP` faithful to the paper?
- World Bank fallback: `benefit_pct = exp_pct × 0.35`. **FLAG**: Where does 0.35 come from? Is it from the paper or an assumption?

**Cronin (2001)** (KB at `2001_Cronin_New_Zealand/`):
- N1701-N1704: Direct from paper Tables 1-2, no computation

**Code to verify** (P20 Cronin section):
- Passthrough `/100` for percentage → fraction conversion. **CHECK**: Are the column names in the CSV correct? Does s/TV in the CSV map to the correct table column?

---

## Round 3: Mohun Comparison + IO Framework (N1401-N1504, T401-T402, T701-T703)

### Agent 1: Mohun (2005) Classification Comparison
**Mohun (2005) methodology** (Cambridge Journal of Economics):
- Different productive/unproductive boundary — Mohun includes "supervision" as unproductive
- N1401 = Mohun's exploitation rate, N1402 = Mohun's productive labor share

**Code to verify** (P16):
- N1404 = T506 / N1401. **CHECK**: Is this the right direction? If ST e > Mohun e, ratio > 1 (= 1.61). But if the registry stores Mohun's rate as N1401, then T506/N1401 = ST/Mohun which should be > 1. Verify the sign convention.

### Agent 2: Mohun (2013) Class Decomposition
**Mohun (2013) methodology** (Review of Radical Political Economics):
- N1501 = WC unproductive workers, N1502 = managerial unproductive

**Code to verify** (P20):
- `luw = lu * 0.813`, `lum = lu * 0.187`. **CRITICAL CHECK**: Where do 0.813 and 0.187 come from? Is this from Mohun's paper directly (a specific table or calculation)? Or is it an ST2 assumption? If from the paper, which year? The fraction may vary over time — using a constant is a strong assumption.
- The Anu Standard requires: "No Proxies Without Justification." If the 81.3/18.7 split is a single-year snapshot applied to all 42 years, this must be documented as a JUSTIFIED_DEVIATION with the source year cited.

### Agent 3: IO Matrices (T401-T402)
**Book methodology** (Ch4, App F, pp.311-320 = chunk 32):
- A-matrix: a_ij = z_ij / x_j (direct requirements from BEA IO benchmark tables)
- B-matrix: (I-A)^{-1} (Leontief inverse)

**Code to verify** (P13):
- The productive/unproductive classification of 85 sectors. **CHECK**: Does `io_85_to_nipa_13_concordance.csv` correctly map all 85 SIC sectors? Cross-reference against Appendix B (chunk 27, Table B.1).
- Condition number check: `cond > 1e6` threshold. **CHECK**: Is this appropriate? Some benchmark years may have near-singular (I-A) matrices.

### Agent 4: Labor Values (T701-T702)
**Book methodology** (Section 4.1, pp.91-100 = chunk 10):
- λ = l(I-A)^{-1} — row vector of direct labor × Leontief inverse
- pp_j = (1+r̄)(c_j + v_j) — prices of production

**Code to verify** (P14):
- `lv = hp_series @ B_matrix`. **CHECK**: Is `hp_series` the correct labor coefficient vector? It should be direct labor hours per unit output by sector, not total employment.
- `v_va_ratio = 1.0 - T507` applied uniformly. **CRITICAL**: The book computes sector-specific V_j/VA_j ratios. Using a single economy-wide ratio is a major simplification. This is the root cause of the R² issue (DEC-011). Document as JUSTIFIED_DEVIATION (Wave 2 will fix).
- `r_bar = total_s_prod / (total_c_prod + total_v_prod)`. **CHECK**: Is this the correct uniform profit rate formula? The book uses r̄ = S*/(C*+V*) for productive sectors only.

### Agent 5: Tonak (1984) Fiscal Analysis (N1001-N1002)
**Tonak (1984) methodology** (PhD dissertation, Chapter IV):
- N1001 = labor taxes / total taxes (from Table V)
- N1002 = net tax / taxes paid by labor (from Table X)

**Code to verify** (P20 Tonak section):
- `labor_share = tax_df["labor_taxes"] / tax_df["total_taxes"]`. **CHECK**: Does the column "labor_taxes" in the Tonak HDARP CSV correspond to Tonak's Table V? Read the KB chunk to verify column mapping.
- **DEC-012 compliance**: Confirmed clean (Round 4 verification passed), but verify the CSV files contain 29 years of annual data, not summary statistics.

---

## Round 4: Extension Faithfulness Deep Audit

For every extended series, apply the 10-Step Extension Faithfulness test from anu-extension v3.3.

### Agent 1: BEA-Extended T-Series (T501-T505, T508-T509)
For each: verify Source Match (Principle 3), Transformation Replication (Principle 6), Transition Analysis (Principle 8).

**Specific checks**:
- T501 splice at 1961: Connection Ratio? Growth Rate Difference? Correlation in overlap?
- T504 splice at 1989: CR = 0.81 documented. Is `W × (V*/W)` the same formula the book used? The book computed V* directly from IO-sector-level wage data, not as a ratio of total wages.
- T505: Derived as `GFP - V*`. If both components are properly extended, this is correct. But if T504 has CR=0.81, the error propagates to T505.

### Agent 2: BLS-Extended Series (T511-T516)
**Specific checks**:
- T511 (Lp/L): Is the ratio extended directly (Principle 3 violation) or are Lp and L extended separately?
- T515/T516 BLS scale factor: `scale = lp_book[1989] / bls_prod[1989]`. Is the 1989 anchor year appropriate? What's the scale factor magnitude? If far from 1.0, the BLS series doesn't match the book's definition.
- DEC-005 faithfulness: 78% for T511, 76% for T512. What drives the gap?

### Agent 3: Pre-Extended Ratio Series (T506, T513-T514)
These load from `ProfitRates_Extended.csv` and `Table5_7_Extended.csv`. 

**CRITICAL**: Who created these extended tables? Were they hand-constructed in a prior session, or are they outputs of the NickyData pipeline? If hand-constructed, the extension methodology is undocumented and potentially unfaithful.

**Specific checks**:
- T506: Is the extended exploitation rate computed as `S*_ext / V*_ext` or spliced directly? Read the source CSV to determine.
- T513: Is the extended profit rate computed as `S*_ext / (C*_ext + V*_ext)` or spliced? DEC-002 says total K is used instead of C*+V*. But what does the pre-extended table actually compute?

### Agent 4: NSW Extension (T605-T607)
**Specific checks**:
- T605/T606 extension via NIPA 2.1/3.1: Does the NIPA line item match the book's definition of worker benefits? The book uses a specific allocation formula (pp.152-161).
- T607 (NSW): Is it extended as `T605_ext + T606_ext - T604_ext`, or is the ratio extended directly?
- What happens at the 1996 welfare reform break? Is there a discontinuity adjustment?

### Agent 5: T510 Linear Trend (Flagged Issue)
**Deep dive into the T510 (C*/V*) linear trend extension.**

This is the most problematic extension:
- The book computes C*/V* from annual IO data.
- The extension uses `np.polyfit(book_years, book_vals, 1)` — a linear OLS trend.
- This assumes C*/V* grows linearly, which is an untested assumption.
- **Anu Principle 3** says: for derived quantities, extend components separately and recompute.
- The correct approach: extend C* (possibly from BEA Fixed Assets) and V* (from T504), then compute C*/V*.
- **Flag**: Is C* even available as a separate series in the pipeline? If not, can it be derived from T501 - T503 - T505 (C* = TP* - GFP - S*... no, C* = TP* - GFP = C*_m)? Actually C*_m = T502. So C*/V* = T502/T504. Verify whether this is feasible.

---

## Round 5: Cross-Series Consistency + Final Verdicts

### Agent 1: Accounting Identity Verification
Verify these identities hold in the output data for every year:
- TP* = C*_m + GFP (T501 = T502 + T503)
- GFP = V* + S* (T503 = T504 + T505)
- e = S*/V* (T506 = T505/T504)
- NSW = Benefits - Taxes (T607 = T605 + T606 - T601 - T602 - T603)

Run these as numerical checks on the actual CSV output files. Report maximum deviation.

### Agent 2: Extension Overlap Validation
For every extended series with an overlap period (book data exists alongside extension data):
- Compute correlation in the overlap
- Compute mean absolute percentage error in the overlap
- Report which series have MAPE > 5% (problematic)

### Agent 3: Unit Consistency Audit
For every formula in every P## script:
- Verify both sides of every equation have matching units
- Flag any `/1e3`, `/1e6`, `/1e9` conversions — are they documented?
- Flag any raw dollar amounts being divided by percentage values (unit mismatch)

### Agent 4: Compile Final Verdicts
For each of the 59 series, produce a one-line verdict:
- FAITHFUL: Code exactly matches book methodology
- JUSTIFIED_DEVIATION: Code differs but deviation is documented (DEC-### reference)
- UNJUSTIFIED_DEVIATION: Code differs without documentation — needs fix
- UNKNOWN: Cannot verify (KB content insufficient)

### Agent 5: Write Methodology Review Report
Compile all findings into `Technical/docs/ST2_METHODOLOGY_REVIEW_REPORT.md`:
1. Executive summary (how many FAITHFUL / JUSTIFIED / UNJUSTIFIED / UNKNOWN)
2. Per-series verdicts table
3. Critical findings requiring immediate action
4. Extension faithfulness scores (Anu v3.3 10-step)
5. Recommendations for Wave 2

---

## Execution Summary

| Round | Focus | Agents | Key Question |
|-------|-------|--------|-------------|
| 1 | Core chain T501-T516 | 5 Opus | Does TP*=C*+V*+S* hold in the extensions? |
| 2 | NSW chain T601-T609 + Moos/Turkey/NZ | 5 Opus | Does NSW=Benefits-Taxes match the book formula? |
| 3 | Mohun + IO + Labor Values | 5 Opus | Are classification boundaries correct? Is 0.813/0.187 justified? |
| 4 | Extension faithfulness deep audit | 5 Opus | Are ratios extended as ratios (violation) or recomputed from components? |
| 5 | Cross-series consistency + verdicts | 5 Opus | Do accounting identities hold across the full 1948-2024 range? |

**Total: 25 Opus agents across 5 sequential rounds**

---

## Known Issues to Resolve (Pre-Flagged)

| # | Issue | Series | Severity | Expected Verdict |
|---|-------|--------|----------|-----------------|
| 1 | T510 linear trend extension | T510 | HIGH | UNJUSTIFIED_DEVIATION — should use C*/V* from components |
| 2 | T504 splice CR=0.81 | T504 | MEDIUM | JUSTIFIED_DEVIATION (DEC-009) but needs Wave 2 fix |
| 3 | Scalar V*/VA* in P14 | T701-T703 | HIGH | JUSTIFIED_DEVIATION (DEC-011) — Wave 2 |
| 4 | Mohun 0.813/0.187 constant split | N1501-N1504 | MEDIUM | Needs source verification |
| 5 | Pre-extended ratio tables (T506, T513) | T506, T513-T514 | HIGH | UNKNOWN until source CSV provenance verified |
| 6 | T511/T512 ratio splice method | T511-T512 | MEDIUM | Possible Principle 3 violation |
| 7 | World Bank 0.35 benefit fraction | N1602 | LOW | Needs paper citation |
| 8 | Moos E2 exclusion justification | N1301-N1305 | LOW | JUSTIFIED_DEVIATION (DEC-013) but needs paper quote |
