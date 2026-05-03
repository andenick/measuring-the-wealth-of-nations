# ST2 Next Steps Plan

**Created**: 2026-03-30 (post-v4.0 Anu Review)
**Updated**: 2026-03-30 (Phase A complete)
**Project Score**: 93%+ (COMPLETE) | Druck: ~91%
**Wave 1**: 26/26 series complete | **Wave 2/3**: 0/7 series started
**Phase A**: COMPLETE (all 7 items implemented and verified)

This plan orders all remaining work by dependency, so each step is unblocked when reached.

---

## Phase A: Wave 1 Polish -- COMPLETE (2026-03-30)

All items implemented and verified in a single session.

### A1. Compute T608 extended values
**Priority**: HIGH | **Effort**: Small | **Blocks**: T901 extended summary completeness
- T608 = T607 / T504 (NSW / Variable Capital)
- T607 (NSW) already extended to 2025; T504 (V*) already extended to 2024
- Populate the empty column in `Technical/ANU_REPLICATOR/data/final-data/chopped/T608_chopped.csv`
- Update `Technical/ANU_REPLICATOR/data/final-data/series/T608.csv`
- Update T608 extenbook
- Rebuild T901 summary table to include T608 for extended period
- Update T608_EPR.md certification (currently CERTIFIED WITH NOTES — computation PENDING)
- **Files**: `scripts/processing/P11_process_nsw.py`, `P12_process_summary.py`

### A2. Resolve DIV-002 (VA*/W constant assumption)
**Priority**: MEDIUM | **Effort**: Medium | **Blocks**: Improved T504-T506, T512 faithfulness
- Replace constant VA*/W = 1.238 with year-varying `ec_u/ec_p` ratio from BLS CES data
- BLS CES data already fetched: `Inputs/API_Data/BLS/bls_ces_production_workers.csv`
- Recompute T504 (V*), T505 (S*), T506 (e = S*/V*), T512 (V*/W) for 1948-2024
- Validate that benchmark years (1948, 1967, 1989) still match within 0.1%
- Update EPRs with new faithfulness scores (expect T504: 76%→85%+, T506: 72%→80%+)
- Update DIVERGENCE_REGISTER.json: DIV-002 status → "resolved"
- **Files**: `scripts/processing/P02_process_variable_capital.py`, `P03_process_surplus_value.py`, `P04_process_exploitation.py`, EPRs for T504-T506, T512

### A3. Complete 1996 welfare reform bridge
**Priority**: MEDIUM | **Effort**: Medium | **Blocks**: Ch6 extension accuracy post-1996
- Structural break at 1996 (Personal Responsibility and Work Opportunity Act)
- Bridge logic partially implemented in `scripts/loading/L08_load_benefits.py` and `scripts/processing/P10_process_benefits.py`
- Need: pre-reform vs post-reform fiscal allocation methodology comparison
- Validate T605 (benefits) and T606 (government services) continuity across 1996
- Document in T605_EPR.md and T606_EPR.md transition analysis sections
- **Files**: `L08_load_benefits.py`, `P10_process_benefits.py`, T605_EPR.md, T606_EPR.md

### A4. Document per-series tolerance thresholds
**Priority**: LOW | **Effort**: Small | **Blocks**: Formal validation completeness
- Currently only aggregate 93.8% benchmark match documented
- Define explicit tolerance per series based on Phase 3 validation results
- Add to each DPR's validation record section
- Categories: rate series (±0.1%), level series (±1%), ratio series (±0.5%)
- **Files**: All 26 DPR files (batch update)

### A5. Flatten Inputs/ directory
**Priority**: LOW | **Effort**: Small | **Blocks**: Druck compliance
- Current: type-based subdirs (PDFs/, Excel/, Documents/, Images/, Data/)
- Target: flat structure preserving user organization
- Move contents up, remove empty type dirs
- Update any path references in scripts/configs
- **Files**: `Inputs/` directory restructure

### A6. Copy KB narrative pages from parent project
**Priority**: LOW | **Effort**: Small | **Blocks**: D1 score improvement
- Ch5 narrative (pp.95-150): copy from `Projects/Shaikh Tonak/Knowledge_Base/`
- Ch6 narrative (pp.151-180): same source
- Will improve D1 scores from 85-90% toward 95%+
- **Files**: `Technical/Knowledge_Base/text/`

### A7. Fresh environment test
**Priority**: MEDIUM | **Effort**: Medium | **Blocks**: Druck production polish, reproducibility
- Run `replicate.py` in a clean Python environment
- Verify all 26 series reproduce from Inputs/ without errors
- Document any missing dependencies in `requirements.txt`
- Run R tests: `test_chapter_{05,06,09}.R`, `test_artifacts.R`
- **Files**: `Technical/ANU_REPLICATOR/replicate.py`, `requirements.txt`

**Phase A completion target**: Project score 93%→95%+ (approaching EXEMPLARY)

---

## Phase B: Chapter 4 — IO Framework (Wave 2 prerequisite)

This phase builds the Input-Output analytical framework required by Wave 2. It is the critical path for the entire remainder of the project.

### B1. Chapter 4 investigation document
**Priority**: HIGH | **Effort**: Medium | **Blocks**: All of Phase B
- Read Ch4 of book (pp.67-94) — IO-based classification methodology
- Create `Technical/docs/chapters/CHAPTER_4_INVESTIGATION.md`
- Document: productive vs unproductive sector classification rules
- Document: IO table structure (A, L, Z matrices), how Shaikh & Tonak use them
- Identify T401 and T402 series definitions precisely
- **New files**: CHAPTER_4_INVESTIGATION.md

### B2. Extend IO matrix coverage (1982-2017)
**Priority**: HIGH | **Effort**: Large | **Blocks**: B3, B4
- Currently have: 1947, 1958, 1963, 1967, 1972, 1977 (6 benchmark years, SIC-era)
- Need: 1982, 1987, 1992, 1997, 2002, 2007, 2012, 2017 (8 additional years)
- 1982-1992: SIC-based BEA benchmark IO tables (may need manual sourcing)
- 1997-2017: NAICS-based BEA benchmark IO tables (available via BEA website)
- Apply SIC-NAICS concordance (`Inputs/Concordances/io_85_to_nipa_13_concordance.csv`) to bridge
- Create A, L, Z matrices for each new year
- **Files**: `Inputs/IO_Matrices/` (24 new CSV files: 8 years × 3 matrices)

### B3. Build productive sector classification engine
**Priority**: HIGH | **Effort**: Large | **Blocks**: B4, all Wave 2 series
- Implement Shaikh & Tonak sector classification algorithm:
  - Classify each IO sector as productive (P) or unproductive (U)
  - Apply to all 14 benchmark years
  - Handle SIC-NAICS transition at 1997
- Create classification mapping files
- Interpolate between benchmark years for annual productive/unproductive ratios
- Use interpolation methodology already documented in `Technical/docs/chapters/INTERPOLATION_METHODOLOGY.md`
- **New files**: `scripts/processing/P13_process_io.py` (already exists as stub), classification CSVs

### B4. Process T401-T402 (IO framework series)
**Priority**: HIGH | **Effort**: Medium | **Blocks**: Phase C
- T401: IO-based productive output measures
- T402: IO-based productive labor classification
- Create DPRs, decompositions, research JSONs
- Load via `L11_load_io_matrices.py` (already exists)
- Process via `P13_process_io.py` (already exists as stub)
- Create chopped CSVs, extenbooks
- Run Anu Review for Ch4
- **Files**: T401_DPR.md, T402_DPR.md, T401_DECOMPOSITION.md, T402_DECOMPOSITION.md, etc.

**Phase B completion target**: Ch4 IO framework operational, T401-T402 complete

---

## Phase C: Wave 2 Series Extension (depends on Phase B)

With the IO classification engine from Phase B, extend the 7 book-period-only Ch5 series and build the Ch7 series.

### C1. Extend T501-T503 (productive output aggregates)
**Priority**: HIGH | **Effort**: Medium | **Blocks**: C2, C3
- T501 (TP*): Apply IO sector classification to restrict gross output to productive sectors
- T502 (C*_m): Apply to restrict intermediate inputs to productive sectors
- T503 (VA*): T501 - T502
- Dependency order: T501 → T502 → T503
- Create EPRs for each (currently have none)
- **Files**: `P01_process_revenue.py`, T501_EPR.md, T502_EPR.md, T503_EPR.md

### C2. Extend T507-T510 (derived ratios and components)
**Priority**: MEDIUM | **Effort**: Medium | **Blocks**: None (improves completeness)
- T507 (S*/Y): Derivable from T505/VA*
- T508 (CON*): IO classification applied to consumption components
- T509 (IG*): IO classification applied to investment components
- T510 (C*/V*): Value composition from T502/T504
- Create EPRs for each
- **Files**: `P07_process_composition.py`, T507-T510 EPRs

### C3. Resolve DIV-001 (productive capital K*)
**Priority**: HIGH | **Effort**: Medium | **Blocks**: T513/T514 certification
- Apply IO productive sector classification to BEA Fixed Assets Table 4.1
- Restrict K to productive sectors → K*
- Recompute T513 (r* = S*/K*) and T514 (r*_adj)
- Update EPRs: expect faithfulness 60%→85%+
- Update DIVERGENCE_REGISTER.json: DIV-001 status → "resolved"
- Cross-validate with Mohun (2005) capital stock estimates
- **Files**: `P08_process_profit_rates.py`, T513_EPR.md, T514_EPR.md

### C4. Build Ch7 series (T701-T703)
**Priority**: MEDIUM | **Effort**: Large | **Blocks**: Phase D (Ch8)
- T701: Labor values (using IO Leontief inverse L)
- T702: Prices of production
- T703: Price-value deviations
- Requires Ch4 IO framework + Leontief calculations
- Create investigation doc, DPRs, decompositions, EPRs, chopped, extenbooks
- Create `L12_load_labor_values.py` and `P14_process_labor_values.py` (stubs already exist)
- **New files**: CHAPTER_7_INVESTIGATION.md, T701-T703 full artifact sets

**Phase C completion target**: All Wave 2 series complete, DIV-001 resolved, project score approaching EXEMPLARY

---

## Phase D: Wave 3 and Final Integration (depends on Phase C)

### D1. Build T201 (Alternative GFP measures, Ch2)
**Priority**: LOW | **Effort**: Medium | **Blocks**: None
- T201: Alternative measures of Gross Final Product
- Largely theoretical — may not require IO framework
- Create investigation doc, DPR, decomposition, research JSON, chopped, extenbook
- **New files**: CHAPTER_2_INVESTIGATION.md, T201 artifact set

### D2. Build T801 (Cross-study comparison, Ch8)
**Priority**: LOW | **Effort**: Large | **Blocks**: None
- T801: International/cross-study comparison of exploitation rates and labor productivity
- Depends on T701-T703 for labor value methodology
- Create investigation doc, DPR, decomposition
- **New files**: CHAPTER_8_INVESTIGATION.md, T801 artifact set

### D3. Final Anu Review (all chapters)
**Priority**: HIGH | **Effort**: Medium | **Blocks**: None
- Run /anu-review full after all 33 series complete
- Target: 95%+ project score (EXEMPLARY)
- All 9 chapters should have review reports
- All adequacy assessments should be refreshed

### D4. Generate final deliverables
**Priority**: HIGH | **Effort**: Large | **Blocks**: None
- LaTeX/PDF reports for each chapter
- Complete database export (1948-2025, all 33 series)
- Publication-quality figures
- Package for Outputs/Deliverables/

### D5. Shiny app final polish
**Priority**: MEDIUM | **Effort**: Medium | **Blocks**: None
- Add Wave 2/3 series to data_loader.R mappings
- Add Ch4, Ch7 chart builders
- Test all figures render correctly
- Deploy to Shiny server if applicable

---

## Dependency Graph

```
Phase A (immediate, parallel)
  A1 T608 compute ──────────┐
  A2 DIV-002 resolve ────────┤
  A3 Welfare bridge ──────────┤── all unblocked
  A4 Tolerance docs ──────────┤
  A5 Flatten Inputs ──────────┤
  A6 KB narrative ────────────┤
  A7 Fresh env test ──────────┘

Phase B (sequential, critical path)
  B1 Ch4 investigation ──→ B2 IO matrices ──→ B3 Classification engine ──→ B4 T401-T402

Phase C (depends on B4)
  C1 T501-T503 extend ──→ C2 T507-T510 extend
  C3 DIV-001 resolve (parallel with C1-C2)
  C4 Ch7 T701-T703 (depends on B4)

Phase D (depends on C)
  D1 T201 (independent, can start anytime)
  D2 T801 (depends on C4)
  D3 Final review (depends on all)
  D4 Deliverables (depends on D3)
  D5 Shiny polish (depends on C4)
```

---

## Estimated Impact on Scores

| Milestone | Project Score | Druck Rating | Series Coverage |
|-----------|-------------|--------------|-----------------|
| Current (v4.0) | 93% | 88% | 26/33 (79%) |
| After Phase A | ~96% | ~92% | 26/33 (79%) |
| After Phase B | ~96% | ~93% | 28/33 (85%) |
| After Phase C | ~97% | ~95% | 33/33 (100%) |
| After Phase D | ~98% | ~97% | 33/33 (100%) |

---

*Plan authored 2026-03-30 following comprehensive v4.0 Anu Review.*
