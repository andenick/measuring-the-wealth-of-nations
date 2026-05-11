# ST2 Wave 2 Development Plan

**Date**: 2026-05-07
**Context**: Methodology review complete. 10 of 16 UNJUSTIFIED verdicts resolved by code fixes. 5 remain blocked on Wave 2 IO framework. Pipeline passes at 77 years extension (1948-2024) for core series.

**Current scorecard** (post all fixes):
- 27 MATCH | 22 JUSTIFIED_DEVIATION | 6 UNJUSTIFIED_DEVIATION | 2 UNKNOWN (Wave 3 deferred)
- The 6 UNJUSTIFIED are: T502, T510 (partial), T511, T512, T513, T514
- All are blocked on the IO framework except T510 (minor)

---

## What Wave 2 Unblocks

The IO framework (Phase B from Next Steps Plan) resolves ALL remaining methodology issues:

| Series | Current Issue | IO Framework Fix |
|--------|-------------|-----------------|
| T502 | GDP growth-rate proxy for C*_m | IO benchmark M'p/GVAp interpolation → annual C*_m |
| T511 | Ratio extended directly (Principle 3) | Extend Lp and L separately from IO classification |
| T512 | Same (derived from T511) | Extend V* and W separately, compute ratio |
| T513 | K (total stock) instead of C*+V* (flow) | Restrict BEA Fixed Assets to productive sectors via IO |
| T514 | Inherits T513 | Automatic once T513 fixed |
| T510 | Linear trend extrapolation | Compute C*/V* = T502/T504 from components |

---

## Phase B Implementation Plan (IO Framework)

### B1. Extend IO Matrix Coverage (1997-2017 NAICS era)

**Goal**: Load 5 additional BEA benchmark IO tables (1997, 2002, 2007, 2012, 2017) to complement existing SIC-era tables (1947-1977).

**Data source**: BEA "Use Tables" and "Make Tables" at detailed level (71 industries). Available at bea.gov/industry/input-output-accounts-data.

**Steps**:
1. Download BEA NAICS benchmark IO tables (use tables, before redefinitions) for 1997, 2002, 2007, 2012, 2017
2. Parse into A-matrix format (71×71 for NAICS era)
3. Store in `Inputs/IO_Matrices/` as `{year}_A_matrix_naics.csv`
4. Apply concordance (`io_85_to_nipa_13_concordance.csv`) or build NAICS equivalent
5. Compute Leontief inverse B = (I-A)^{-1} for each year
6. Validate: condition numbers, positive eigenvalues, row/column sums

**Key decision**: SIC (85 sectors, 1947-1977) vs NAICS (71 sectors, 1997-2017). Need a bridge methodology for 1978-1996 gap.

**Effort**: 4-6 hours (data download + parsing + validation)

### B2. Build Productive Sector Classification Engine

**Goal**: Classify each IO sector as productive (P) or unproductive (U) per Shaikh & Tonak's criteria, for every benchmark year.

**Implementation**:
1. Read book's Appendix B (KB chunk 27) for classification rules
2. Create `productive_classification_sic.csv` (85 sectors, already partially done in `naics_classification.py`)
3. Create `productive_classification_naics.csv` (71 sectors)
4. For each benchmark year: apply classification → productive output ratio, productive employment ratio, productive intermediate input ratio
5. Interpolate between benchmark years (linear, as documented in `INTERPOLATION_METHODOLOGY.md`)

**Output**: Annual time series (1947-2017) of:
- `ratio_productive_output[yr]` = GO_productive / GO_total
- `ratio_productive_employment[yr]` = L_productive / L_total  
- `ratio_productive_materials[yr]` = M_productive / M_total

**Effort**: 3-4 hours

### B3. Fix T502 (C*_m via IO interpolation)

**Book methodology** (pp.94-96): C*_m[yr] = (M'p/GVAp)[benchmark] × GVAp[yr], interpolated between benchmarks.

**Implementation**:
1. From each benchmark IO table: compute M'p (materials consumed by productive sectors) and GVAp (value added by productive sectors)
2. Compute ratio xp[yr] = M'p/GVAp at each benchmark
3. Linearly interpolate xp between benchmarks for annual values
4. Multiply by annual NIPA GVA_productive (from GDP-by-Industry)
5. Replace P01's GDP growth-rate extension for T502

**Effort**: 2 hours (after B1+B2)

### B4. Fix T511/T512 (Component Extension)

**Current**: T511 = Lp/L loaded from pre-extended CSV (piecewise linear interpolation).

**Correct approach**:
1. T511 = Lp/L where Lp = productive employment, L = total employment
2. Use IO classification ratios from B2: `Lp[yr] = L_total[yr] × ratio_productive_employment[yr]`
3. L_total from BLS total nonfarm (fetch CES0000000001)
4. Compute T511 = Lp/L for each year
5. T512 = V*/W: V* from T504 (now working), W from BEA total compensation
6. Replace Table5_7_Extended.csv dependency

**Effort**: 2 hours (after B2)

### B5. Fix T513/T514 (K* Denominator)

**Current**: Uses total private capital stock K from BEA Fixed Assets Table 4.1.
**Correct**: K* = productive-sector capital only.

**Implementation**:
1. Download BEA Fixed Assets Table 4.1 by industry (already partially available)
2. Apply IO productive sector classification to restrict to productive industries
3. K*[yr] = sum(K_j) for j ∈ productive sectors
4. r*[yr] = S*[yr] / K*[yr] (or S*/(C*+V*) if flow-based available from B3)
5. Replace current M02 K/K* scaling with direct K* computation

**Effort**: 2 hours (after B2)

---

## Pre-Wave 2: Quick Improvements (No IO dependency)

### Q1. Fetch BLS CES0000000001 (Total Nonfarm)

**Purpose**: Fix T516 total_scale from 1.307 to ~1.08 by using total nonfarm employment instead of total private.

**Steps**:
1. Add CES0000000001 to the BLS data fetch script
2. Update P06 to use total nonfarm for the Lu computation
3. Verify total_scale drops to near 1.0

**Effort**: 30 min

### Q2. Extend T601-T604 (Tax Series)

**Current**: Book-only (1952-1989). No extension attempted.
**Opportunity**: NIPA has all tax components:
- T601: NIPA 3.1 "Personal current taxes" × (EC/PI) for worker allocation
- T602: NIPA 3.7 "Contributions for government social insurance"
- T603: NIPA 3.5 "Taxes on production and imports" × consumption share

**Steps**:
1. Load NIPA 3.1, 3.5, 3.7 via BEA API
2. Apply book's allocation formulas to each component
3. Compute T604 = T601 + T602 + T603 (identity by construction)
4. Growth-rate splice at 1989

**Effort**: 2-3 hours
**Impact**: Extends NSW computation (T607) to full 1952-2025 from real components instead of pre-computed table

### Q3. T510 Extension via BEA Intermediate Inputs

**Current**: Linear trend extrapolation on decoded book values.
**Better**: Even without full IO framework, BEA GDP-by-Industry has "intermediate inputs" by industry. Use the ratio of productive-sector intermediate inputs to productive wages as a proxy for C*/V*.

**Steps**:
1. Check if NAICS_marxian_aggregates.csv (used by P01 for TV*) also has intermediate input data
2. If available: compute C*_proxy = intermediate_productive, V*_proxy = compensation_productive
3. T510_ext = C*_proxy / V*_proxy for 1997+
4. Bridge 1990-1996 with linear interpolation from book end to 1997 start

**Effort**: 1-2 hours (if data available in existing files)

### Q4. Add V05 Identity Checks

**Currently missing identity checks that should be added to V05_cross_series.py**:
1. T501 = T502 + T503 (all years)
2. T503 = T504 + T505 (book years only — different unit systems)
3. T506 = T505 / T504 (all years)
4. T604 = T601 + T602 + T603 (book years)
5. T607 = T605 + T606 - T604 (needs investigation — may not hold due to book's pre-computation)

**Effort**: 1 hour

### Q5. Update Review Report to Final State

The methodology review report still has many series listed as UNJUSTIFIED that are now fixed. Update all verdicts to reflect actual current state.

**Effort**: 15 min

---

## Development Priority

```
Immediate (this session or next):
  Q5. Update review report verdicts (15 min)
  Q1. Fetch CES0000000001 for T516 (30 min)
  Q4. Add V05 identity checks (1 hr)

Near-term (1-2 sessions):
  Q2. Extend T601-T604 taxes (2-3 hr)
  Q3. T510 BEA proxy extension (1-2 hr)

Wave 2 (dedicated campaign, 3-5 sessions):
  B1. Download + parse NAICS IO tables (4-6 hr)
  B2. Productive sector classification engine (3-4 hr)
  B3. T502 C*_m via IO interpolation (2 hr)
  B4. T511/T512 component extension (2 hr)
  B5. T513/T514 K* denominator (2 hr)
```

**Total Wave 2 effort**: ~15-20 hours across 3-5 sessions.

---

## Impact Projections

| Milestone | MATCH | JUSTIFIED | UNJUSTIFIED | Score |
|-----------|-------|-----------|-------------|-------|
| Current (post-fixes) | 27 | 22 | 6 | ~83% |
| After Q-series | 28 | 23 | 4 | ~86% |
| After Wave 2 B1-B5 | 32 | 25 | 0 | ~97% |

---

## Data Requirements

### BEA Data to Download (Wave 2)
- IO Use Tables (before redefinitions): 1997, 2002, 2007, 2012, 2017
- Fixed Assets Table 4.1 by industry (for K*)
- GDP-by-Industry: intermediate inputs by industry (for C*_m)

### BLS Data to Fetch (Pre-Wave 2)
- CES0000000001 (total nonfarm employment, all employees)

### Existing Data Already Sufficient For
- Q2 tax extension (NIPA 3.1, 3.5, 3.7 — check if already in Inputs/API_Data/BEA/)
- Q3 T510 proxy (NAICS_marxian_aggregates.csv intermediate inputs — check availability)

---

*Plan authored 2026-05-07 following methodology review implementation and investigation rounds.*
