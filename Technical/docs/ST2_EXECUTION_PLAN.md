# ST2 Execution Plan — Path to Perfect Replication

**Date**: 2026-05-08
**Author**: Claude Opus 4.6 (Sessions 21-22)
**Pipeline state**: PASS, 17.2s, 59 series, 15 validators, 0 failures
**Current score**: 28 MATCH / 27 JUSTIFIED / 2 UNJUSTIFIED / 2 UNKNOWN
**Target**: 0 UNJUSTIFIED, 0 UNKNOWN, all faithfulness >85%, full annual book data

---

## Execution Order

Steps are numbered in the order they should be executed. Dependencies are explicit. Each step lists files touched, effort, and the specific improvement it produces.

---

### Step 1: Digitize Table H.1 Full Annual Data (42 years)

**Why first**: Every downstream step benefits from correct annual S*/V*, V*, S* values. The current Table5_7_KeyRatios.csv has linear interpolation between 5 benchmarks — the real data has year-to-year fluctuations (e.g., 1972: book says 1.99, our CSV says 2.10).

**What**: Extract all 42 rows × 19 columns of Table H.1 from the original PDF using HDARP agent reading on the chunk_35 PDF (10 pages, pages 322-331). Also extract Table 5.7 (chunk 14, the actual annual ratios for e, Lp/L, V*/W, C*/V*).

**Method**:
1. Read chunk_35 PDF (`Shaikh Tonak Book Processing/Technical/pdf_chunks/*chunk_35.pdf`) with agent vision — extract Table H.1 rows for ALL 42 years (1948-1989)
2. Read chunk_14 PDF for Table 5.7 annual data (same 42 years)
3. Cross-check: S*/V* from H.1 should match Table 5.7's e column
4. Save as `Inputs/BookTables/ch05/TableH1_SurplusValue_1948_1989.csv` and `Inputs/BookTables/ch05/Table5_7_ACTUAL_KeyRatios.csv`
5. Update V_S_star_reconstructed.csv to use ALL 42 years instead of 8-point interpolation
6. Replace Table5_7_KeyRatios.csv reference in L03 with actual annual data
7. Run pipeline, verify V01 still passes with tighter reference values

**Files touched**:
- NEW: `Inputs/BookTables/ch05/TableH1_SurplusValue_1948_1989.csv`
- NEW: `Inputs/BookTables/ch05/Table5_7_ACTUAL_KeyRatios.csv`
- MODIFY: `code/loading/L02b_reconstruct_v_star.py` (use full H.1 data)
- MODIFY: `code/loading/L03_load_key_ratios.py` (read actual instead of interpolated)
- MODIFY: `data/final-data/book/series/V_S_star_reconstructed.csv`
- MODIFY: `validation_config.json` (add more reference years)

**Effort**: 2-3 hours
**Produces**: Correct annual book-period data for T504, T505, T506, T511, T512 (book columns). Eliminates the "linearly interpolated between benchmarks" data quality issue for 5 series.

**Dependency**: None (standalone)

---

### Step 2: Implement "Roughly Productive Sectors" BLS Adjustment

**Why second**: The KB revealed (Appendix I, chunk 35) that the book subtracts trade and FIRE workers from BLS production/nonsupervisory totals before computing hp and Lp. Our pipeline uses aggregate BLS CES without this adjustment. This affects T511, T512, T515, T516 extension accuracy.

**What**: Modify the employment extension logic to:
1. Start with BLS CES total private nonagricultural (CES0500000001)
2. Subtract CES trade workers (wholesale + retail)
3. Subtract CES FIRE workers
4. Result = "roughly productive sector" production workers
5. Apply this adjusted ratio to Table F.1 Lp for the extension splice

**Method**:
1. Identify BLS CES series IDs for trade and FIRE sectors
2. Check if these exist in our `Inputs/API_Data/BLS/` or need fetching
3. If not available: fetch via FRED (which mirrors BLS series) — no BLS API key needed
4. Create `L04b_load_bls_sector_employment.py` to parse sector-level CES data
5. Modify `P06_process_employment.py` to apply the trade+FIRE subtraction
6. Recompute T515, T516 with adjusted ratios
7. Verify total_scale drops closer to 1.0 (currently 1.307)

**Files touched**:
- NEW: `code/loading/L04b_load_bls_sector_employment.py`
- MODIFY: `code/processing/P06_process_employment.py`
- POSSIBLY: `Inputs/API_Data/BLS/` (new sector CES files)

**Effort**: 3-4 hours
**Produces**: More faithful T515 (Lp) and T516 (Lu) extension values. Reduced total_scale gap. Better foundation for T511/T512.

**Dependency**: None (standalone, but benefits from Step 1 for book-period cross-check)

---

### Step 3: V* Sector-by-Sector Calculation

**Why third**: The KB (Appendix G, chunk 33) documents three methodology gaps in how we compute V*: (a) no self-employed wage equivalent, (b) aggregate not sector-level BLS ratios, (c) no corporate officers' salary exclusion. Fixing these improves T504/T505/T506 extension faithfulness.

**What**: Refactor V* extension to follow the book's Appendix G procedure:
1. L = NIPA PEP (persons engaged in production) = FEE + SEP — include self-employed
2. Compute (ecp)j = BLS wp × (EC/WS)j per production sector
3. V* = Σ (ecp)j × (Lp)j for 7 production sectors
4. Exclude corporate officers' salaries (COS) from V*
5. Wu = W - V* (residual)

**Method**:
1. Fetch NIPA Table 6.5 (FTE employees by industry) and Table 6.10 (persons engaged, includes SEP)
2. Fetch NIPA Table 6.4 (EC by industry)
3. For each of the 7 production sectors: compute ec = EC/FEE, then W = ec × L
4. For production workers: use BLS CES sector wages × (EC/WS) adjustment
5. Compute V* = Σ (ecp)j × (Lp)j sector by sector
6. Compare with current aggregate approach; document magnitude of improvement

**Files touched**:
- NEW: `code/processing/P02b_sector_variable_capital.py`
- MODIFY: `code/processing/P02_process_variable_capital.py` (call P02b for extension)
- MODIFY: `code/manual/M01_adjust_va_star_ratio.py` (use sector V* if available)

**Effort**: 4-6 hours
**Produces**: T504 extension computed by the book's own methodology. Should improve T504 splice quality (currently CR=0.81). Cascades to T505, T506.

**Dependency**: Step 2 (needs sector-level BLS data)

---

### Step 4: NSW Methodology Upgrade (T601-T609)

**Why fourth**: The KB (Appendix N, chunk 38) revealed our T606 uses a fixed 40% defense exclusion, but the book uses a 3-group classification with time-varying labor share. This is the weakest link in Chapter 6.

**What**: Implement the book's exact NSW methodology from Appendix N:
1. Classify government expenditures into Groups I, II, III
2. Group I (income support, social security, welfare, housing, labor training): 100% to workers
3. Group II (education, health, recreation, energy, natural resources, transport, postal): × (labor income / personal income) annually
4. Group III (defense, international, space, civilian safety, veterans, agriculture, economic development): 0% to workers
5. For taxes: Group I (social security) at 100%, Group II (personal taxes, property, motor vehicle) at × labor share, exclude corporate/indirect/estate taxes
6. Recompute T605 (benefits) and T606 (govt services) from this classification
7. T607 = T605 + T606 - T604 from extended components

**Method**:
1. Identify NIPA tables for each expenditure category in Groups I-III
2. Load NIPA 2.1 for annual labor_income/personal_income ratio (already have this in L07)
3. Create `L08b_load_nsw_appendix_n.py` implementing the 3-group methodology
4. Compute benefits (B1), taxes (T1), net transfer (NT = B1 - T1) per Appendix N
5. Compare with current T605/T606/T607 values
6. If improvement significant: replace T605/T606 extension logic

**Files touched**:
- NEW: `code/loading/L08b_load_nsw_appendix_n.py`
- MODIFY: `code/loading/L08_load_benefits.py` (use new methodology for extension)
- MODIFY: `code/processing/P10_process_benefits.py`
- MODIFY: `code/processing/P11_process_nsw.py` (T607 from components)

**Effort**: 4-6 hours
**Produces**: More faithful T605, T606, T607 extension. Should reduce the NSW/GDP gap with Moos (currently 0.013 vs 0.011). Also fixes T608 (NSW/V*) which now has correct V* levels from DEC-020.

**Dependency**: Step 1 (for V* levels in T608 computation)

---

### Step 5: T702/T703 — Reproduce Ochoa's 1958 Regression

**Why fifth**: The most intellectually interesting open question. The book claims R² = 0.98 (from Ochoa 1984), but our A06 gets R² = 0.003-0.035 for NAICS era. The KB (Section 5.10, chunk 17) confirms the correct specification: regress log(market prices) on log(labor values) across sectors, NOT log(prices of production) on log(labor values).

**What**:
1. Run the correct regression on our existing 1958 SIC IO data (already in pipeline via L11)
2. Verify R² ≈ 0.98 for 1958 (the book's claim)
3. Run same regression on each SIC benchmark year (1947, 1963, 1967, 1972, 1977)
4. Run same regression on NAICS benchmark years (1997, 2002, 2007, 2012, 2017)
5. If SIC-era R² is high but NAICS-era R² is low: document as genuine empirical finding (financialization reduces price-value correspondence)
6. If SIC-era R² is also low: spec error in our code, debug

**Method**:
1. Modify `code/analysis/A06_labor_value_analysis.py` to use correct regression: log(p_j) on log(λ_j) where p_j = GO_j/L_j (market price proxy) and λ_j = labor value from T701
2. Compute λ* = hp* · (I - app*)^{-1} for each benchmark year
3. Market prices: use gross output per unit (GO_j from IO table) as proxy
4. Run OLS regression, report R², slope, intercept, number of sectors
5. Save results to `outputs/analysis/labor_value_price_deviations_corrected.json`

**Files touched**:
- MODIFY: `code/analysis/A06_labor_value_analysis.py`
- MODIFY: `data/final-data/book/series/T702_prices_of_production.json`
- MODIFY: `data/final-data/book/series/T703_value_price_deviations.json`

**Effort**: 3-4 hours
**Produces**: Resolves the R² crisis. Either confirms book's 0.98 (validating our IO computation) or identifies a real empirical finding about structural change. Upgrades T702/T703 documentation.

**Dependency**: None (uses existing IO matrices from L11/L11b)

---

### Step 6: T510 Definition Verification and Fix

**Why sixth**: The KB (Section 5.5, chunk 15) reveals the book's "value composition" C*/V* = K/V* (capital STOCK / variable capital flow), but our T510 source data is stored as ln(V*/C*) in the ExploitationComposition CSV, where the C* may be materials flow, not capital stock.

**What**:
1. Compute K/V* using BEA Fixed Assets (K, already available) and reconstructed V*
2. Compare with the decoded T510 values (exp(-x) from ExploitationComposition)
3. If they match: T510 is correct (it's K/V*)
4. If they don't match: identify what T510 actually is and correct it
5. Update series_registry.json with the correct definition

**Method**:
1. Load BEA Fixed Assets Table 4.1 (total private fixed assets at replacement cost)
2. Load reconstructed V* from V_S_star_reconstructed.csv
3. Compute K/V* for each book year
4. Compare with exp(-T510_value_composition) from ExploitationComposition CSV
5. Also compute M'p/V* from Table E.1 data to check the flow alternative

**Files touched**:
- POSSIBLY MODIFY: `code/loading/L05_load_composition.py`
- POSSIBLY MODIFY: `code/processing/P07_process_composition.py`
- MODIFY: `series_registry.json` (T510 definition field)

**Effort**: 1-2 hours
**Produces**: Confirmed definition for T510. Faithfulness upgrade from 55% to 75%+.

**Dependency**: Step 1 (needs correct V* for the K/V* computation)

---

### Step 7: Fetch CES0000000001 (Total Nonfarm Employment)

**Why seventh**: The book includes government workers in total employment L. Our BLS data uses CES0500000001 (total private only), creating the 1.307 total_scale gap. CES0000000001 (total nonfarm, includes government) should reduce this to ~1.08.

**What**:
1. Fetch CES0000000001 from FRED (PAYEMS series) — no BLS API key needed
2. Update P06 to use total nonfarm for the Lu = L - Lp computation
3. Verify total_scale drops from 1.307 to near 1.08
4. This also improves T511 extension (Lp/L denominator is now correct universe)

**Method**:
1. Add FRED PAYEMS to `api_config.json`
2. Fetch via existing FRED fetcher infrastructure
3. Modify P06 to prefer CES0000000001 over CES0500000001
4. Recompute T515, T516, verify total_scale

**Files touched**:
- MODIFY: `api_config.json`
- NEW or MODIFY: `code/loading/L04_load_employment.py` (add FRED fetch)
- MODIFY: `code/processing/P06_process_employment.py`

**Effort**: 1 hour
**Produces**: total_scale drops from 1.307 to ~1.08. More faithful T515/T516. Partially addresses T511/T512 UNJUSTIFIED.

**Dependency**: None (standalone). Synergizes with Step 2.

---

### Step 8: Parse NAICS IO Benchmark Tables (Full Wave 2 Foundation)

**Why eighth**: This is the foundation for fixing the last 2 UNJUSTIFIED series (T511/T512) and improving T502, T510, T513/T514. L11b already partially parses 5 NAICS benchmarks — this step completes the parsing with the book's sector classification applied.

**What**:
1. Validate existing L11b parsing for 5 NAICS years (1997, 2002, 2007, 2012, 2017)
2. Apply the book's productive sector classification (from Appendix F/chunk 33) to all ~71 NAICS industries
3. Compute for each benchmark year:
   - ratio_productive_output = GO_productive / GO_total
   - ratio_productive_employment = L_productive / L_total
   - ratio_productive_materials = M_productive / M_total
4. Bridge to SIC era: use existing 6 SIC benchmarks (1947-1977) with the book's 85-sector classification
5. Handle the 1978-1996 gap with the 1977 SIC and 1997 NAICS endpoints

**Method**:
1. Create `Inputs/Concordances/naics_productive_classification.csv` (71 sectors × {productive, trade, royalties})
2. Extend L11b to output annual interpolated ratios for all three types
3. Store in `data/final-data/book/series/IO_productive_ratios_full.csv`
4. Validate: productive output ratio should be 0.55-0.58 (matching L11b's existing output)

**Files touched**:
- NEW: `Inputs/Concordances/naics_productive_classification.csv`
- MODIFY: `code/loading/L11b_parse_naics_io.py` (add employment + materials ratios)
- MODIFY: `data/final-data/book/series/IO_productive_ratios.csv`

**Effort**: 4-6 hours
**Produces**: Complete IO productive sector ratio time series (1947-2017, interpolated annually). Foundation for Steps 9-12.

**Dependency**: None (builds on existing L11b)

---

### Step 9: Fix T502 (C*_m via IO Interpolation)

**Why ninth**: The book's methodology (Appendix E, chunk 31): C*_m[yr] = (Mp'/GVAp)[benchmark] × GVAp[yr]. Currently uses GDP growth-rate proxy (DEC-015).

**What**: Replace GDP proxy with IO benchmark interpolation for C*_m.

**Method**:
1. From Step 8: get annual Mp'/GVAp ratios (interpolated between benchmarks)
2. From BEA GDP-by-Industry: get annual GVAp (productive sector value added)
3. C*_m = ratio × GVAp for each year
4. Update P01 to use IO-interpolated C*_m instead of GDP growth-rate splice
5. T503 (GFP*) automatically corrected via identity enforcement (T501 - T502)

**Files touched**:
- MODIFY: `code/processing/P01_process_revenue.py` (use IO C*_m)

**Effort**: 2 hours
**Produces**: T502 upgraded from JUSTIFIED (GDP proxy) to MATCH (IO interpolation). T503 inherits improvement.

**Dependency**: Step 8

---

### Step 10: Fix T511/T512 from IO Employment Classification

**Why tenth**: The last 2 UNJUSTIFIED series. Requires IO productive employment ratios from Step 8.

**What**: Extend T511 (Lp/L) and T512 (V*/W) by separately extending numerators and denominators (Principle 3 compliance).

**Method**:
1. T511: Lp[yr] = L_total[yr] × ratio_productive_employment[yr] from Step 8
2. L_total from CES0000000001 (Step 7) or NIPA PEP
3. T511 = Lp / L for each year (Principle 3: ratio from separate components)
4. T512: V*[yr] = ecp[yr] × Lp[yr] where ecp from sector-level BLS (Step 3)
5. W[yr] from BEA total compensation
6. T512 = V* / W for each year
7. Deprecate Table5_7_Extended.csv

**Files touched**:
- MODIFY: `code/processing/P05_process_labor_shares.py`
- MODIFY: `code/loading/L03_load_key_ratios.py` (remove extended CSV dependency)
- DELETE: `Inputs/ST_Chopped/ch05/Table5_7_Extended.csv` (deprecated)

**Effort**: 3-4 hours
**Produces**: T511 and T512 upgraded from UNJUSTIFIED to JUSTIFIED or MATCH. UNJUSTIFIED count drops to 0. Table5_7_Extended.csv finally deprecated.

**Dependency**: Steps 7, 8 (needs IO employment ratios + total nonfarm employment)

---

### Step 11: Fix T513/T514 K* from IO-Restricted Fixed Assets

**Why eleventh**: Currently uses total K instead of productive-sector K*. The formula r* = S*/K is correct (DEC-017), but K should be restricted to productive sectors.

**What**: Apply IO sector classification to BEA Fixed Assets by industry to compute K*.

**Method**:
1. Download BEA Fixed Assets Table 4.1 by industry (may already be partially available)
2. Apply productive sector classification from Step 8
3. K*[yr] = Σ K_j for j ∈ productive sectors
4. r*[yr] = S*[yr] / K*[yr]
5. r*_adj[yr] = r*[yr] × (1/TCU[yr])
6. Compare with current total-K values

**Files touched**:
- MODIFY: `code/processing/P08_process_profit_rates.py`
- MODIFY: `code/loading/L06_load_profit_rates.py`

**Effort**: 2-3 hours
**Produces**: T513/T514 faithfulness upgraded from 70% to 85%+. Proper productive-sector profit rate.

**Dependency**: Step 8 (needs sector classification)

---

### Step 12: T510 Recompute from Components

**Why twelfth**: After Steps 1, 8, 9 correct T502 (C*_m) and V* levels, T510 = C*/V* can be properly recomputed from components instead of using the decoded log-encoded values or linear trend.

**What**: T510 = K/V* where K from BEA Fixed Assets and V* from reconstructed data.

**Method**:
1. If Step 6 confirmed T510 = K/V*: compute from BEA Fixed Assets / V*
2. If Step 6 found T510 = M'p/V* (flow): compute from IO-interpolated C*_m / V*
3. Either way: use real component data, not linear trend extrapolation

**Files touched**:
- MODIFY: `code/processing/P07_process_composition.py`
- MODIFY: `code/loading/L05_load_composition.py`

**Effort**: 1-2 hours
**Produces**: T510 faithfulness upgraded from 55% to 80%+.

**Dependency**: Steps 1, 6, 8, 9

---

### Step 13: SIC-NAICS Bridge (1978-1996)

**Why thirteenth**: The IO framework has a 19-year gap between the last SIC benchmark (1977) and first NAICS (1997). Simple linear interpolation of IO coefficients across this gap is the weakest link in the Wave 2 framework.

**What**: Obtain the 1992 BEA benchmark IO table (published in both SIC-compatible and NAICS-compatible format) to narrow the gap to 1978-1991 and 1993-1996.

**Method**:
1. Check BEA website for 1992 benchmark IO tables
2. If available: download, parse like other benchmarks
3. Create SIC→NAICS bridge using the dual-format 1992 data
4. Interpolation now: SIC 1977 → SIC 1992 → NAICS 1997 (two shorter gaps vs one long one)
5. Document the bridge methodology

**Files touched**:
- NEW: `Inputs/IO_Matrices/SIC/1992_A_matrix_sic.csv` (if available)
- MODIFY: `code/loading/L11b_parse_naics_io.py` (add 1992 bridge)

**Effort**: 2-3 hours
**Produces**: Smoother IO coefficient interpolation across the SIC-NAICS transition.

**Dependency**: Step 8

---

### Step 14: Full Re-Validation + Moos Shift Investigation

**Why fourteenth**: After all fixes, run comprehensive validation and investigate remaining calibration issues.

**What**:
1. Run full pipeline with all improvements
2. Run all 15 validators, document any new warnings
3. Investigate Moos structural shift: our +0.054 vs Moos's +0.030
4. Decompose: is the gap from NIPA vintage, from E2 exclusion, or from the labor share allocation method?
5. Update methodology review report with final verdicts

**Method**:
1. `python run.py --test-all`
2. For Moos: compute pre-2000 and post-2000 NSW/GDP means separately
3. Check NIPA revision impact on benefit series (2018 and 2023 comprehensive revisions)
4. Test E2 sensitivity: what shift does α=0.5 allocation produce?
5. Update ST2_METHODOLOGY_REVIEW_REPORT.md with all final verdicts

**Files touched**:
- MODIFY: `Technical/docs/ST2_METHODOLOGY_REVIEW_REPORT.md`
- MODIFY: `code/analysis/A03_moos_shift.py` (sensitivity analysis)

**Effort**: 2-3 hours
**Produces**: Final methodology review. Moos shift gap explained or documented.

**Dependency**: Steps 1-12

---

### Step 15: T201/T801 Wave 3 Implementation

**Why fifteenth**: The 2 UNKNOWN series. Low priority but needed for completeness.

**What**:
- T201 (Alternative GFP, Ch 2): Comparison table showing TP* ≈ 82% GP, TP* ≈ 1.5× GNP, GFP* ≈ 15% smaller than GNP. Content type: theoretical/cross-sectional, not time series.
- T801 (Cross-Study, Ch 8): Assembles Wolff/Mage/Gouverneur estimates alongside our own. Cross-reference table.

**Method**:
1. T201: Compute TP*/GP, TP*/GNP, GFP*/GNP for benchmark years from existing data
2. T801: Assemble from existing N-series (Mohun, Moos, Turkey, Cronin) + add Wolff/Mage from KB literature review data
3. Mark both as `content_type: "cross_sectional"` — no extension needed

**Files touched**:
- MODIFY: `code/loading/L14_load_alternative_gfp.py`
- MODIFY: `code/processing/P15_process_wave3.py`
- MODIFY: `series_registry.json` (T201, T801 status)

**Effort**: 2-3 hours
**Produces**: 0 UNKNOWN. All 59 series at MATCH or JUSTIFIED.

**Dependency**: Steps 1-12 (needs final series values)

---

### Step 16: Production Polish

**Why last**: Everything must be correct before polishing.

**What**:
1. Fresh-environment test: clone repo, install requirements, run `python run.py --test-all`
2. Generate LaTeX methodology report (PDF)
3. Update README.md with final statistics
4. Git commit + GitHub push
5. Final handoff documentation

**Method**:
1. Create a clean venv, pip install from requirements.txt, verify PASS
2. Write `Outputs/Reports/AS2_Methodology_Report.tex` compiling all findings
3. LaTeX → PDF
4. Stage all changes, commit, push

**Files touched**:
- MODIFY: `README.md`
- NEW: `Outputs/Reports/AS2_Methodology_Report.tex`
- NEW: `Outputs/Reports/AS2_Methodology_Report.pdf`
- MODIFY: `Technical/Handoffs/HANDOFF_YYYYMMDD_SESSIONXX.md`

**Effort**: 3-4 hours
**Produces**: Publication-ready deliverable package.

**Dependency**: All previous steps

---

## Dependency Graph

```
Step 1 (Table H.1 digitize) ───┬──> Step 6 (T510 verify)
                                ├──> Step 4 (NSW upgrade)
                                └──> Step 12 (T510 recompute)

Step 2 (BLS sector adjust) ────┬──> Step 3 (V* sector calc)
                                └──> Step 10 (T511/T512 fix)

Step 7 (CES0000000001) ────────┬──> Step 10 (T511/T512 fix)
                                └──> Step 2 (synergy)

Step 5 (T702/T703 regression) ─── standalone

Step 8 (IO framework) ─────────┬──> Step 9 (T502 C*_m)
                                ├──> Step 10 (T511/T512)
                                ├──> Step 11 (T513/T514 K*)
                                ├──> Step 12 (T510)
                                └──> Step 13 (SIC-NAICS bridge)

Steps 1-12 ────────────────────┬──> Step 14 (re-validation)
                                └──> Step 15 (Wave 3)

Step 14 + 15 ────────────────────> Step 16 (polish)
```

## Parallel Execution Opportunities

These steps can run simultaneously:
- **Step 1 + Step 5 + Step 7** (independent: PDF digitization, regression analysis, FRED fetch)
- **Step 2 + Step 8** (both fetch data, no overlap)
- **Step 3 + Step 4** (V* calc + NSW upgrade, independent after Step 2)
- **Step 9 + Step 10 + Step 11** (all depend on Step 8 but not on each other)
- **Step 15** can start alongside Step 14

## Effort Summary

| Phase | Steps | Hours | Sessions |
|-------|-------|-------|----------|
| Data foundation | 1, 7 | 3-4 | 1 |
| BLS/employment | 2, 3 | 7-10 | 2 |
| Chapter 6 + analysis | 4, 5, 6 | 8-12 | 2-3 |
| Wave 2 IO | 8, 9, 10, 11, 12, 13 | 14-20 | 3-5 |
| Validation + polish | 14, 15, 16 | 7-10 | 2-3 |
| **Total** | **16 steps** | **39-56** | **10-14** |

## Projected Scorecard After Each Phase

| After Phase | MATCH | JUSTIFIED | UNJUSTIFIED | UNKNOWN | Key Changes |
|------------|-------|-----------|-------------|---------|-------------|
| Current | 28 | 27 | 2 | 2 | — |
| Data foundation (1,7) | 28 | 27 | 2 | 2 | Better book data quality |
| BLS/employment (2,3) | 28 | 27 | 2 | 2 | T504-T506 faithfulness up |
| Chapter 6 + analysis (4,5,6) | 29 | 26 | 2 | 2 | T606 upgrade, T510 fix, T702/T703 resolved |
| Wave 2 IO (8-13) | 33 | 24 | **0** | 2 | T502, T511, T512, T513, T514 all upgraded |
| Wave 3 (14,15) | 33 | 24 | 0 | **0** | T201, T801 implemented |
| Polish (16) | 33 | 24 | 0 | 0 | Publication ready |

---

*Plan authored 2026-05-08. Based on KB deep dive (16/40 chunks, 10/12 questions resolved), unit audit (DEC-020 resolved), and 22 sessions of cumulative project knowledge.*
