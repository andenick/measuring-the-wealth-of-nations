# AS2 Decision Log

Structured record of all non-trivial design decisions. Each entry documents what was decided, why, and what it affects.

---

## DEC-001: T### Series ID Convention (2026-02-23)

**Decision**: Use T### IDs (e.g., T501, T601) instead of the Anu Suite standard S### convention.

**Rationale**: The T prefix encodes meaningful structure — the first digit is the chapter number (T5xx = Chapter 5, T6xx = Chapter 6), matching the book's table numbering. This makes IDs self-documenting for anyone familiar with Shaikh & Tonak (1994).

**Alternatives Considered**:
- S### (Anu standard): Rejected — loses chapter-table semantics
- S5xx (hybrid): Rejected — non-standard and confusing

**Impact**: All scripts, catalogs, DPRs, and registry entries use T### throughout. Documented as VAR-001 in VARIANT_REGISTRY.json.

---

## DEC-002: Accept DIV-001 — Total K Instead of Productive K* (2026-02-23)

**Decision**: Use total private fixed assets K from BEA Fixed Assets Table 4.1 as the denominator for Marxian profit rate r*, instead of restricting to productive sector capital K*.

**Rationale**: Restricting K to productive sectors requires the IO-based sector classification from Chapter 4 (Wave 2). Proceeding with total K allows Wave 1 to complete while preserving trend dynamics. The level of r* is understated but the trajectory is correct.

**Alternatives Considered**:
- Block T513/T514 until Wave 2: Rejected — would delay all downstream series
- Use Mohun's K* estimates: Rejected — different classification methodology

**Impact**: T513 and T514 profit rate levels are lower than book values.

**Status update (Session 23+)**: RESOLVED. K* = K × IO_productive_output_ratio (0.567) via L06 + L11 NAICS classification. r* increases 5.7% vs total K. Book confirms r* = S*/K (DEC-017).

---

## DEC-003: VA*/W Constant Assumption (2025-12-05, partially resolved 2026-03-30)

**Decision**: Initially used constant VA*/W = 1.238 for deriving V* from total compensation W. Partially resolved in Session 14 by enabling year-varying ec_u/ec_p input in marxian_accounts.py.

**Rationale**: The book computes V*/W from the ec_u/ec_p ratio (employee compensation per worker, unproductive vs productive sectors). The constant approximation matches benchmark years exactly but may diverge at inter-benchmark years. Full resolution requires BLS industry-level compensation data, unavailable for 1990-1997 (SIC-era gap).

**Alternatives Considered**:
- Linear interpolation between benchmarks: Feasible but introduces its own assumptions
- Wait for complete BLS data: Would delay extensions indefinitely

**Impact**: T504, T505, T506, T512 extension period values carry small systematic error. See ADJ-002.

---

## DEC-004: Growth-Rate Splice as Default Extension Method (2026-02-25)

**Decision**: Use growth-rate splicing as the default method for extending book-period series with modern API data.

**Rationale**: Growth-rate splicing preserves the level of the book-period endpoint while using the dynamics of the new data source. This is faithful to Shaikh & Tonak's own splicing methodology and minimizes discontinuity at the transition point.

**Alternatives Considered**:
- Direct level match: Used for some series (T511, T512) where sources are directly comparable
- Ratio splicing: Overly complex for most series

**Impact**: 19 extended series use this method. Splice quality assessed by V06.

---

## DEC-005: BLS CES Ratio as Productive Labor Proxy (2026-02-25)

**Decision**: Use BLS Current Employment Statistics (CES) production/nonsupervisory worker ratios as proxy for IO-based productive/unproductive labor decomposition when extending T511 and T512.

**Rationale**: The book's productive labor classification uses the IO framework (Chapter 4). For the extension period, BLS CES production workers in goods-producing industries provide the closest available proxy. Cross-validated against Mohun (2005) estimates.

**Alternatives Considered**:
- Wait for IO framework (Wave 2): Would block T511/T512 extension
- Use total manufacturing employment: Too narrow (excludes mining, construction, transport)

**Impact**: T511 and T512 extensions are certified at 78% and 76% faithfulness respectively (CERTIFIED WITH NOTES).

---

## DEC-006: 1996 Welfare Reform Bridge (2026-03-30)

**Decision**: Handle the 1996 Personal Responsibility and Work Opportunity Reconciliation Act transition by using NIPA Tables 2.1 and 3.1 for continuous coverage, with explicit documentation of the policy discontinuity.

**Rationale**: The 1996 welfare reform restructured federal benefits programs. NIPA data provides continuous coverage across this transition, though the composition of benefits changed significantly. The discontinuity is documented but not adjusted.

**Alternatives Considered**:
- Split pre/post-1996 as separate subseries: Rejected — overcomplicates for minimal analytical gain
- Apply adjustment factor: Rejected — no reliable basis for calibration

**Impact**: T605 and T606 show a structural break around 1996-1997. Flagged in V03 continuity checks.

---

---

## DEC-007: SIC-NAICS Gap Interpolation Method (2026-04-08)

**Decision**: Use log-linear interpolation for ec_u/ec_p ratio between 1989 (book value) and 1998 (first NAICS year from BEA NIPA 6.2D).

**Rationale**: BEA NIPA 6.2D industry-level compensation data starts at 1998 (NAICS era). The 1990-1997 gap cannot be filled from this source. Log-linear interpolation preserves the smooth transition between known endpoints.

**Impact**: T504, T505, T506, T512 extension period 1990-1997 values are interpolated. M01 confirmed ec_u/ec_p changes are small (max 0.42 from constant assumption).

---

## DEC-008: Ch6 Tax Allocation Methodology Verified (2026-04-09)

**Decision**: Confirmed that the income-proportional tax allocation method (T_w = taxes × W_p/PI) aligns with the book's framework.

**Rationale**: HDARP extraction of Section 3.3 (chunk_09, pages 63-65) documents the "net royalty" framework: NRYwp = net taxes on productive workers. The book uses the same worker-share-of-income approach for allocating taxes. Section 5.9 and Appendix N provide the detailed estimation, which our P09 implementation follows.

**Verification**: Confirmed from book quote p.64: "The true measure of variable capital is the nominal wage of productive workers minus any net royalty payments made by them."

**Impact**: No change needed. P09 methodology is correct.

---

---

## DEC-009: T504 Splice Fix Deferred — Unit Scaling Issue (2026-04-09)

**Decision**: The T504 splice quality (CR=0.81) cannot be fixed by simply substituting NIPA T20100 aggregate compensation for the interpolation. Attempting this worsened the splice to CR=0.11 due to unit scaling mismatch between book-period V* (millions, from Table 5.7 direct calculation) and extension-period W×(V*/W) (derived from BEA 6.2D compensation in different base units).

**Rationale**: The book's V* is computed from ec_p × L_p (average productive wage × productive employment) which gives a different magnitude than total compensation of employees × (V*/W). The proper fix requires understanding the exact ratio between book V* and NIPA total compensation — this is part of the broader Wave 2 unit normalization.

**Data acquired**: `Inputs/API_Data/BEA/nipa_T20100_compensation_1929_2025.csv` (97 years, fetched from BEA API) — available for future use.

**Impact**: T504 splice remains at CR=0.81 (documented as WARN-04, accepted).

---

---

## DEC-010: DIV-001 Blocked by Unit Mismatch (2026-04-09)

**Decision**: The K→K* capital stock restriction (DIV-001/ADJ-001) cannot be properly computed until the unit mismatch across dollar-denominated series is resolved. T505 (S*) is in millions (from Table 5.7), while K from BEA Fixed Assets is in millions with UNIT_MULT=6. Computing S*/K gives inflated ratios because the series aren't on the same base.

**Root Cause**: The original Shaikh Tonak project computed V* and S* from a different pathway than the Table E.2 aggregates (T501-T503). The Table 5.7 ratios (e, V*/W, Lp/L) are self-consistent, but the dollar magnitudes use different unit conventions.

**Required**: A comprehensive unit audit that traces each series back to its source table, identifies the unit conversion, and creates a normalization layer. This is a foundational Step 0 that should precede all other Wave 2 work.

**Impact**: ADJ-001 remains BLOCKED pending unit normalization. M02_adjust_profit_rates.py is created but produces incorrect results with current mixed units.

---

---

## DEC-011: T702-T703 Require Labor Value of Money Conversion (2026-04-09)

**Decision**: The initial T702-T703 computation produced incorrect results (R²=0.003-0.035, MAD=31,000%+) because it compared labor values λ* (hours/$) with money-based prices of production pp* (comp/$). These are in different units.

**Correct approach**: The book computes prices of production in labor-value terms using the labor value of money λ_m = total productive hours / total value added. Money compensation v_j must be converted to labor-value compensation via v_j × λ_m before computing pp*_j = (1+r̄)(c_j_labor + v_j_labor).

**Status**: Data saved as T702/T703 JSON files. Proper computation requires λ_m calculation from KLEMS hours + IO value added. Deferred to next focused session.

**Reference**: IO_METHODOLOGY_EXTRACTION.md Section IX (rates of exploitation formulas), HDARP chunk_11 (pages 101-110).

**Update (2026-04-09)**: Applied λ_m conversion — MAD improved from 31,000% to 72-87%. R² still low (0.003-0.035). Remaining issue: surplus computation uses GO-V* instead of VA-V*. The book's methodology (Section 4.2, pp.86-88) requires careful sector-level value-added decomposition. Further refinement needed in dedicated session.

---

## DEC-012: No Synthetic Data Policy (2026-05-03)

**Decision**: Retroactively apply a strict no-synthetic-data rule. All series with `"status": "synthetic"` or `"data_quality": "estimated_from_benchmarks"` must be replaced with real data extracted from HDARP, APIs, or digitized figures. If real data cannot be obtained, the series is marked `data_unavailable` with an empty CSV — never filled with fabricated values.

**Rationale**: The Anu Extension Standard Principle 10 ("FAIL ON UNCERTAINTY") logically extends to data itself. Synthetic placeholders that use `np.random` to generate fake annual data from summary statistics violate the Anu Suite's core commitment to provenance and reproducibility. Five N-series (N1001, N1002, N1601, N1602, N1701) were identified as using synthetic data.

**Remediation plan**:
- N1001/N1002 (Tonak 1984): Extract real annual data from HDARP Table V.B (28 years available)
- N1601/N1602 (Turkey 2022): Digitize from paper figures or obtain TURKSTAT data
- N1701 (Cronin NZ 2001): Digitize from paper figures or obtain Stats NZ data

**Impact**: All 13 Anu Suite skill files updated with explicit no-synthetic-data rules. Series registry, processing scripts, DPRs, and EPRs to be updated as data is obtained.

---

## DEC-013: Moos NSW Formula — E2 Excluded (2026-05-06)

**Decision**: The independent Moos (2017) NSW replication (P21) uses `NSW = E1 - (T1 + T2*LS)` — direct social benefits minus taxes. Government consumption expenditure (E2: education, health, transportation from NIPA T3.16) is loaded by L17 but NOT included in the NSW computation.

**Rationale**: The standard Shaikh-Tonak/Moos NSW formula measures the net fiscal transfer to workers: direct benefits received minus taxes paid. Government consumption on education, health, and transportation is a distinct concept ("social wage in kind") not included in Moos's published results. With E2 excluded, P21 produces a 1959-1997 overlap mean of 0.013 — within 0.002 of Moos's published 0.011 (residual gap attributable to NIPA vintage differences between our 2026 pull and Moos's ~2015 data). With E2 included at alpha=1.0, the mean is 0.071 — far from the target.

**Prior state**: L17 also had incorrect T3.16 line number mappings (education=15 was actually "Highways", etc.). Fixed to education=30, health=28, transportation=14 based on CSV LineDescription verification.

**Alternatives Considered**:
- Include E2 at partial allocation (alpha=0.05-0.30): Rejected — no published evidence for any specific fraction, and even small alphas overshoot the 0.011 target
- Include E2 at full allocation (alpha=1.0): Rejected — produces mean=0.071, 6.5x the target

**Impact**: N1301-N1305 series, V11 benchmark range [0.008, 0.018]. E2 data retained in L17/parsed CSVs for future sensitivity analysis.

---

---

## DEC-014: Turkey Labor Share — TurkStat HDARP Replaces SBB Proxy (2026-05-06)

**Decision**: N1601 (Turkish labor share) now uses TurkStat national accounts data (Table 20.37: compensation of employees as % of GDP, 1980-2006) extracted via HDARP from `turkstat_statistical_indicators_1923_2011.pdf`. The SBB "Personel" budget expenditure share proxy is removed.

**Rationale**: The SBB Personel share measures government personnel spending as a fraction of total government expenditure — structurally different from the economy-wide labor share (compensation of all employees / GDP). TurkStat Table 20.37 is the official Turkish national accounts income-approach decomposition, directly comparable to the Karabacak & Tonak (2022) methodology.

**Data coverage**: 1980-2006 (27 years) from TurkStat. The yearbook 2012 does NOT publish income-approach GDP tables for 2007-2012. Years 2007-2019 are NaN per DEC-012 (no synthetic fill).

**Impact on N1602 (NSW/GDP)**: Mean improved from -0.0025 to -0.0098 (paper reports -0.011). The `* 0.3` transfer multiplier and `* 1.1` tax multiplier in Path A/B of P18 were also removed — these were artifacts of the proxy calibration, not the paper's methodology.

**Alternatives Considered**:
- OECD compensation data for 2007-2019: Only has tax/GDP ratios, not compensation
- World Bank employment-pop-ratio proxy: Rejected — DEC-012 prohibits synthetic fill

---

---

## DEC-015: T502 GDP Proxy Accepted for Wave 1 (2026-05-07)

**Decision**: T502 (C*_m, constant capital / materials consumed) extension uses GDP growth-rate proxy from BEA NIPA 1.7.5, same as T501 Phase 1.

**Rationale**: The book's C*_m extension methodology requires IO benchmark-year M'p/GVAp ratios interpolated annually and applied to NIPA GVA_productive. This requires the full IO framework (Phase B of Next Steps Plan) which is not yet built. GDP growth rates are a reasonable approximation for Wave 1.

**Impact**: T503 (GFP) inherits this approximation. Mitigated by identity enforcement in P01 (T503 = T501 - T502), ensuring internal consistency even if absolute levels are approximate.

**Status**: ACCEPTED for Wave 1. Will be replaced when Phase B IO framework provides annual productive-sector intermediate input data.

---

## DEC-016: T511/T512 Principle 3 Violation Accepted for Wave 1 (2026-05-07)

**Decision**: T511 (Lp/L) and T512 (V*/W) are extended as ratios from pre-built `Table5_7_Extended.csv`, not via separate extension of numerator and denominator (Anu Principle 3 violation).

**Rationale**: Extending Lp and L separately requires the IO-based productive labor classification (Phase B IO framework). Without it, there is no data source for annual productive employment counts — only the BLS CES production/nonsupervisory worker proxy, which maps to a different concept than the book's IO-based boundary.

**Technical note**: The pre-extended values in Table5_7_Extended.csv use piecewise-linear interpolation in three segments (-0.002/yr, -0.004/yr, -0.002/yr), not actual BLS CES data despite column header labels suggesting otherwise.

**Impact**: T512 is upstream of T504 (V* = W × T512 ratio), propagating the approximation into the exploitation rate chain. The M01 adjustment (ec_u/ec_p) partially compensates.

**Faithfulness**: T511=78%, T512=76% (per DEC-005 proxy assessment).

**Status**: ACCEPTED for Wave 1. Wave 2 will extend Lp and L separately using IO classification, then recompute T511=Lp/L and T512=V*/W from components.

---

## DEC-017: T513/T514 Denominator Confirmed as S*/K (Stock) (2026-05-08)

**Decision**: The 25-agent methodology review's UNJUSTIFIED verdict on T513/T514 ("wrong denominator: K stock vs C*+V* flow") was incorrect. The book defines r* = S*/K (Section 5.5, p.122). Reclassified to JUSTIFIED_DEVIATION.

**Evidence**: KB deep dive Session 21 read chunk 15 (Section 5.5): "the Marxian general rate of profit r*, defined here as the ratio of surplus value to total fixed capital K." Footnote 16 acknowledges circulating capital should be added but isn't due to data limitations. The remaining gap (total K vs productive K*) is DEC-002.

**Impact**: UNJUSTIFIED count drops from 4 to 2. T513/T514 faithfulness upgraded from 60% to 70%.

---

## DEC-018: T609 Denominator Confirmed as National Income (2026-05-08)

**Decision**: T609 (NSW/NI) denominator is NIPA National Income, confirmed by reverse-engineering. The book has TWO NSW ratio measures: Table 6.3/6.4 uses NI; Appendix N Table N.2 uses EC (Employee Compensation).

**Evidence**: Reverse-engineering T607/T609 yields a denominator that is ~0.97 of known NI values, ~0.81 of GDP, and ~1.45 of EC — matching National Income.

**Impact**: T609 verdict could be upgraded from JUSTIFIED_DEVIATION to MATCH once NI is independently loaded and identity-checked.

---

## DEC-019: T511 = T515/(T515+T516) Not Viable (2026-05-08)

**Decision**: Cannot deprecate Table5_7_Extended.csv by recomputing T511 from T515/(T515+T516). The BLS-based ratio is structurally flat (~0.49) while the book's IO-based Lp/L declines from 0.57 to 0.36. Max discrepancy: 0.23 (extension period).

**Root cause**: BLS "production and nonsupervisory workers" covers ~82% of private employment (stable share). The book's "productive labor" uses IO sector classification + within-sector production worker ratios, producing a much smaller and declining share.

**Impact**: Table5_7_Extended.csv remains in pipeline for T511. Wave 2 IO framework (B4) is the only viable fix. T511 UNJUSTIFIED verdict stands.

---

## DEC-020: T504/T505 Source CSV Contains Wrong-Unit Phase 3 Data (2026-05-08)

**Decision**: The `VariableCapital_SurplusValue.csv` source file does NOT contain the book's actual V* and S* values. It contains Phase 3 intermediate calculations that are 9-15x too large relative to the book's Table H.1 values (confirmed by KB deep dive).

**Evidence (unit audit)**:
- T501 (TP*): pipeline 446.21 vs KB 446.25 → ratio 1.000 (CORRECT, billions)
- T504 (V*): pipeline 1,294.2 vs KB 88.41 → ratio 14.6x (WRONG)
- T505 (S*): pipeline 1,673.1 vs KB 149.94 → ratio 11.2x (WRONG)
- Implied S*/V* from T505/T504 = 1.293, not 1.70 (the correct exploitation rate)

**Why pipeline still works**: T506 (exploitation rate) comes from Table5_7_KeyRatios.csv (correct ratios 1.70-2.44), not from T505/T504. Extension-period T504 is computed from correct ratios (T512 × W). The wrong levels are isolated to book-period T504/T505.

**Affected downstream**: T608 (NSW/V*) uses T504 levels — these are wrong by 14.6x in the book period.

**Fix**: Replace VariableCapital_SurplusValue.csv with actual Table H.1 annual data (V* and S* in billions, 1948-1989). This data exists in the HDARP extraction (chunk 35, Appendix H) but needs full 42-year digitization from the original PDF.

**Status**: RESOLVED (Session 22). L02b_reconstruct_v_star.py generates V_S_star_reconstructed.csv from 8 KB-verified V* data points + 11 KB-verified e* data points. L02 modified to read from this source. V01 benchmarks updated to correct KB values (1948: 88.41, 1972: 324.30, 1989: 1206.40). Pipeline PASS, 15 validators clean, T608 now shows correct values (-0.03 to -0.13 range).

---

*Last updated: 2026-05-08 (KB deep dive: DEC-017 through DEC-020, encoding fixes, unit audit)*
