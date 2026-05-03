# AS2 Master Roadmap
## All Next Steps — Post-Infrastructure Upgrade (v3.0)

**Created**: 2026-04-08 (Session 15)
**Supersedes**: ST2_NEXT_STEPS_PLAN.md (Phase A now complete)
**Current State**: Wave 1 = 93% (26/26 series), Infrastructure v3.0, Wave 2/3 = 0%

---

## Phase 1: Validation Tuning & ADJ-002 (Immediate — 1 session)

The V## validation suite runs but produces 12 FAILs and 11 WARNs that need triage and tuning before the results become a trusted baseline.

### 1.1 Fix V04 Completeness — T901 Start Year
- **Problem**: V04 assumes all series start at 1948, but T901 starts at 1952 (depends on Ch6 NSW data)
- **Fix**: Read `year_range` from series_registry.json for each series; use `exp_start` instead of hardcoded `CORE_START` when checking for missing years
- **File**: `scripts/validation/V04_completeness.py`
- **Effort**: 15 minutes
- **Expected result**: T901 FAIL → PASS

### 1.2 Fix V02 Range Checks — Per-Series Overrides
- **Problem**: T201.FP_star is negative by construction (FP* = GDP - TP*); dollar_series bounds don't cover raw-dollar values (T201 uses raw dollars, not billions)
- **Fix**: Add T201 to `series_overrides` in validation_config.json with custom range, or create a new `raw_dollar_series` type. Also add T505, T508, T509 which are large dollar values
- **File**: `config/validation_config.json`
- **Effort**: 30 minutes
- **Expected result**: 9 T201/T505/T508/T509 FAILs → PASS

### 1.3 Tune V01 Reference Values — T511/T512 Benchmarks
- **Problem**: T511 and T512 reference values in validation_config.json are approximate (rounded from book tables). Actual computed values differ by 2-9%.
- **Options**:
  - A) Widen tolerance for share_series to 10% relative (reflects book rounding)
  - B) Update reference values to match actual computed values (requires verifying against book Table 5.7)
  - C) Accept as WARN instead of FAIL (change threshold logic)
- **Recommendation**: Option B — read the DPRs for T511/T512 to extract exact book values, update validation_config.json
- **Files**: `config/validation_config.json`, `Technical/docs/series/T511_DPR.md`, `Technical/docs/series/T512_DPR.md`
- **Effort**: 1 hour

### 1.4 Tune V05 Cross-Series — Extension Period Exclusion
- **Problem**: S*=TP*-V* and e=S*/V* identities fail at 77-100% rate because T501/T503 are book-period only (1948-1989) while T504/T505 are extended to 2024. The identity is mathematically broken outside the book period by design.
- **Fix**: Restrict V05 checks to the core book period (1948-1989) or to years where ALL component series have data. Add `core_period_only: true` option to cross-series checks.
- **File**: `scripts/validation/V05_cross_series.py`
- **Effort**: 30 minutes
- **Expected result**: Both identity FAILs → PASS (for book period), with a note that extension period is structurally incomplete

### 1.5 Execute ADJ-002 — Year-Varying VA*/W
- **Problem**: Extension period for T504-T506, T512 uses constant VA*/W=1.238 instead of year-varying ec_u/ec_p ratio
- **Status**: READY in ADJUSTMENT_MANIFEST.json; `marxian_accounts.py` already supports year-varying input
- **Steps**:
  1. Create `scripts/manual/M01_adjust_va_star_ratio.py` — regenerates T504, T505, T506, T512 using year-varying ratio
  2. Run `replicate.py --full` to execute L→P→V→M pipeline
  3. Compare adjusted vs original series; verify benchmark years still match
  4. Update ADJUSTMENT_MANIFEST.json with execution results
  5. Regenerate chopped CSVs and extenbooks for affected series
- **Files**: New `M01_adjust_va_star_ratio.py`, modified `ADJUSTMENT_MANIFEST.json`
- **Effort**: 2-3 hours
- **Impact**: DIV-002 fully resolved; T504-T506, T512 extension accuracy improved

### 1.6 Run Full Pipeline Verification
- **Command**: `python replicate.py` (L+P+V, no --full yet)
- **Expected**: All L## and P## pass (as before); V## shows improved results after tuning
- **Update**: CHECKLIST.md last unchecked item

### Phase 1 Exit Criteria
- [ ] V## validation: 0 FAIL (all legitimate issues resolved or reclassified)
- [ ] ADJ-002 executed and verified
- [ ] Full pipeline run successful
- [ ] VALIDATION_REPORT.json shows clean baseline

---

## Phase 2: Wave 1 Documentation Completion (1 session)

Wave 1 data is complete but documentation has gaps that suppress the quality score.

### 2.1 Create Ch6 EPRs (T601-T609)
- **Problem**: Chapter 6 has 0 EPRs despite all 9 series being extended. This is the single largest score suppressor.
- **Task**: Write 9 EPRs following the Anu Extension v3.0 template:
  - T601_EPR.md — Personal tax extension (NIPA 2.1, 1990-2025)
  - T602_EPR.md — Social insurance tax extension
  - T603_EPR.md — Property tax extension
  - T604_EPR.md — Total tax extension
  - T605_EPR.md — Total benefits extension (NIPA 3.1, welfare reform bridge)
  - T606_EPR.md — Government services extension
  - T607_EPR.md — NSW extension (interpolation + BLS)
  - T608_EPR.md — NSW/V* ratio extension (derived from T607/T504)
  - T609_EPR.md — NSW/NI extension
- **Template**: Follow existing T511_EPR.md or T504_EPR.md format
- **Location**: `Technical/docs/series/`
- **Effort**: 3-4 hours (9 EPRs, each ~2-3 pages)
- **Score Impact**: Ch6 92% → ~96%

### 2.2 Complete Missing Ch5 DPRs
- **Problem**: Gap analysis shows only 4/16 Ch5 DPRs were fully written in early sessions. Sessions 4-6 created remaining DPRs but they may need quality review.
- **Task**: Audit all 16 Ch5 DPRs for completeness against DPR template (subsources, transformation chain, validation, known issues)
- **Effort**: 2 hours (audit + fix gaps)

### 2.3 Add Benchmark Values to validation_config.json
- **Problem**: Only T506, T511, T512 have benchmark_validation entries. The remaining 23 Wave 1 series have no reference value checks.
- **Task**: Extract reference values from DPRs and book tables for all 26 series. At minimum, add 1948 and 1989 benchmarks for each.
- **File**: `config/validation_config.json`
- **Effort**: 2-3 hours
- **Impact**: V01 becomes comprehensive (currently checks only 3 of 26 series)

### 2.4 Run Anu Review v4.1
- **Task**: Run `/anu-review` on all three chapters with the updated infrastructure
- **Expected**: Ch5 93%→95%, Ch6 92%→96%, Ch9 94%→95%, Project 93%→95%
- **Effort**: 1 hour

### Phase 2 Exit Criteria
- [ ] All 9 Ch6 EPRs written
- [ ] All 16 Ch5 DPRs audited and complete
- [ ] 26/26 series have benchmark_validation entries
- [ ] Anu Review v4.1: project score ≥ 95% (EXEMPLARY)

---

## Phase 3: IO Matrix Sourcing (1-2 sessions — CRITICAL PATH)

This is the primary blocker for all Wave 2 work. Without post-1977 IO matrices, Chapters 4, 7, and the remaining Chapter 5 extensions cannot proceed.

### 3.1 Source Post-1977 BEA Benchmark IO Tables

**Available sources by era**:

| Period | Years | Classification | Source | Difficulty |
|--------|-------|---------------|--------|------------|
| 1982-1992 | 1982, 1987, 1992 | SIC | BEA Historical IO Archive | HIGH — may require NBER or archived CDs |
| 1997 | 1997 | Dual (SIC+NAICS) | BEA "Bridge" tables | MEDIUM — published but needs manual extraction |
| 2002-2017 | 2002, 2007, 2012, 2017 | NAICS | BEA Interactive Tables (bea.gov) | LOW — readily downloadable |

**Strategy**:
1. Start with 2002-2017 NAICS tables (easiest to acquire)
2. Download 1997 bridge table (BEA website, historical section)
3. Research 1982-1992 SIC tables:
   - Check BEA historical archives at bea.gov
   - Check NBER data repository
   - Check Shaikh's own data sources (cited in book appendix)
   - Check academic replication packages (Mohun 2005, Ochoa 1984)
   - If unavailable: interpolate between 1977 and 1997 using annual Make/Use tables

### 3.2 Build SIC-NAICS Concordance Pipeline
- **Task**: Operationalize the concordance at `Inputs/Concordances/` for bridging SIC (1947-1996) and NAICS (1997+) sector classifications
- **Existing**: `io_85_to_nipa_13_concordance.csv` (85 IO sectors to 13 NIPA sectors)
- **Needed**: Full SIC-to-NAICS mapping at the IO detail level (400+ sectors)
- **Approach**: Use Census Bureau official crosswalk + manual review for many-to-many mappings
- **File**: New `Inputs/Concordances/sic_naics_io_concordance.csv`
- **Effort**: 4-6 hours

### 3.3 Process New IO Matrices
- **Task**: For each newly acquired matrix year:
  1. Convert to standard format (85x85 or equivalent)
  2. Compute A-matrix (technical coefficients)
  3. Compute L-matrix (Leontief inverse)
  4. Compute Z-matrix (direct labor inputs)
  5. Save to `Inputs/IO_Matrices/{year}_A_matrix.csv`, `{year}_L_matrix.csv`, `{year}_Z_matrix.csv`
- **Scripts**: L11_load_io_matrices.py already handles multi-year loading; P13_process_io.py validates
- **Effort**: 2-3 hours per era (SIC vs NAICS need separate processing)

### Phase 3 Exit Criteria
- [ ] At minimum 3 post-1977 IO benchmark years acquired (ideally 1997 + 2 NAICS years)
- [ ] SIC-NAICS concordance operational
- [ ] All new matrices pass P13 Leontief validation (eigenvalue check, row-sum check)
- [ ] L11 and P13 updated to handle new years

---

## Phase 4: Wave 2 — Chapter 4 IO Framework (1-2 sessions)

### 4.1 Complete Chapter 4 Investigation
- **Current**: CHAPTER_4_INVESTIGATION.md at ~80%
- **Remaining**: Expand narrative on productive/unproductive sector classification methodology, document how Shaikh & Tonak apply Marx's distinction to IO sectors
- **Effort**: 2 hours

### 4.2 Build Sector Classification Engine
- **Task**: Implement the productive/unproductive/trading sector classification for all benchmark years
- **Approach**: 
  - For SIC era (1947-1996): Use book's Appendix C classification (75 productive, 7 unproductive, 3 trading)
  - For NAICS era (1997+): Map via concordance, then manually verify boundary sectors (FIRE, government, real estate)
- **Scripts**: Extend `lib/transforms/io_transforms.py::classify_sectors()`
- **Output**: `Technical/sector_classifications/{year}_classification.json` for each benchmark year
- **Effort**: 4-6 hours

### 4.3 Build T401/T402 Full Pipeline
- **Task**: Complete T401 (A-matrix) and T402 (Leontief inverse) as proper Anu Suite series:
  - Create T401_DPR.md, T402_DPR.md
  - Create T401_DECOMPOSITION.md, T402_DECOMPOSITION.md
  - Create T401_research.json, T402_research.json
  - Verify L11 and P13 produce complete outputs
  - Generate chopped CSVs and extenbooks
- **Note**: T401/T402 are multi-year matrix series (not time series) — special handling needed
- **Effort**: 4-6 hours

### 4.4 Resolve DIV-001 — Productive Capital Stock K*
- **Task**: Restrict BEA Fixed Assets Table 4.1 capital stock to productive sectors using IO classification
- **Steps**:
  1. Map Fixed Assets industry categories to IO sector classification
  2. Sum only productive-sector capital stock for each year
  3. Recompute T513 (r* = S*/(C*+V*)) and T514 (r*adj) using K* instead of K
  4. Create M02_adjust_profit_rates.py
  5. Validate against book Table 5.11 benchmarks
  6. Update DIVERGENCE_REGISTER.json (DIV-001 → resolved)
  7. Update ADJUSTMENT_MANIFEST.json (ADJ-001 → completed)
- **Effort**: 6-8 hours
- **Impact**: T513/T514 profit rate levels should match book values within 5%

### Phase 4 Exit Criteria
- [ ] Chapter 4 investigation complete (100%)
- [ ] Sector classification operational for all available benchmark years
- [ ] T401/T402 have DPRs, decompositions, and pass validation
- [ ] DIV-001 resolved; T513/T514 profit rates match book benchmarks
- [ ] ADJ-001 executed and verified

---

## Phase 5: Wave 2 — Series Extension (1-2 sessions)

### 5.1 Extend T501-T503 (Revenue Accounts)
- **Current**: Book period only (1948-1989); extension starts 1997 via BEA NIPA 1.7.5 (SIC-NAICS gap: 1990-1996)
- **Task**:
  - For 1990-1996: Interpolate using growth rates from aggregate NIPA GDP/GO data
  - For 1997-2024: Use BEA Gross Output by Industry (NAICS) with sector classification from Phase 4
  - Apply Marxian category mapping: productive GO + trading GO = TP*, etc.
  - Create T501_EPR.md, T502_EPR.md, T503_EPR.md
- **Dependencies**: Phase 4 (sector classification)
- **Effort**: 6-8 hours

### 5.2 Extend T507-T510 (Composition Ratios)
- **Current**: Book period only (1948-1989)
- **Task**: Derive from extended T501-T506 (composition ratios are derived, not independently sourced)
  - T507 = S*/(S*+V*) (surplus ratio)
  - T510 = C*/V* (value composition of capital)
- **Dependencies**: 5.1 (T501-T505 must be extended first)
- **Effort**: 2-3 hours

### 5.3 Fix Cross-Series Identities
- **Task**: After T501-T503 extension, re-run V05 to verify:
  - T505 = T501 - T504 (now should pass for all years)
  - T506 = T505 / T504 (now should pass for all years)
- **Expected**: V05 cross-series checks move from FAIL to PASS

### 5.4 Build Chapter 7 Labor Values (T701-T703)
- **Task**: Implement labor value computation from IO framework:
  - T701: Labor values lv* = hp* @ B (direct labor × Leontief inverse)
  - T702: Prices of production (equalized profit rates across sectors)
  - T703: Value-price deviations (regression analysis)
- **Dependencies**: Phase 4 (IO matrices + sector classification)
- **Scripts**: L12_load_labor_values.py and P14_process_labor_values.py (stubs exist)
- **Effort**: 8-12 hours (methodologically complex)

### 5.5 Build Chapter 8 Cross-Study Comparison (T801)
- **Task**: Compare AS2 results with:
  - Mohun (2005) — different productive labor classification
  - Moos (2021) — updated methodology
  - Tonak benchmark files (if extractable from DOCX)
- **Dependencies**: 5.1-5.4 (need complete Wave 2 series for meaningful comparison)
- **Scripts**: L13_load_comparison.py and P15_process_comparison.py (stubs exist)
- **Effort**: 4-6 hours

### Phase 5 Exit Criteria
- [ ] T501-T503 extended to 2024
- [ ] T507-T510 extended (derived from T501-T506)
- [ ] V05 cross-series identities pass for full period
- [ ] T701-T703 computed for all available benchmark years
- [ ] T801 comparison matrix populated
- [ ] All 7 new series have DPRs and EPRs
- [ ] 33/33 series complete

---

## Phase 6: Wave 3 & Final Integration (1 session)

### 6.1 T201 Alternative GFP Measures
- **Task**: Complete the alternative Gross Final Product measures comparing Marxian GFP with orthodox GDP
- **Current**: Stub exists (L14, P15); BEA NIPA 1.7.5 data available
- **Effort**: 2-3 hours

### 6.2 Run Comprehensive Anu Review v5.0
- **Task**: Full 12-dimension review across all chapters with all 33 series
- **Expected**: Project score ≥ 97% (EXEMPLARY)
- **Effort**: 2 hours

### 6.3 Update Pipeline State
- **Task**: Update PIPELINE_STATE.json v2.0 to reflect all stages complete for all chapters
- **Update**: CHECKLIST.md, VERSION_LOG.md, HANDOFF_DOCUMENTATION.md

### 6.4 Regenerate ANU_LEDGER.json
- **Command**: `python replicate.py --ledger`
- **Expected**: Coverage 95%+ (up from 87%)

### Phase 6 Exit Criteria
- [ ] 33/33 series complete with full artifact sets
- [ ] Anu Review v5.0: project score ≥ 97%
- [ ] Pipeline state: all chapters through stage 6
- [ ] Ledger: documentation health ≥ 95%

---

## Phase 7: Deliverables & Production (1-2 sessions)

### 7.1 Generate LaTeX/PDF Reports
- **Task**: Create publication-quality reports for each chapter:
  - Chapter summary with key findings
  - Data tables (replicated vs original vs extended)
  - Figures (all FPR figures rendered)
  - Methodology notes (splice methods, divergences, assumptions)
- **Output**: `Outputs/Reports/`
- **Effort**: 4-6 hours

### 7.2 ShinyApp Modularization
- **Task**: Refactor the 114KB server_logic.R monolith into modular components:
  - Extract tab-specific logic into `modules/` (11 tabs → 11 modules)
  - Extract shared utilities into `utils/` (data loading, chart helpers)
  - Keep app.R as thin orchestrator
- **Effort**: 6-8 hours
- **Impact**: Maintainability improvement; no functional change

### 7.3 ShinyApp Wave 2 Integration
- **Task**: Add Wave 2 series to Shiny app:
  - Add CH4_SERIES_MAPPING, CH7_SERIES_MAPPING to data_loader.R
  - Create chart builders for IO analysis, labor values, cross-study comparison
  - Add new tabs: IO Framework, Labor Values, Comparison
- **Dependencies**: Phase 5 (Wave 2 series must exist)
- **Effort**: 4-6 hours

### 7.4 Fresh Environment Reproducibility Test
- **Task**: Clone the Replicator package to a clean directory, install dependencies, run full pipeline
- **Steps**:
  1. Copy ANU_REPLICATOR/ to a temp directory
  2. Install requirements.txt in a fresh venv
  3. Set API keys
  4. Run `python replicate.py --full`
  5. Verify all outputs match originals (V08 hash check)
- **Effort**: 2-3 hours
- **Impact**: Confirms reproducibility guarantee

### 7.5 Package Final Deliverables
- **Task**: Create deliverable packages in `Outputs/Deliverables/`:
  - Complete dataset (1948-2025, all 33 series)
  - Extenbook collection (33 XLSX workbooks)
  - Methodology report (PDF)
  - Replicator package (self-contained ZIP)
  - Shiny app deployment bundle
- **Effort**: 2-3 hours

### Phase 7 Exit Criteria
- [ ] LaTeX/PDF reports generated for all chapters
- [ ] ShinyApp modularized and Wave 2 integrated
- [ ] Fresh environment test passed
- [ ] Deliverable packages created
- [ ] Druck Completion Rating: ≥ 97%

---

## Dependency Graph

```
Phase 1 (V## tuning + ADJ-002)
    │
    v
Phase 2 (Documentation completion)
    │
    v
Phase 3 (IO matrix sourcing) ← CRITICAL PATH / EXTERNAL DEPENDENCY
    │
    v
Phase 4 (Ch4 IO framework + DIV-001)
    │
    v
Phase 5 (Wave 2 series extension)
    │
    v
Phase 6 (Wave 3 + final review)
    │
    v
Phase 7 (Deliverables + production)
```

**Note**: Phases 1 and 2 can run in parallel. Phase 3 is the critical external dependency.

---

## Effort Estimates

| Phase | Scope | Sessions | Hours |
|-------|-------|----------|-------|
| 1 | V## tuning + ADJ-002 | 1 | 4-6 |
| 2 | Documentation completion | 1 | 8-10 |
| 3 | IO matrix sourcing | 1-2 | 8-14 |
| 4 | Ch4 IO framework | 1-2 | 16-22 |
| 5 | Wave 2 series | 1-2 | 22-32 |
| 6 | Wave 3 + review | 1 | 6-8 |
| 7 | Deliverables | 1-2 | 18-26 |
| **Total** | | **7-12** | **82-118** |

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 1982-1992 IO matrices unavailable | MEDIUM | HIGH — blocks all Wave 2 | Use interpolation between 1977 and 1997; or use annual Make/Use tables as proxy |
| SIC-NAICS concordance has many-to-many sectors | HIGH | MEDIUM — requires judgment calls | Document each decision in DECISION_LOG; cross-validate with Mohun |
| DIV-001 resolution changes profit rate trajectory | LOW | HIGH — may invalidate existing analysis | Run sensitivity analysis first; compare K vs K* trajectories before committing |
| API data vintage changes on re-pull | LOW | LOW — small revisions | Vintage dates tracked in api_config.json; compare before overwriting |
| ShinyApp modularization introduces bugs | MEDIUM | LOW — no data impact | Run test_app.R and validate_data.R before and after refactoring |

---

*This roadmap supersedes ST2_NEXT_STEPS_PLAN.md (Phase A complete) and captures all remaining work from v3.0 infrastructure upgrade through final deliverables.*

*Last updated: 2026-04-08*
