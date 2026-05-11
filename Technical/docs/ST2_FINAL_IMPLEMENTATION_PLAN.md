# ST2 Final Implementation Plan — 98% to 100%

**Date**: 2026-05-08
**Baseline**: Pipeline PASS, 60 series, 0 UNJUSTIFIED, 0 UNKNOWN, 98% Druck completion
**Target**: All remaining methodology gaps closed, all data from real sources, no fabricated artifacts

---

## Step A: V* Sector-by-Sector Calculation

**Why**: The book (Appendix G, chunk 33) computes V* = Σ (ecp)j × (Lp)j across 7 production sectors. Our pipeline uses aggregate BLS production workers × average compensation. The sector-level approach captures wage differentials between sectors and excludes corporate officers' salaries (following Mage 1963).

**Inputs already available**:
- NIPA 6.2D: `nipa_6_2D_compensation_by_industry.csv` (EC by industry, already used by M01)
- NIPA 6.5D: `nipa_6_5D_fte_by_industry.csv` (FTE by industry, loaded but not fully parsed)
- BLS CES: `bls_ces_production_workers.csv` (production worker counts by sector: mining, construction, manufacturing)
- FRED sector employment: `sector_employment.csv` (trade, FIRE, government totals)

**Implementation**:

```
1. Create code/processing/P02b_sector_variable_capital.py

2. Load NIPA 6.2D compensation by industry:
   - Parse line descriptions to identify 7 production sectors:
     agriculture, mining, construction, manufacturing,
     transport+utilities, productive_services, govt_enterprises
   - Extract EC_j for each sector and year (1998-2024)

3. Load NIPA 6.5D FTE by industry:
   - Same sector mapping
   - Extract FEE_j for each sector and year
   - Compute ec_j = EC_j / FEE_j (compensation per FTE)

4. Load BLS CES production worker data by sector:
   - CES1000000006 (mining prod workers)
   - CES2000000006 (construction prod workers)
   - CES3000000006 (manufacturing prod workers)
   - For services: use NIPA sector ec_j directly (book's method)

5. Compute V* per sector:
   - For mining/construction/manufacturing:
     (ecp)_j = BLS_wage_j × (EC_j / WS_j)  [supplements adjustment]
     V*_j = (ecp)_j × (Lp)_j
   - For services:
     (ecp)_serv = ec_serv (average for sector)
     V*_serv = ec_serv × (Lp)_serv
   - For agriculture, transport, govt enterprises:
     Use sector-level ec_j × (Lp)_j from NIPA data

6. Total V* = Σ V*_j across all 7 production sectors

7. Compare with current aggregate V* (from P02):
   - If difference < 5%: use sector V* as primary, document improvement
   - If difference > 5%: investigate, ensure splice quality at 1989
```

**Files**:
- NEW: `code/processing/P02b_sector_variable_capital.py`
- MODIFY: `code/processing/P02_process_variable_capital.py` (call P02b if available)

**Effort**: 4-6 hours
**Produces**: Faithful Appendix G V* for extension period. Improves T504, T505, T506 extension accuracy.

---

## Step B: NIPA 6.5 Industry-to-IO Sector Mapping

**Why**: L11b computes ratio_productive_employment by falling back to the output ratio because the NIPA 6.5 FTE data can't be matched to IO sector codes. This mapping is needed for Steps A and C.

**Implementation**:

```
1. Read NIPA 6.5D CSV, extract unique LineDescription values

2. Create mapping dict: NIPA_description -> IO_classification
   Examples:
     "Farms" -> productive
     "Mining" -> productive
     "Utilities" -> productive
     "Construction" -> productive
     "Manufacturing" -> productive
     "Wholesale trade" -> trading
     "Retail trade" -> trading
     "Transportation and warehousing" -> productive
     "Finance, insurance, real estate" -> unproductive
     "Professional and business services" -> unproductive
     "Educational services, health care" -> productive
     "Arts, entertainment, recreation, accommodation" -> productive
     "Other services, except government" -> productive
     "Government" -> government

3. Save as Inputs/Concordances/nipa_65_to_io_classification.json

4. Update L11b to use this mapping:
   - For each benchmark year: sum FTE by classification
   - Compute ratio_productive_employment = FTE_productive / FTE_total
   - This replaces the output ratio fallback

5. Verify: productive employment share should be ~0.40-0.45
   (lower than output share ~0.55 because services have many workers per $ output)
```

**Files**:
- NEW: `Inputs/Concordances/nipa_65_to_io_classification.json` (write to Technical/ if Inputs/ blocked)
- MODIFY: `code/loading/L11b_parse_naics_io.py` (proper employment ratio)

**Effort**: 2 hours
**Produces**: Correct ratio_productive_employment for IO framework. Better T511 extension.

---

## Step C: T512 IO-Extension + Deprecate Table5_7_Extended.csv

**Why**: T511 is now IO-extended, but T512 (V*/W) still reads from Table5_7_Extended.csv — the fabricated piecewise-linear file created in Session 5. With sector-level V* from Step A and total W from BEA, T512 can be computed from components (Principle 3 compliant).

**Implementation**:

```
1. In P05 (or a new P05b):
   - Load V* extension from P02/P02b output (T504 combined, billions)
   - Load W (total compensation) from BEA NIPA T20100 or 6.2D aggregate
   - Compute T512_ext = V*_ext / W_ext for each year 1990-2024

2. For 1990-1997 (gap before BEA industry data):
   - Use M01-adjusted T512 values (log-linear interpolation between
     book 1989 value and first computed 1998+ value)

3. Combine: T512 = book (1948-1989) + interpolated (1990-1997) + computed (1998-2024)

4. Verify T512 values are reasonable (should decline from ~0.36 in 1989
   toward ~0.24-0.28 in 2024, per the declining productive wage share)

5. Remove Table5_7_Extended.csv from pipeline:
   - L03: remove EXT_COLS references for T511 and T512
   - P05: remove fallback to ext_parsed for T512
   - Mark Table5_7_Extended.csv as DEPRECATED in Inputs/

6. Update series_registry.json: T512 construction steps to reflect
   component-based extension
```

**Dependency**: Step A (V* sector calculation provides the numerator)

**Files**:
- MODIFY: `code/processing/P05_process_labor_shares.py` (T512 from V*/W components)
- MODIFY: `code/loading/L03_load_key_ratios.py` (remove extended CSV dependency)
- MODIFY: `series_registry.json` (T512 construction)

**Effort**: 2 hours
**Produces**: T512 Principle 3 compliant. Table5_7_Extended.csv deprecated. Both T511 and T512 now derived from separately extended components.

---

## Step D: BEA Fixed Assets by Industry

**Why**: T513/T514 (profit rate) use total K instead of productive-sector K*. T510 (value composition K/V*) extension needs K by year. Both require industry-level fixed assets.

**Implementation**:

```
1. Fetch BEA Fixed Assets Table 4.1 by industry:
   - API: BEA FixedAssets dataset, TableName=FAAt401
   - Parameters: industry-level detail (not just aggregate)
   - Cache to Inputs/API_Data/BEA/fixed_assets_4_1_by_industry.csv

2. Parse industry classifications:
   - Map BEA industry codes to productive/trading/royalties
   - Use same classification as L11b NAICS CLASSIFICATION dict

3. Compute K* = Σ K_j for j ∈ productive sectors, each year

4. Compute K*_by_year for 1948-2024 (BEA Fixed Assets covers 1925+)

5. Update P08_process_profit_rates.py:
   - r* = S* / K* (using productive K* instead of total K)
   - r*_adj = r* × (1/TCU)

6. Update P07_process_composition.py:
   - T510_ext = K* / V* for extension years (using K* and reconstructed V*)
   - Replaces the linear trend extrapolation on decoded book values

7. Validate: r* should be HIGHER than current (since K* < K)
   Typical productive share of fixed assets: ~60-70%
   So r* would increase by roughly 1/0.65 ≈ 1.5x
```

**Files**:
- NEW: `code/loading/L06b_fetch_fixed_assets_industry.py`
- MODIFY: `code/processing/P08_process_profit_rates.py` (K* instead of K)
- MODIFY: `code/processing/P07_process_composition.py` (T510 extension)
- MODIFY: `code/loading/L06_load_profit_rates.py` (load K* data)

**Effort**: 3-4 hours
**Produces**: Productive-sector K* for T513/T514. T510 extended from components. T513/T514 faithfulness → 85%+.

---

## Step E: 1992 IO Benchmark for SIC-NAICS Bridge

**Why**: The IO framework has a 19-year gap (1978-1996). The 1992 BEA benchmark was published in both SIC and NAICS-compatible formats, providing a bridge point that narrows the gap to two shorter segments.

**Implementation**:

```
1. Check BEA website for 1992 benchmark IO tables:
   - Look for "1992 Input-Output" in BEA Industry section
   - May be in the "Historical" or "Supplemental" IO data
   - Format: likely Excel or CSV, not JSON (pre-API era)

2. If available:
   - Download Use table and Total Requirements table
   - Parse into same format as NAICS benchmarks
   - Apply productive sector classification
   - Compute productive ratios at 1992

3. Update L11b interpolation:
   - SIC era: 1947, 1958, 1963, 1967, 1972, 1977, [1992]
   - NAICS era: [1992], 1997, 2002, 2007, 2012, 2017
   - 1992 serves as bridge between the two classification systems

4. The 1992 benchmark helps verify:
   - Whether productive output/employment ratios shifted during 1978-1996
   - Whether the linear interpolation across the gap was reasonable

5. If NOT available at BEA:
   - Document as attempted, maintain current approach
   - The existing GDP proxy for 1978-1996 is already documented in DEC-015
```

**Files**:
- NEW: `Inputs/IO_Matrices/SIC/1992_Use_table.csv` (if available)
- MODIFY: `code/loading/L11b_parse_naics_io.py` (add 1992 bridge)
- NEW or MODIFY: `Inputs/Concordances/sic_naics_bridge_1992.csv`

**Effort**: 2-3 hours
**Produces**: Narrower interpolation gap. Better IO coefficient estimates for 1978-1996.

---

## Step F: T201 Unit Fix

**Why**: T201 (Alternative GFP) has GDP in raw NIPA units (~10^11) while GFP is in pipeline billions. The ratio GFP/GDP = ~10^-10 instead of ~0.82. Trivial fix.

**Implementation**:

```
1. In P15_process_wave3.py (or wherever T201 is assembled):
   - Find where GDP is loaded
   - Add: GDP = GDP / 1e9 (convert to billions)
   - Or: adjust the ratio formula to account for units

2. Verify: GFP/GDP should be ~0.82 (per book Ch 2)
   TP*/GNP should be ~1.5
   GFP*/GNP should be ~0.85
```

**Files**:
- MODIFY: `code/processing/P15_process_wave3.py`

**Effort**: 15 minutes
**Produces**: Correct T201 ratios. Cosmetic but eliminates a data quality issue.

---

## Step G: Fresh-Environment Test

**Why**: Last clean-env test was Session 20 before all Sessions 21-23 changes. Need to verify everything works from scratch.

**Implementation**:

```
1. Create temporary clean venv:
   python -m venv /tmp/st2_test_env
   source /tmp/st2_test_env/bin/activate  (or Windows equivalent)
   pip install -r requirements.txt

2. Copy api_keys.env to data/user-inputs/

3. Run: python run.py --test-all

4. Expected: PASS, ~33s, 60 series, 15 validators, 0 failures

5. If fails: diagnose, fix, re-test

6. Document: "Fresh-env test: PASS, date, Python version, OS"
```

**Effort**: 30 minutes
**Produces**: Confirmed reproducibility.

---

## Execution Order

```
Step F (T201 fix, 15 min) ── standalone, trivial
Step B (NIPA 6.5 mapping, 2 hr) ── foundation for A and C
Step A (V* sector calc, 4-6 hr) ── depends on B
Step C (T512 IO + deprecate CSV, 2 hr) ── depends on A
Step D (Fixed Assets by industry, 3-4 hr) ── standalone
Step E (1992 IO benchmark, 2-3 hr) ── standalone
Step G (Fresh-env test, 30 min) ── after all above
```

**Parallel opportunities**:
- F + B can run simultaneously
- D + E can run simultaneously (both are data fetches)
- A must follow B
- C must follow A
- G must be last

## Total Effort: 14-19 hours across 3-4 sessions

## Projected Outcome

After all steps:
- V* computed by book's exact Appendix G methodology (sector-by-sector)
- T512 = V*/W from separately extended components (Principle 3)
- Table5_7_Extended.csv fully deprecated
- K* from productive-sector Fixed Assets (not total K)
- T510 extended from K*/V* components (not linear trend)
- IO framework with proper employment ratios and 1992 bridge point
- T201 unit-correct
- Fresh-env tested

**Druck completion**: 100%
**Methodology verdicts**: 28+ MATCH / 29+ JUSTIFIED / 0 UNJUSTIFIED / 0 UNKNOWN
**All series derived from real data sources with documented provenance**

---

*Plan authored 2026-05-08 (Session 23). All dependencies verified against current pipeline state.*
