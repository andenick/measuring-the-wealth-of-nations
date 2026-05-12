# ST2 Series Review, Analysis & Next Steps Plan

**Date**: 2026-05-07
**Author**: Claude Opus 4.6 (Session 21)
**Scope**: All 59 series — chapter-by-chapter deep review, Knowledge Base cross-reference, and prioritized next steps
**Inputs**: series_registry.json, DECISION_LOG (16 entries), ASSUMPTIONS.md (7 assumptions), ST2_METHODOLOGY_REVIEW_REPORT (25-agent, 5 rounds), ST2_WAVE2_DEVELOPMENT_PLAN, ST2_REMAINING_INVESTIGATIONS_PLAN, HDARP 40-chunk Knowledge Base (399 pages), KB SUMMARY_KEY_FINDINGS, PHASE0_GAP_AND_BLOCKER_REGISTER, CHECKLIST.md, HANDOFF_20260507_SESSION20

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Knowledge Base Inventory & Exploitation Audit](#2-knowledge-base-inventory--exploitation-audit)
3. [Chapter 5 Series Review (T501–T516)](#3-chapter-5-series-review-t501t516)
4. [Chapter 6 Series Review (T601–T609)](#4-chapter-6-series-review-t601t609)
5. [Chapter 4 Series Review (T401–T402)](#5-chapter-4-series-review-t401t402)
6. [Chapter 7 Series Review (T701–T703)](#6-chapter-7-series-review-t701t703)
7. [Chapters 2, 8, 9 Series Review (T201, T801, T901)](#7-chapters-2-8-9-series-review-t201-t801-t901)
8. [External Studies Review (N-series)](#8-external-studies-review-n-series)
9. [Cross-Cutting Structural Issues](#9-cross-cutting-structural-issues)
10. [Knowledge Base Lessons — What the Book Actually Says](#10-knowledge-base-lessons--what-the-book-actually-says)
11. [Prioritized Next Steps](#11-prioritized-next-steps)
12. [Dependency Graph](#12-dependency-graph)
13. [Effort & Session Estimates](#13-effort--session-estimates)

---

## 1. Executive Summary

### The Pipeline Today

| Metric | Value |
|--------|-------|
| Total series | 59 (33 T-series + 26 N-series) |
| Scripts | 70+ across 8 phases (S/L/P/V/M/A/O/E) |
| Validators | 15 (348 checks, 0 FAIL) |
| Runtime | ~13 seconds |
| Extension range | 1948–2024 (77 years) for core series |
| Methodology verdicts | 28 MATCH / 25 JUSTIFIED / 4 UNJUSTIFIED / 2 UNKNOWN |
| Completion rating | 97% (Druck formula) |

### What's Working

The pipeline replicates the core accounting framework (Ch 5), the net social wage analysis (Ch 6), and 8 external studies with zero validation failures. The exploitation rate rises from 1.70 (1948) to ~3.59 (2024). The NSW is negative for 92% of years. Growth-rate splicing produces smooth transitions at the 1989/1990 boundary. The 25-agent methodology review found and fixed 14 code errors.

### What's Not Working

Four series remain UNJUSTIFIED: T511 (Lp/L), T512 (V*/W), T513 (r*), T514 (r*_adj) — all blocked on the IO framework. Two are UNKNOWN: T201 and T801 (Wave 3 deferred). The T702/T703 labor-value regression produces R² = 0.003–0.035 for NAICS-era data vs the book's 0.98 for 1958. The Table5_7_Extended.csv file is a fabricated artifact still consumed by the pipeline. Unit mismatches between Table E.2 (billions) and Table 5.7 (millions÷1000) persist in the data layer though M01/M99 adjustments compensate at runtime.

### What the Knowledge Base Can Still Teach Us

The HDARP extraction of the full 399-page book (40 chunks, old Shaikh Tonak project) has been only partially mined. Key untapped resources:

- **Appendix N** (chunks 35–37): The exact estimation procedures for every empirical table — formulas, data sources, BEA table numbers, allocation rules. This is the Rosetta Stone for resolving DEC-003 (VA*/W), DEC-008 (tax allocation), and the T609 NI denominator.
- **Appendix E tables** (chunks 31–34): Tables E.1–E.3 contain the annual data behind T501–T516 and T515–T516. Cross-checking these against our CSVs would catch transcription errors.
- **Chapter 4 IO methodology** (chunks 10–11): The exact sector classification rules, the productive/unproductive boundary definition, and the interpolation method between benchmark years — everything Wave 2 needs.
- **Chapter 7 regression specification** (chunks 22–24): Whether the book regresses log(market prices) on log(labor values) or log(prices of production) on log(labor values) — the answer determines whether our R² = 0.003 is a bug or a genuine empirical finding for the NAICS era.
- **Chapter 6 Table N.2** (chunk 37): The exact definition of "NI" in the NSW/NI ratio (T609).

---

## 2. Knowledge Base Inventory & Exploitation Audit

### Two Knowledge Bases

The project has two KBs, reflecting its evolution from the old Shaikh Tonak project to AS2/ST2:

#### KB-1: Old HDARP (Shaikh Tonak project)
- **Location**: `../Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/`
- **Coverage**: 40 chunks × ~10 pages = 399 pages (complete book)
- **Content types per chunk**: full_transcription.md + tables/ + equations/ + figures/
- **Quality**: Full HDARP v1.0 extraction with per-chunk tables (CSV), equations (LaTeX/MD), figure descriptions (MD)
- **Status**: RICH but UNDEREXPLOITED — the pipeline references it for DEC-008 verification and a few table cross-checks, but most chunks have never been systematically mined for formula verification

#### KB-2: ST2 In-Project KB
- **Location**: `./Technical/Knowledge_Base/`
- **Coverage**: Sparse — SUMMARY_KEY_FINDINGS.md (20 sampled pages), page-level text files (mostly pp 301–399), 1 equation file, some table/figure files
- **Quality**: Mix of real HDARP and ZHDARP v3.3 "placeholder extraction" (pages 201–300 are placeholders, not real OCR)
- **Status**: INCOMPLETE — the page 201–300 extraction is explicitly labeled as placeholder; equation extraction covers only 1 page

### Chunk-to-Chapter Mapping (KB-1)

| Chunks | Pages | Book Content | Pipeline Series | Exploitation Status |
|--------|-------|-------------|-----------------|-------------------|
| 01–03 | 1–30 | Front matter, Preface, Ch 1 (Introduction) | None | Low priority |
| 04–05 | 31–50 | Ch 2 (National Accounting) | T201 | **UNMINED** — T201 is Wave 3 deferred; Ch 2 tables define the GFP/GDP relationship |
| 06–09 | 51–90 | Ch 3 (Sectoral Structure, IO-Marxian Mapping) | T401/T402 foundations | **PARTIALLY MINED** — chunk_06 tables extracted (Table 3.1), chunk_07 has 6 tables + 6 figures, chunk_08–09 have additional tables. These define the productive/unproductive sector boundary used in ALL Ch 5 calculations |
| 10–11 | 91–110 | Ch 4 (IO Framework, Labor Value Theory) | T401, T402, T701–T703 | **CRITICALLY UNDERMINED** — chunk_10 has equations/figures for labor value calculations, chunk_11 has tables 4.1–4.4 + equations. This is the theoretical core for Wave 2 |
| 12–17 | 111–170 | Ch 5 (Accounting Framework — all empirical tables) | T501–T516 | **PARTIALLY MINED** — chunk_12–13 have Tables 5.4/5.5 (exploitation accounting), chunks 14–15 have Tables 5.6–5.9 (wages, surplus, profit rates), chunks 16–17 have Tables 5.10–5.14 (composition, deviations). DPRs reference some but not all |
| 18–21 | 171–210 | Ch 6 (Net Social Wage) + Ch 6 International | T601–T609 | **PARTIALLY MINED** — chunk_18 has Tables 6.1–6.3 + Figures 6.1–6.3, chunks 19–21 have Tables 6.4–6.8 (international comparisons). DEC-008 verified from chunk_09 |
| 22–24 | 211–240 | Ch 7 (Labor Values and Prices of Production) | T701–T703 | **CRITICALLY UNDERMINED** — The regression specification (what variables are regressed on what) is here but hasn't been carefully extracted for T702/T703 debugging |
| 25–27 | 241–270 | Ch 8 (Cross-Country Comparisons) | T801 | **UNMINED** — Wave 3 deferred |
| 28–30 | 271–300 | Ch 9 (Summary and Conclusions) | T901 | **UNMINED** — mostly narrative, but contains the summary table definitions |
| 31–34 | 301–340 | Appendix E (Data Tables E.1–E.3) | T501–T516, T515–T516 | **PARTIALLY MINED** — some table extractions exist but systematic cross-check against pipeline CSVs not done |
| 35–37 | 341–370 | Appendix N (Sources and Methods) | ALL series | **THE ROSETTA STONE — BARELY TOUCHED** — contains exact BEA table numbers, allocation formulas, estimation procedures for every empirical series |
| 38–40 | 371–399 | Bibliography, Index | Reference only | Low priority |

### Exploitation Gap Analysis

**High-value unmined content** (ranked by impact on open issues):

1. **Appendix N (chunks 35–37)**: Resolves DEC-003 (ec_u/ec_p), DEC-009 (T504 splice), Investigation 2 (T609 NI), Investigation 5 (T516 employment universe). Every formula and data source in the book is documented here.
2. **Ch 4 methodology (chunks 10–11)**: Resolves ALL Wave 2 blockers — sector classification rules, IO interpolation methodology, labor value computation spec.
3. **Ch 7 regression spec (chunks 22–24)**: Resolves Investigation 1 (T702/T703 R² = 0.003). Determines whether this is a bug or a real finding.
4. **Ch 5 Tables 5.5–5.14 (chunks 12–17)**: Cross-check pipeline reference values; extract any annual data not yet in CSVs.
5. **Ch 6 Table N.2 (chunk 37)**: Resolves Investigation 2 (T609 denominator identity).
6. **Appendix E tables (chunks 31–34)**: Systematic cross-check of T501–T516 book-period data against our source CSVs.

---

## 3. Chapter 5 Series Review (T501–T516)

Chapter 5 is the heart of the project: 16 series covering the complete Marxian accounting framework from Total Product down to profit rates. It represents 16/33 T-series (48% of book series) and drives the entire exploitation chain.

### 3.1 The Revenue Chain (T501–T503)

#### T501: Total Product (TP*)
- **Registry**: Book Table E.2, 1948–2024, billions USD
- **Construction**: Book data (1948–1989) + BEA GDP-by-Industry growth-rate splice (1997–2024)
- **Verdict**: JUSTIFIED_DEVIATION (72% faithfulness)
- **Issue**: Phase 1 uses GDP growth rates as proxy; Phase 2 added IO productive-sector correction for 1997+ via L11b (NAICS benchmark interpolation producing annual productive output ratios 0.55–0.58)
- **KB lesson needed**: Appendix N should document whether TP* = GDP × (productive fraction) or uses a different aggregation. Chunk 31–34 (Appendix E, Table E.2) has the actual annual TP* values for cross-check.
- **Status**: Functionally correct for trend analysis; absolute levels approximate for 1990–1996 gap.

#### T502: Constant Capital (C*_m)
- **Registry**: Book Table E.2, 1948–1989, billions USD
- **Construction**: Book data only (no extension in registry); P01 applies IO C*_m overlay for 1997+ from NAICS Use table benchmarks
- **Verdict**: JUSTIFIED_DEVIATION
- **Issue**: DEC-015 accepts GDP proxy for Wave 1. The correct methodology (pp. 94–96 per Wave 2 plan) requires C*_m[yr] = (M'p/GVAp)[benchmark] × GVAp[yr] with interpolation between IO benchmarks.
- **KB lesson needed**: Chunks 10–11 (Ch 4 IO framework) define M'p exactly. Appendix N should specify which BEA tables the book used for intermediate inputs. Cross-check chunk_06 Table 3.1 (sectoral structure) for the productive/trade/secondary decomposition.
- **Wave 2 fix**: B3 in development plan — IO benchmark interpolation for annual C*_m.

#### T503: Gross Final Product (GFP = TP* − C*_m)
- **Registry**: Derived identity, 1948–1989
- **Construction**: Enforced as T501 − T502 in P01 (identity enforcement added Session 20)
- **Verdict**: MATCH
- **Note**: Identity enforcement means T503 inherits whatever approximations T501 and T502 carry, but it is always internally consistent. The methodology review flagged this as MATCH because the formula itself is correct.

### 3.2 The Exploitation Chain (T504–T506)

This is the most complex and most corrected part of the pipeline. The 25-agent review found critical issues here (T504 unit cascade, T506 lazy splice, T510 log-encoding) that were fixed in Session 20.

#### T504: Variable Capital (V*)
- **Registry**: Book Table 5.5, 1948–2024, billions USD
- **Construction**: Book data + extension via V* = W × (V*/W) where V*/W comes from T512
- **Verdict**: JUSTIFIED_DEVIATION (76% faithfulness)
- **Issues (resolved and open)**:
  - RESOLVED: Growth-rate splice replaced absolute W×T512 product (Session 20, T504 splice fix)
  - RESOLVED: M99 now promotes adjustment years into the series (not just overwrites)
  - OPEN (DEC-003): ec_u/ec_p ratio used for V*/W extension is interpolated 1990–1997 (log-linear between book 1989 value and first NAICS 1998 value). Max deviation from constant assumption: 0.42.
  - OPEN (DEC-009): Splice quality CR = 0.81 — cannot improve without unit normalization
- **KB lesson needed**: Appendix N should document the exact formula for V* = ec_p × L_p (average productive-sector employee compensation × productive employment). The distinction between "compensation" (includes benefits) and "wages" (excludes benefits) matters here. Chunk 14 (Tables 5.6–5.7) should have the annual V* values for cross-check. Also: chunk_09 (pp 63–65) documents the "net royalty" framework for true V* (nominal wage minus net royalty payments — DEC-008 confirmed this).
- **Upstream dependency**: T512 (V*/W ratio) → feeds T504-EXT → feeds T505, T506

#### T505: Surplus Value (S* = GFP − V*)
- **Registry**: Derived, 1948–2024, billions USD
- **Construction**: T503 − T504 for book period; M01 recomputes as e × V* for extension
- **Verdict**: JUSTIFIED_DEVIATION (70% faithfulness)
- **Issues**:
  - Inherits all T503 and T504 approximations
  - M01 adjustment ensures no negative surplus values (the pre-fix state had S* < 0 for 1990–92 due to unit cascade)
  - The extension-period S* is effectively a derived quantity: GFP_ext × (1 − 1/(1+e_ext)) where e_ext comes from the M01-adjusted exploitation rate
- **KB lesson**: Chunks 14–15 should have Tables 5.8–5.9 (surplus value breakdowns). Cross-checking S* = GFP − V* against the book's own Table E.2 would verify our reconstruction.

#### T506: Rate of Exploitation (e = S*/V*)
- **Registry**: Book Table 5.7, 1948–2024, ratio
- **Reference values**: 1948: 1.70, 1958: 1.83, 1967: 2.10, 1977: 2.10, 1989: 2.44
- **Construction**: Book data + P04 recomputes from S*/V* + M01 ec_u/ec_p adjustment (Principle 3 compliant as of Session 20)
- **Verdict**: JUSTIFIED_DEVIATION (72% faithfulness)
- **Issues (resolved)**:
  - RESOLVED: Was a lazy splice from pre-baked CSV with constant VA*/W = 1.238 — now recomputed from components
  - RESOLVED: P04 applies Principle 3 (S*/V* from independently extended S* and V*)
- **KB lesson**: The book's Table 5.7 (chunk 13–14) has annual e values for all benchmark years. More importantly, Appendix N should document whether the book ever adjusts e for the net royalty framework (i.e., whether V* is before or after net royalty deduction). This matters because if V* in Table 5.7 is post-royalty, the exploitation rate is higher than if it's pre-royalty.
- **Key finding**: e = ~3.59 in 2024 — a 111% increase over the book-end 1989 value of 2.44. This is the project's headline result.

### 3.3 The Composition and Employment Block (T507–T512)

#### T507: Surplus Ratio (S*/Y = S*/(S*+V*))
- **Registry**: Book Table 5.7, 1948–1989, ratio
- **Verdict**: MATCH
- **Note**: Recomputed correctly from T505/T504. No extension — book period only.

#### T508: Productive Consumption (CON*) / T509: Productive Investment (IG*)
- **Registry**: Book Table E.2, 1948–1989, billions USD
- **Verdict**: JUSTIFIED_DEVIATION (65% / 60% faithfulness)
- **Issue**: Both use GDP growth-rate splice for extension. These are revenue-side aggregates that should be extended via IO framework decomposition.
- **KB lesson**: Appendix E Table E.2 (chunks 31–34) has the annual values. Appendix N should document the BEA sources for consumption and investment decomposition.

#### T510: Value Composition (C*/V*)
- **Registry**: Book Table 5.7, 1948–1989, ratio
- **Verdict**: JUSTIFIED_DEVIATION (55% faithfulness — lowest of any non-UNJUSTIFIED series)
- **Issues**:
  - RESOLVED: Was stored as ln(V*/C*), not C*/V* — fixed with np.exp(-x) decode
  - OPEN: Extension uses linear trend extrapolation on decoded values. Component recomputation (C*/V* = T502/T504) is blocked by the unit mismatch between T502 (billions) and T504 (millions÷1000).
- **KB lesson**: Chunk 16 has Table 5.10 (composition data). The book's C*/V* is the ratio of constant capital consumed to variable capital — specifically, it's the flow measure (materials consumed ÷ productive wages), NOT the stock measure (capital stock ÷ variable capital). This distinction is critical: our T513 uses the stock measure for the profit rate denominator but the book's C*/V* in Table 5.7 is a flow ratio. Appendix N should confirm.

#### T511: Productive Labor Share (Lp/L) — UNJUSTIFIED
- **Registry**: Book Table 5.7, 1948–2024, share
- **Reference values**: 1948: 0.57, 1967: 0.48, 1989: 0.37
- **Verdict**: UNJUSTIFIED_DEVIATION (78% faithfulness)
- **Root cause**: Extended as a ratio directly from Table5_7_Extended.csv — a fabricated piecewise-linear interpolation with three segments (-0.002/yr, -0.004/yr, -0.002/yr). This is NOT BLS CES data despite column headers claiming otherwise. No generation script exists.
- **Principle 3 violation**: Ratio should be recomputed as Lp_ext / L_ext from separately extended components.
- **KB lesson**: The book defines Lp as employment in "productive" sectors per the IO classification (Chapter 4). Chunk_06 Table 3.1 and chunk_07 Tables 3.2–3.6 define exactly which sectors are productive. Appendix N should document whether the employment numbers come from BLS establishment survey (CES), BLS household survey (CPS), or BEA employment tables. This determines the correct extension source. The KB Summary notes L fell from 58,000 (1948) to >110,000 (1988) and Lp from 33,000 to ~41,000 — cross-check these against T515/T516 book-period data.
- **Wave 2 fix**: B4 — derive Lp from IO classification applied to BLS employment by industry, then compute T511 = Lp/L.
- **Interim fix possibility**: T511 = T515/(T515+T516) would be Principle 3 compliant and use real BLS CES data, not fabricated linear trends. Investigate whether this is viable (Investigation 4 in Remaining Investigations Plan).

#### T512: Productive Wage Share (V*/W) — UNJUSTIFIED
- **Registry**: Book Table 5.7, 1948–2024, share
- **Reference values**: 1948: 0.54, 1967: 0.46, 1989: 0.33
- **Verdict**: UNJUSTIFIED_DEVIATION (76% faithfulness)
- **Root cause**: Same as T511 — from Table5_7_Extended.csv, same piecewise-linear fabrication.
- **Upstream impact**: T512 feeds T504 extension (V* = W × T512) — so this fabrication propagates into the entire exploitation chain.
- **KB lesson**: Appendix N should document V*/W = (ec_p × Lp) / (EC_total) where ec_p is average compensation per productive worker. The M01 adjustment partially corrects this by applying year-varying ec_u/ec_p ratios from BEA NIPA 6.2D (1998+) with log-linear interpolation for 1990–1997.
- **Wave 2 fix**: B4 — extend V* and W independently, then compute V*/W.

### 3.4 The Profit Rate Block (T513–T514) — UNJUSTIFIED

#### T513: Marxian Profit Rate (r* = S*/(C*+V*))
- **Registry**: Book Table 5.11, 1948–2024, rate
- **Verdict**: UNJUSTIFIED_DEVIATION (60% faithfulness)
- **Root cause**: Uses total private capital stock K from BEA Fixed Assets Table 4.1 as denominator, not productive-sector capital K*. Additionally, the book's profit rate formula may use flow C*+V* (materials + wages), not stock K (DEC-002, DEC-010).
- **KB lesson**: THIS IS THE SINGLE MOST IMPORTANT KB MINING TASK. Chunks 15–16 have Tables 5.11–5.14 (profit rate data). But more critically, Appendix N should document:
  1. Whether the denominator is C*+V* (flow) or K* (stock) or both (the book presents both measures)
  2. If K*, which BEA table and which sectors were used
  3. The exact capacity utilization adjustment for T514
  The KB Summary (page 140 data) shows S*/P at 224% and S*/V* at 210% — these are different measures than r*, and their relationship to T513 should be traced.
- **Wave 2 fix**: B5 — apply IO sector classification to BEA Fixed Assets by industry to compute K*.

#### T514: Capacity-Adjusted Profit Rate (r*_adj = r* × (1/TCU))
- **Registry**: Book Table 5.11, 1948–2024, rate
- **Verdict**: UNJUSTIFIED_DEVIATION (60% faithfulness)
- **Root cause**: Inherits T513's denominator problem.
- **KB lesson**: Same as T513 — plus the specific TCU (Total Capacity Utilization) source. FRED's TCU series starts in 1967; the book covers 1948–1989. What source did Shaikh & Tonak use for pre-1967 capacity utilization? Appendix N should tell us.

### 3.5 The Employment Block (T515–T516)

#### T515: Productive Employment (Lp)
- **Registry**: Book Table E.3, 1948–2024, thousands
- **Verdict**: JUSTIFIED_DEVIATION (78% faithfulness)
- **Construction**: Book data + BLS CES production workers scaled at 1989 splice point
- **KB lesson**: Appendix E Table E.3 (chunks 31–34) has the annual Lp values. Cross-check against our CSV. The scale factor at 1989 should be near 1.0 if our BLS series matches the book's employment universe.

#### T516: Unproductive Employment (Lu = L − Lp)
- **Registry**: Derived, 1948–2024, thousands
- **Verdict**: JUSTIFIED_DEVIATION (75% faithfulness)
- **Issue**: total_scale = 1.307 — the book's total employment (Lp+Lu = 117,819 in 1989) is 31% larger than BLS total private (90,120). This means the book includes government workers in L.
- **KB lesson**: Appendix N should confirm the employment universe. Investigation 5 in the Remaining Investigations Plan notes that CES0000000001 (total nonfarm including government, ~109M in 1989) would reduce the scale to ~1.08. The KB Summary's employment data (page 130: L from 58,000 to >110,000) gives us a cross-check point.
- **Quick fix**: Fetch CES0000000001 via BLS API and recompute.

---

## 4. Chapter 6 Series Review (T601–T609)

Chapter 6 covers the Net Social Wage — the analysis of whether workers subsidize the state or vice versa. 9 series, recently extended (Session 20 added T601–T604 extension to 74 years).

### 4.1 The Tax Block (T601–T604)

#### T601: Personal Tax Workers / T602: Social Insurance Tax Workers / T603: Indirect Taxes Workers
- **Registry**: Book Table 6.1, 1952–1989, billions USD
- **Verdicts**: All MATCH
- **Session 20 work**: T603 column fix (was loading property_tax_workers instead of sales_excise_tax_workers — ~78% understatement). Now loads both components (sales_excise + property_tax). T601–T604 extended to 74 years via NIPA 3.1 tax components.
- **KB lesson**: Chunk 18 (Table 6.1) should have the annual values for cross-check. DEC-008 already verified the tax allocation methodology against the book's framework (confirmed from chunk_09, pp 63–65). But Appendix N should document exactly which NIPA tables map to each tax component — this would validate our L07 extension logic.

#### T604: Total Tax on Workers (T_w = T601 + T602 + T603)
- **Registry**: Derived identity, 1952–1989
- **Verdict**: MATCH
- **Note**: Identity now holds (max error 0.0001 post-T603 fix).

### 4.2 The Benefits Block (T605–T606)

#### T605: Government Benefits to Workers (B_w)
- **Registry**: Book Table 6.2, 1952–1989, billions USD
- **Verdict**: MATCH (93% faithfulness for extension)
- **Extension**: NIPA 2.1 government social benefits; CR = 1.000 (splice quality perfect)
- **KB lesson**: Chunk 18 Table 6.2 has annual values. The 1996 welfare reform (DEC-006) creates a structural break that is documented but not adjusted.

#### T606: Government Services to Workers (G_w)
- **Registry**: Book Table 6.2, 1952–1989, billions USD
- **Verdict**: MATCH
- **Session 20 fix**: Was using frozen 1989 ratio (NIPA 3.1 × 0.5614); now correctly uses NIPA 3.2 + 3.3 with 40% defense exclusion (the book's formula).
- **KB lesson**: Appendix N should document the exact decomposition of government consumption expenditure into worker-relevant components. The 40% defense exclusion is a key parameter — is it constant or does the book vary it? Chunk 18 figures (Figs 6.1–6.3) may illustrate this.

### 4.3 The NSW Block (T607–T609)

#### T607: Net Social Wage (NSW = B_w + G_w − T_w)
- **Registry**: 1952–2025, billions USD
- **Verdict**: JUSTIFIED_DEVIATION
- **Construction**: Pre-computed from components in source CSV + NIPA extension
- **Key finding**: NSW negative for 92% of years — workers subsidize the state, not vice versa. COVID-19 spike to 8.95% of GDP in 2020, now returning to historical levels.
- **KB lesson**: Chunk 18–19 should have Table 6.3 (annual NSW values). Cross-check book values against our CSV. The 1996 structural break (T605/T606) may affect the extended series composition even though the aggregate NSW is smooth.

#### T608: NSW/V* Ratio
- **Registry**: Derived, 1952–1989, ratio
- **Verdict**: JUSTIFIED_DEVIATION
- **Issue**: M01-adjusted V* used in denominator. Plausible range [-0.02, +0.09].
- **KB lesson**: Table 6.4 (chunk 19–20) has these ratios. This is the measure that shows the exploitation rate including fiscal transfers — the "true" rate of exploitation.

#### T609: NSW/NI Share — UNKNOWN DENOMINATOR
- **Registry**: Book Table 6.4, 1952–1989, share
- **Verdict**: JUSTIFIED_DEVIATION (but Investigation 2 flagged the denominator as unidentified)
- **Issue**: Loaded from pre-computed column in Table6_3_Extended.csv. The "NI" denominator is never independently loaded. Could be NIPA National Income (~82% of GDP), Personal Income, NDP, or EC.
- **KB lesson**: **This is directly resolvable from the KB.** Chunk 37 (Appendix N, Table N.2) should define NI. Even without Appendix N, we can reverse-engineer: compute X = T607/T609 for each year and match against known NIPA aggregates. Investigation 2 estimates this at 30 minutes. Session 20 handoff notes "NI = NIPA National Income (~82% of GDP); reverse-engineered."
- **Quick fix**: Confirm via KB, load NI independently from NIPA 1.7.5, add V05 identity check.

---

## 5. Chapter 4 Series Review (T401–T402)

#### T401: A-Matrix (Technical Coefficients)
- **Registry**: Book Table 4.1, 6 SIC benchmark years (1947, 1958, 1963, 1967, 1972, 1977), matrix
- **Verdict**: MATCH
- **Status**: benchmark_only — no annual series, just the matrices themselves
- **Session 20 work**: L11b added 5 NAICS benchmark years (1997, 2002, 2007, 2012, 2017)
- **KB lesson**: Chunks 10–11 contain the IO methodology. The exact formula for the A-matrix (a_ij = purchases from sector i by sector j ÷ total output of sector j) is standard, but the book's specific sector aggregation scheme (85 SIC sectors → productive/unproductive) is NOT standard and is documented in these chunks + Appendix B (which may be in chunks 28–30 or early appendix chunks).

#### T402: B-Matrix (Leontief Inverse, (I−A)^{−1})
- **Registry**: Derived from T401, same years
- **Verdict**: MATCH
- **Note**: Near-singular tolerance documented. Condition numbers acceptable for all benchmark years.
- **KB lesson**: Chunk 11 has the theoretical derivation including equations for λ* = hp* × (I − app*)^{−1}. The distinction between "total requirements" and "direct requirements" matrices is important for the labor value computation (T701).

---

## 6. Chapter 7 Series Review (T701–T703)

This is the most theoretically complex part of the project and the one where the KB is most critically undermined.

#### T701: Labor Values (λ = l(I−A)^{−1})
- **Registry**: Book Table 7.1, 6 SIC benchmark years, labor_hours_per_dollar
- **Verdict**: MATCH
- **Construction**: Correctly computes λ from hours data (hp*) and Leontief inverse (T402)
- **KB lesson**: Chunk 11 equations document the labor value formula. The key input is hp* (hours of productive labor per unit of output for each sector). Where does this come from? BLS produces hours data by industry, but the mapping to IO sectors requires a concordance. Appendix N should document the exact BLS series used.

#### T702: Prices of Production — R² CRISIS
- **Registry**: Book Table 7.2, 6 SIC benchmark years, index
- **Verdict**: JUSTIFIED_DEVIATION
- **THE CORE PROBLEM**: The book reports R² = 0.98 for the price-value regression (1958 data). Our pipeline produces R² = 0.003–0.035 for NAICS-era (1997–2017) data. The README claims 0.70–0.98 but the T703.csv file actually does contain these correct SIC-era results — the confusion is between the main P14 output (SIC era, correct) and the supplementary A06 analysis (NAICS era, poor).
- **Investigation 1 analysis**: Five possible explanations:
  1. Aggregation effect (71 NAICS vs 85 SIC sectors reduces variation)
  2. Concordance noise (SIC→NAICS mapping)
  3. Real structural change (financialization reduces price-value correspondence)
  4. Hours data quality (headcount vs hours, output unit issues)
  5. Regression specification mismatch (log market prices vs log prices of production)
- **KB lesson**: **CHUNKS 22–24 ARE CRITICAL.** The book's Ch 7 methodology should specify:
  1. Whether it regresses log(observed market prices p_j) on log(labor values λ_j) — this would give high R² because both are driven by capital intensity
  2. Or log(prices of production pp_j) on log(labor values λ_j) — this should give lower R² because pp includes the uniform profit rate markup
  3. The exact definition of pp*_j: is it (1+r̄)(c_j + v_j) in labor value terms or money terms?
  4. How the labor value of money (λ_m = total productive hours / total value added) is computed
  DEC-011 notes this conversion was partially applied (MAD improved from 31,000% to 72–87%) but R² still low. The remaining issue may be the regression specification itself.
- **Action**: Read chunks 22–24 carefully, compare regression spec, test on 1958 SIC data first.

#### T703: Value-Price Deviations
- **Registry**: Book Table 7.3, same years, percent
- **Verdict**: JUSTIFIED_DEVIATION
- **Note**: The SIC-era R² values (0.70–0.98) ARE in the output. The A06 NAICS-era R² values (0.003–0.035) are supplementary. The verdict is justified because the main output is correct.

---

## 7. Chapters 2, 8, 9 Series Review (T201, T801, T901)

#### T201: Alternative GFP Measures (Ch 2) — UNKNOWN
- **Registry**: Wave 3 deferred
- **Status**: wave3_planned
- **What it is**: Table 2.1 compares orthodox GDP with Marxian GFP, showing TP* ≈ 82% of IO gross product, TP* ≈ 1.5× GNP, GFP* ≈ 15% smaller than GNP.
- **KB lesson**: Chunks 04–05 have Ch 2. This is primarily a theoretical comparison table, not a time series to be extended. Content type should be "cross_sectional" or "theoretical" per Anu Suite rules.

#### T801: Cross-Study Comparison (Ch 8) — UNKNOWN
- **Registry**: Wave 3 deferred
- **Status**: wave3_planned
- **What it is**: Table 8.1 compares Shaikh-Tonak with Wolff, Mage, and other researchers' estimates of Marxian categories.
- **KB lesson**: Chunks 25–27 have Ch 8. Much of the international comparison data (Aglietta on France, Mage on US, Khanjian/Cronin/Gouverneur on other countries) is here. However, the N-series already replicate most relevant external studies. T801 may be best treated as a formatted comparison table assembled from existing series, not an independent computation.

#### T901: Summary Table (Ch 9)
- **Registry**: 1948–1989, mixed units
- **Verdict**: JUSTIFIED_DEVIATION (88% faithfulness)
- **Construction**: Pure assembler — pulls from T506, T511, T512, T513, T514, T608
- **Note**: Inherits all deviations from source series but is itself correctly assembled.

---

## 8. External Studies Review (N-series)

### 8.1 Studies That Are Working Well

| Study | Series | Verdict | Notes |
|-------|--------|---------|-------|
| ST 1987 | N1101–N1103 | All MATCH | Clean derivations from T604/T605 + BEA NIPA |
| ST 2002 | N1201–N1202 | Both MATCH | Uses NIPA GDP correctly (N1201 fallback never triggers) |
| Mohun 2005 | N1401–N1404 | 2 MATCH, 2 JUSTIFIED | ST/Mohun ratio = 1.61 (stable); N1402 fixed to use pre-computed share |
| Mohun 2013 | N1501–N1504 | 2 MATCH, 2 JUSTIFIED | 0.813 working class fraction from paper Section 3 |
| Cronin NZ | N1701–N1704 | All MATCH | Input files present, correct passthrough/conversion |

### 8.2 Studies Requiring Attention

#### Tonak 1984 (N1001–N1002)
- **Verdicts**: JUSTIFIED_DEVIATION (both)
- **Issue**: Registry cites wrong table numbers (Table II → should be Table V for N1001, Table III → Table X for N1002). Formula is correct.
- **KB lesson**: The Tonak 1984 dissertation is NOT in our HDARP KB (the KB covers Shaikh & Tonak 1994 only). However, chunks 18–21 (Ch 6) may reference Tonak's earlier work since Chapter 6 builds on his dissertation methodology.
- **DEC-012 compliance**: These series formerly used synthetic data; now marked as "calculated" from HDARP extraction of Table V.B (28 years available).

#### Moos 2017 (N1301–N1305)
- **Verdicts**: 2 MATCH, 3 JUSTIFIED_DEVIATION
- **Key issue**: N1305 structural shift = +0.054 (our data) vs Moos's +0.030. Investigation 6 notes this is an 80% overstatement, likely due to NIPA vintage differences (our 2026 pull vs Moos's ~2015 data). The ACA and COVID transfers in 2010–2020 significantly changed the post-2000 benefit landscape.
- **DEC-013**: E2 (government consumption) is excluded from the NSW computation. With E2, mean = 0.071 (6.5× target); without E2, mean = 0.013 (within 0.002 of Moos's 0.011).
- **KB lesson**: The Moos 2017 paper is not in our KB, but the NSW methodology it extends IS documented in Ch 6 (chunks 18–21). Specifically, whether Moos uses the same allocation formula for taxes and benefits that Shaikh & Tonak (1994) use would help calibrate the comparison.

#### Turkey 2022 (N1601–N1602)
- **Verdicts**: Both JUSTIFIED_DEVIATION
- **Session 20 fix**: N1601 now uses TurkStat Table 20.37 (compensation of employees as % of GDP) instead of the incorrect SBB Personel proxy. N1602 had the 0.35 multiplier removed.
- **Data gap**: 2007–2019 are NaN per DEC-012 (TurkStat yearbook 2012 doesn't publish income-approach GDP for those years).
- **KB lesson**: The Karabacak & Tonak 2022 paper methodology may be referenced in a future HDARP extraction, but is not currently in the KB.

---

## 9. Cross-Cutting Structural Issues

### 9.1 The Unit Mismatch Problem

The deepest unresolved structural issue. Series from different book tables use different unit conventions:

| Source | Unit Convention | Series |
|--------|---------------|--------|
| Table E.2 | Billions USD (original NIPA scale) | T501, T502, T503, T508, T509 |
| Table 5.5 / 5.7 | Implicit: millions USD (÷1000 from thousands in L02) | T504, T505, T506, T507, T510, T511, T512 |
| Table 5.11 | Rate (dimensionless) | T513, T514 |
| Table E.3 | Thousands (persons) | T515, T516 |
| Table 6.x | Billions USD (original NIPA scale) | T601–T609 |

The T501–T503 (billions) vs T504–T505 (millions) mismatch means:
- GFP − V* ≠ S* in raw units (off by factor ~1000)
- NSW/V* computation (T608) requires unit conversion
- The profit rate S*/K mixes S* (millions) with K (BEA millions with UNIT_MULT=6)

**M01 and M99 compensate at runtime** — they apply scaling factors that make the output correct. But the underlying data layer is inconsistent. A comprehensive unit audit (proposed as "Step 0" in DEC-010) should precede all Wave 2 work.

**KB resolution**: Appendix N (chunks 35–37) should document the unit convention for each table. Appendix E tables (chunks 31–34) contain the actual data in its original units — reading these would settle the question definitively.

### 9.2 Table5_7_Extended.csv — The Fabricated Artifact

This file was created by Claude Opus 4 in Session 5 (Feb 24, 2026) as a convenient way to extend T506, T511, T512. It contains:
- Piecewise-linear interpolation (not real data)
- Three segments: -0.002/yr, -0.004/yr, -0.002/yr
- Column headers falsely claiming "BLS CES" provenance
- No generation script

**Current dependency**: After Session 20 fixes, T506 and T512 are recomputed from components (P04, M01). Only T511 may still depend on this file.

**Investigation 4** proposes: if T511 = T515/(T515+T516) is viable, the file can be deprecated entirely.

### 9.3 The SIC-NAICS Gap (1978–1996)

The IO framework has data for:
- SIC era: 1947, 1958, 1963, 1967, 1972, 1977 (6 benchmarks, 85 sectors)
- NAICS era: 1997, 2002, 2007, 2012, 2017 (5 benchmarks, 71 sectors)
- Gap: 1978–1996 (no IO data)

The 1978–1996 gap is 19 years. It spans the Reagan deregulation era, S&L crisis, and early Clinton years — a period of significant structural change in the US economy. Simple linear interpolation of IO coefficients across this gap is risky.

**KB lesson**: The book itself only uses SIC-era data through 1977. The extension beyond 1977 is entirely our work. Chapter 4 methodology (chunks 10–11) documents the interpolation approach between benchmarks within the SIC era. Whether that same approach is valid across the SIC-NAICS break is an open methodological question.

**Possible bridge**: BEA published a 1992 benchmark in both SIC and NAICS-compatible format. If this can be obtained, the gap narrows to 1978–1991 and 1993–1996.

### 9.4 The No-BLS-API-Key Problem

Five open issues depend on BLS data:
- T516 total_scale (needs CES0000000001)
- T511/T512 component extension (needs employment by industry)
- T510 component recomputation (needs compensation by industry)

**Workaround**: BLS data can be downloaded manually from bls.gov/data/ without an API key (just slower). Or fetch via FRED, which mirrors many BLS series.

---

## 10. Knowledge Base Lessons — What the Book Actually Says

This section synthesizes what the KB has already taught us and identifies the specific questions that targeted KB mining would answer.

### 10.1 Already Learned from KB

| Lesson | Source | Applied To |
|--------|--------|-----------|
| Tax allocation = income-proportional (T_w = taxes × W_p/PI) | Chunk 09, pp 63–65 | DEC-008, T601–T604 |
| Rate of surplus value S*/V* differs from profit/wage ratio P/W by factor ~3× | KB Summary, p70 | T506 vs orthodox measures |
| Lp/L declined >37% postwar; Lu/Lp rose 138% | KB Summary, p130 | T511, T512 interpretation |
| Tax rates rose from 18% to 32% (1952–1988); benefit rates from 11% to 28% | KB Summary, p160 | T601–T606 validation |
| Government G = G' + W_G (purchases + wages) | KB Summary, p80 | T606 decomposition |
| λ* = hp* × (I − app*)^{−1} (labor value equation) | KB Summary, p220 | T701 formula |
| S*/V* differs from true rate by only 6–9% due to price-value deviations | KB Summary, p220 | T506/T703 cross-check |
| TP* ≈ 82% of IO gross product; TP* ≈ 1.5× GNP | KB Summary, p240 | T201, T501 |

### 10.2 Questions the KB Can Answer (Targeted Mining)

| # | Question | KB Location | Impact | Effort |
|---|----------|-------------|--------|--------|
| Q1 | What is the exact employment universe (total nonfarm? civilian?) | App N (chunks 35–37) | Resolves T516 scale (Investigation 5) | 20 min |
| Q2 | What is "NI" in the NSW/NI ratio? | App N, Table N.2 (chunk 37) | Resolves T609 (Investigation 2) | 15 min |
| Q3 | What BEA tables does the book use for C*_m (intermediate inputs)? | App N (chunks 35–37) | Informs Wave 2 B3 (T502 fix) | 30 min |
| Q4 | What is the profit rate denominator: C*+V* (flow) or K* (stock)? | Ch 5, Table 5.11 note (chunks 15–16) + App N | Resolves T513/T514 (Investigation) | 30 min |
| Q5 | What variables does the Ch 7 regression use? log(p) on log(λ) or log(pp) on log(λ)? | Ch 7 (chunks 22–24) | Resolves T702/T703 R² crisis (Investigation 1) | 1 hr |
| Q6 | How does the book interpolate IO coefficients between benchmark years? | Ch 4 (chunks 10–11) | Defines Wave 2 interpolation methodology | 30 min |
| Q7 | What is the productive sector classification rule? | Ch 3 (chunks 06–09) + App B (chunk 27?) | Defines Wave 2 B2 classification engine | 1 hr |
| Q8 | What BLS series does the book use for employment (CES? CPS?)? | App N (chunks 35–37) | Validates T515/T516 extension source | 20 min |
| Q9 | Does the 40% defense exclusion for G_w vary over time? | App N or Ch 6 (chunks 18–19) | Validates T606 extension | 15 min |
| Q10 | What are the exact Table E.2 and E.3 annual values? | App E (chunks 31–34) | Cross-checks T501–T516 book-period data | 1 hr |
| Q11 | Does V* in Table 5.7 include or exclude net royalty payments? | App N + Ch 5 (chunks 12–14) | Clarifies T504/T506 level accuracy | 20 min |
| Q12 | What capacity utilization source does the book use pre-1967? | App N (chunks 35–37) | Validates T514 extension | 15 min |

**Total KB mining effort: ~6 hours across 2–3 sessions.**

### 10.3 KB Content That Would Generate NEW Series or Analyses

Beyond fixing existing issues, the KB contains material for new work:

1. **The Wharton capacity utilization index** (referenced in the book for pre-1967 years) — if extractable, would allow extending T514 further back than FRED's 1967 start
2. **Mage (1963) comparison data** (Ch 8) — could create N1801 series comparing our exploitation rate with Mage's pioneering estimate
3. **Wolff estimates** (Ch 8, Table 6.5–6.6 in chunk 20) — international comparison with France (Aglietta), Greece (Gouverneur), Puerto Rico (Wolff)
4. **The detailed IO matrices** (Ch 4) — the book's own A-matrices for 1947, 1958, 1963, 1967, 1972, 1977 at 85-sector detail are the canonical data for SIC-era labor value calculations
5. **Appendix B sector classification** — the definitive productive/unproductive boundary that Wave 2 needs to implement

---

## 11. Prioritized Next Steps

### Tier 0: KB Mining Sprint (No Code Changes)

These produce no code changes but unlock everything else. **Do this first.**

| # | Task | KB Source | Resolves | Effort |
|---|------|-----------|----------|--------|
| 0.1 | Read Appendix N in full (chunks 35–37) | Old HDARP | Q1, Q2, Q3, Q4, Q8, Q9, Q11, Q12 | 2 hr |
| 0.2 | Read Ch 4 methodology (chunks 10–11) | Old HDARP | Q6, Q7 (partial) | 1 hr |
| 0.3 | Read Ch 7 regression spec (chunks 22–24) | Old HDARP | Q5 (T702/T703 crisis) | 1 hr |
| 0.4 | Read Ch 3 sector classification (chunks 06–09) | Old HDARP | Q7 (productive boundary) | 1 hr |
| 0.5 | Cross-check Appendix E tables (chunks 31–34) against CSVs | Old HDARP | Q10 (data verification) | 1 hr |

**Total Tier 0: ~6 hours, 2 sessions. Output: a KB Findings Report documenting answers to Q1–Q12.**

### Tier 1: Quick Wins (< 1 hour each, no Wave 2 dependency)

| # | Task | Series | Effort | Impact |
|---|------|--------|--------|--------|
| 1.1 | Confirm T609 NI denominator (Investigation 2) | T609 | 30 min | Resolves 1 UNKNOWN → MATCH |
| 1.2 | Fetch CES0000000001 via FRED/manual download (Investigation 5) | T516 | 30 min | Reduces total_scale from 1.307 to ~1.08 |
| 1.3 | Test T511 = T515/(T515+T516) viability (Investigation 4) | T511 | 30 min | May deprecate Table5_7_Extended.csv |
| 1.4 | Add V05 identity checks: GFP, tax, exploitation, employment | V05 | 1 hr | 4 new automated checks |
| 1.5 | Update methodology review report verdicts to final state | Docs | 15 min | Accurate documentation |

**Total Tier 1: ~3 hours, 1 session.**

### Tier 2: Medium Fixes (1–3 hours each, no Wave 2 dependency)

| # | Task | Series | Effort | Impact |
|---|------|--------|--------|--------|
| 2.1 | Extend T601–T604 from components (if not already done — Session 20 claims done) | T601–T604 | Verify 30 min | Validates 74-year tax extension |
| 2.2 | T510 extension via BEA intermediate inputs proxy | T510 | 1–2 hr | Improves from 55% to ~70% faithfulness |
| 2.3 | T702/T703 — reproduce 1958 result, then diagnose NAICS divergence (Investigation 1) | T702, T703 | 2–3 hr | Resolves R² crisis |
| 2.4 | Moos structural shift calibration (Investigation 6) | N1305 | 1 hr | Explains 0.054 vs 0.030 gap |
| 2.5 | Comprehensive unit audit — trace every series to source table units | All | 2 hr | Prerequisite for Wave 2; resolves DEC-010 |
| 2.6 | Recompute T607 from extended components (T604, T605, T606 now all extended) | T607 | 1 hr | Full-component NSW (not pre-computed) |

**Total Tier 2: ~8–11 hours, 2–3 sessions.**

### Tier 3: Wave 2 — IO Framework Campaign (3–5 sessions)

This is the major remaining work. All tasks depend on Tier 0 KB mining (particularly the sector classification rules and IO methodology).

| # | Task | Series | Effort | Dependency |
|---|------|--------|--------|-----------|
| 3.1 | **B1**: Parse + validate 5 NAICS IO Use tables (1997–2017) | T401 | 4–6 hr | Tier 0.2 |
| 3.2 | **B2**: Build productive sector classification engine (SIC + NAICS) | All Ch 5 | 3–4 hr | Tier 0.4, 3.1 |
| 3.3 | **B3**: Fix T502 — C*_m via IO benchmark interpolation | T502, T503 | 2 hr | 3.2 |
| 3.4 | **B4**: Fix T511/T512 — component extension via IO employment classification | T511, T512, T504 | 2 hr | 3.2 |
| 3.5 | **B5**: Fix T513/T514 — K* from IO-restricted BEA Fixed Assets | T513, T514 | 2 hr | 3.2 |
| 3.6 | Recompute T510 from corrected T502/T504 | T510 | 1 hr | 3.3, 3.4 |
| 3.7 | SIC-NAICS bridge methodology (1978–1996 gap) | All IO series | 2–3 hr | 3.1, 3.2 |
| 3.8 | Full re-validation pass with updated V05 + V10 | All | 2 hr | All above |

**Total Tier 3: ~18–24 hours, 3–5 sessions.**

### Tier 4: Wave 3 + Polish

| # | Task | Series | Effort |
|---|------|--------|--------|
| 4.1 | T201 — implement Ch 2 alternative GFP comparison table | T201 | 2 hr |
| 4.2 | T801 — implement Ch 8 cross-study comparison (Wolff/Mage/Gouverneur) | T801 | 3 hr |
| 4.3 | New N-series from KB: Mage comparison, Aglietta France, Gouverneur Belgium | N18xx+ | 4 hr |
| 4.4 | NAICS-era labor value analysis paper (documenting R² decline) | Analysis | 4 hr |
| 4.5 | Final deliverables: LaTeX methodology report, PDF figures | Output | 3 hr |
| 4.6 | Fresh-environment test | QA | 1 hr |
| 4.7 | GitHub push + documentation update | Infra | 1 hr |

**Total Tier 4: ~18 hours, 3–4 sessions.**

---

## 12. Dependency Graph

```
TIER 0: KB Mining Sprint
  0.1 Appendix N ──────┬─> 1.1 T609 NI
  0.2 Ch 4 IO method ──┤   1.2 T516 CES
  0.3 Ch 7 regression ─┤   1.3 T511 recompute
  0.4 Ch 3 sectors ────┤   2.3 T702/T703 fix
  0.5 App E cross-check ┘   2.5 Unit audit

TIER 1: Quick Wins (parallel, no dependencies between them)
  1.1 ─┐
  1.2 ─┤
  1.3 ─┼─> All can run in parallel
  1.4 ─┤
  1.5 ─┘

TIER 2: Medium Fixes
  2.1 (verify tax extension) ───┐
  2.2 (T510 proxy) ─────────────┼─> 2.6 (recompute T607 from components)
  2.3 (T702/T703) ──────────────┤
  2.4 (Moos shift) ─────────────┘
  2.5 (unit audit) ─────────────────> TIER 3 (prerequisite)

TIER 3: Wave 2 IO Campaign
  3.1 (parse IO tables)
    └─> 3.2 (sector classification)
          ├─> 3.3 (T502 C*_m)
          ├─> 3.4 (T511/T512 components)
          ├─> 3.5 (T513/T514 K*)
          └─> 3.7 (SIC-NAICS bridge)
               └─> 3.6 (T510 recompute)
                    └─> 3.8 (full re-validation)

TIER 4: Wave 3 + Polish (after Tier 3 complete)
  4.1–4.7 all parallel after Tier 3
```

---

## 13. Effort & Session Estimates

| Tier | Total Effort | Sessions | Cumulative |
|------|-------------|----------|------------|
| 0 (KB Mining) | 6 hr | 2 | 2 |
| 1 (Quick Wins) | 3 hr | 1 | 3 |
| 2 (Medium Fixes) | 8–11 hr | 2–3 | 5–6 |
| 3 (Wave 2 IO) | 18–24 hr | 3–5 | 8–11 |
| 4 (Wave 3 + Polish) | 18 hr | 3–4 | 11–15 |

**Projected endpoint**: 11–15 sessions to reach 100% methodology compliance, all 59 series at MATCH or JUSTIFIED, zero UNJUSTIFIED, LaTeX report published, fresh-env tested.

**CORRECTION (from KB Deep Dive, Session 21)**: T513/T514 were classified UNJUSTIFIED due to "wrong denominator: K stock vs C*+V* flow." The KB confirms the book defines r* = S*/K (Section 5.5, page 122) — our formula is correct. Only the sector restriction (total K vs productive K*) remains. These should be reclassified as JUSTIFIED_DEVIATION, reducing UNJUSTIFIED count from 4 to 2 immediately.

**Projected scorecard after each tier**:

| Milestone | MATCH | JUSTIFIED | UNJUSTIFIED | UNKNOWN | Score |
|-----------|-------|-----------|-------------|---------|-------|
| Current (pre-correction) | 28 | 25 | 4 | 2 | ~83% |
| After KB correction (T513/T514) | 28 | 27 | 2 | 2 | ~86% |
| After Tier 0+1 | 30 | 27 | 0 | 2 | ~90% |
| After Tier 2 | 31 | 28 | 0 | 0 | ~93% |
| After Tier 3 | 35 | 24 | 0 | 0 | ~97% |
| After Tier 4 | 37 | 22 | 0 | 0 | 100% |

---

*Plan authored 2026-05-07 (Session 21). Source materials: 59-series registry, 16-decision log, 7-assumption register, 25-agent methodology review, 40-chunk HDARP Knowledge Base, 6-investigation plan, Wave 2 development plan, Phase 0 gap register, 20-session handoff chain.*
