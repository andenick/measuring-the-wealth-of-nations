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

**Impact**: T513 and T514 profit rate levels are lower than book values. Resolution planned for Wave 2 (ADJ-001).

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

*Last updated: 2026-05-03 (no-synthetic-data policy)*
