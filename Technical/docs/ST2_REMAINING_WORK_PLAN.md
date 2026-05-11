# ST2 Remaining Work Plan

**Date**: 2026-05-09
**Pipeline state**: PASS (idempotent), 59 series + 3 analytical, V02 86/0, 0 FAIL
**Data quality**: Verified (H.1 digitization confirmed, BLS ratios from data, M01 stable)
**Goal**: Complete all remaining code quality, data extensions, and investigation items

---

## Phase A: Code Consolidation (2 hours)

Merge sub-scripts into their parents, clean file organization.

### A1. Consolidate L04 family (L04, L04b, L04c)

L04 calls L04b and L04c via importlib hacks. These should be proper functions inside L04.

**What**:
- Move `load()` from L04b into L04 as `_fetch_payems()`
- Move `load_gdp_deflator()` from L04b into L04 as `_fetch_gdp_deflator()`
- Move `load()` from L04c into L04 as `_fetch_sector_employment()`
- Call all three from L04's `load()` function
- Delete L04b and L04c files
- Update any imports that reference them

**Files**: L04, L04b (delete), L04c (delete)
**Effort**: 30 minutes

### A2. Consolidate L06 family (L06, L06b)

Same pattern: L06 calls L06b via importlib.

**What**:
- Move `load()` from L06b into L06 as `_fetch_fixed_assets_industry()`
- Call from L06's `load()` function
- Delete L06b
- Update P08 if it references L06b directly

**Files**: L06, L06b (delete)
**Effort**: 20 minutes

### A3. Consolidate L02 family (L02, L02b)

L02 reads from L02b-generated CSV. L02b is essentially a data prep step.

**What**:
- Move L02b's `reconstruct()` into L02 as `_load_from_table_h1()`
- L02 calls this directly instead of checking for the reconstructed CSV
- Delete L02b
- The book_tableH1 CSV remains as the source; L02 reads it directly

**Files**: L02, L02b (delete)
**Effort**: 20 minutes

### A4. Consolidate L11 family (L11, L11b)

L11 calls L11b via importlib.

**What**:
- Move L11b's `load()` into L11 as `_parse_naics_io()`
- Keep NAICS classification dict and employment ratio computation
- Delete L11b
- The IO_productive_ratios.csv output path stays the same

**Files**: L11, L11b (delete)
**Effort**: 30 minutes

### A5. Clean P02b

P02b (sector V*) is called from P02 via importlib. It's a reference computation, not a primary pipeline path.

**What**:
- Move P02b's `compute_sector_v_star()` into P02 as a comparison function
- Call after the main T504 computation
- Delete P02b

**Files**: P02, P02b (delete)
**Effort**: 20 minutes

---

## Phase B: Documentation Pass (1.5 hours)

Update every script header docstring to reflect current data flow.

### B1. Update all L## docstrings

For each loader script, ensure the docstring accurately describes:
- What data source it reads (book_tableH1, NIPA, FRED, BLS)
- What parsed CSVs it produces
- What dependencies it has
- Any FRED/BEA API keys required

Scripts to update: L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11, L12, L13, L14, L15, L17, L18

**Effort**: 30 minutes

### B2. Update all P## docstrings

For each processor, ensure:
- Formula is documented (e.g., "T506 = S*/V* from T505/T504")
- Input/output files are correct
- Priority and dependency chain is documented
- Any Principle 3 compliance notes

Scripts to update: P01-P21

**Effort**: 30 minutes

### B3. Update DECISION_LOG with final status

Add status updates to all 20 DEC entries reflecting current state:
- DEC-002: "Resolved: K* = K × 0.567 via IO ratio"
- DEC-005: "Superseded: T511 IO-extended, T512 from V*/W components"
- DEC-009: "Resolved: CR=0.975 raw (M01 adjusts to 1.109 by design)"
- DEC-012: "Enforced: all synthetic data removed"
- DEC-020: "Resolved: Table H.1 digitized, V* in correct billions"

**Effort**: 20 minutes

### B4. Update README.md

The project README should reflect final pipeline stats:
- 59 series + 3 analytical
- 0 UNJUSTIFIED, 0 UNKNOWN
- Table H.1 digitized
- Pipeline idempotent
- Key results: e 1.70→2.44→~2.10(2024), q*(1989)=$78.64/hr, Khanjian=0.801

**Effort**: 15 minutes

---

## Phase C: Remaining Data Extensions (3 hours)

### C1. Read remaining high-value KB chunks

**Chunks 6-9** (Chapter 3: sectoral structure, IO-Marxian mapping):
- Contains the definitive productive/unproductive sector classification rules
- Would validate our NAICS classification in L11b
- 4 chunks × 15 min = 1 hour

**Chunks 25-27** (Chapter 7 conclusions + Appendices A-C):
- Chapter 7 narrative about the falling rate of profit
- Appendices A-C: IO aggregation methodology
- 3 chunks × 15 min = 45 minutes

**Output**: Updated KB_DEEP_DIVE_FINDINGS.md with new findings. Possible classification corrections to L11b.

**Effort**: 2 hours

### C2. 1992 IO benchmark search

**What**: Check BEA website for the 1992 benchmark IO table. If available, download and parse to narrow the 1978-1996 interpolation gap.

**Method**:
1. WebSearch for "BEA 1992 benchmark input output table"
2. Check bea.gov/industry/input-output-accounts-data
3. If found: download Use table, parse with L11 infrastructure
4. If not: document as unavailable, current approach stands

**Effort**: 30 minutes (search + document)

### C3. Extend Table H.1 cross-checks to extension period

**What**: The digitized Table H.1 gives us exact book values for 1948-1989. For the extension period (1990-2024), we should compute the same variables (S*, VA*, V*, S*/V*, TP*, GFP*, P+, EC) from NIPA data and compare them with the pipeline's T-series outputs to verify consistency.

**Method**: Use NIPA 1.7.5 (GDP/NNP), 2.1 (personal income/EC), and pipeline T501-T506 to compute a "synthetic Table H.1" for 1990-2024. Verify S* = VA* - V* identity holds for all extension years.

**Effort**: 30 minutes

---

## Phase D: Empirical Investigations (6 hours)

### D1. Social burden rate trajectory 1948-2024

**What**: A07 already computes P+/S* and Eu_share for 78 years. Needs analysis + figures.

**Method**:
1. Compute period means: 1948-73, 1973-80, 1980-89, 1989-2000, 2000-08, 2008-20, 2020-24
2. Identify turning points: when does Eu_share peak? Is there a neoliberal reversal?
3. Compute r* trajectory: falling 1948-80, recovering 1980-89, what after 1989?
4. Generate publication figure with annotated phases

**Output**: Figure + summary statistics + brief interpretation

**Effort**: 1.5 hours

### D2. Productivity slowdown decomposition

**What**: A10 computes q*, y*, y for 78 years in real 1982$. Needs period analysis.

**Method**:
1. Compute growth rates by period (same periods as D1)
2. Decompose q*/y ratio = (TP*/GDP) × (L/Lp): which component drives the widening gap?
3. Identify whether the post-2005 "productivity slowdown" is visible in q* or only in y
4. Check COVID productivity spike (2020-21): compositional or real?
5. Generate figure: q* vs y indexed to 1948=100

**Output**: Figure + growth rate table + decomposition

**Effort**: 1.5 hours

### D3. Exploitation convergence post-1989

**What**: A09 shows eu/ep convergence from 0.80 to 0.97 in the book period. Extended to 2024.

**Method**:
1. Plot eu, ep, eu/ep for 1948-2024
2. Did eu permanently surpass ep (the 1978 crossover in the book)?
3. Is the ecu/ecp ratio (wage differential) still near 1.01?
4. What does the gig economy do to the productive/unproductive classification?

**Output**: Figure + summary

**Effort**: 1 hour

### D4. Sensitivity analysis

**What**: Test how results change under 4 key assumptions.

**Tests**:
1. VA*/W: constant 1.238 vs M01 year-varying → T506 extension
2. IO productive ratio: output (~0.55) vs employment (~0.60) → T511
3. Total K vs K*×0.567 → r* level
4. NSW: old 40% defense vs Appendix N 3-group → T607

**Method**: For each, modify the parameter, re-run pipeline, record T506[2024], T511[2024], r*[2024], T607[2024]. Compute maximum and mean deviation from baseline.

**Output**: Sensitivity matrix (4 assumptions × 4 series × 3 metrics)

**Effort**: 2 hours

---

## Phase E: Publication Preparation (8 hours)

### E1. LaTeX methodology paper

**Structure**:
1. Introduction (1 page): Shaikh & Tonak (1994), replication scope, key contributions
2. Data and sources (2 pages): Table H.1 digitization, BEA/BLS/FRED APIs, IO framework
3. Methodology (4 pages): chapter-by-chapter series construction, 20 decisions documented
4. Results (3 pages): 59 series replicated, cross-validations (Khanjian 0.801, Ochoa R²=0.931)
5. Extensions (3 pages): post-1989 social burden rate, productivity, exploitation convergence
6. Discussion (2 pages): NAICS-era price-value decline, Moos shift, structural implications
7. Appendix: complete series registry, validation results, data provenance

**Effort**: 6-8 hours across 2 sessions

### E2. GitHub preparation

**What**:
- Update .gitignore (API keys, __pycache__, adjusted-final-data)
- Sanitize NAICS IO JSON metadata (remove API keys)
- Write clean requirements.txt
- README with installation + run instructions
- Commit with comprehensive message

**Effort**: 1 hour

### E3. Fresh-environment test

**What**: Clean venv, pip install, copy api_keys.env, run pipeline, verify PASS.

**Effort**: 30 minutes

---

## Execution Order

```
Phase A (consolidation, 2h)
  A1 -> A2 -> A3 -> A4 -> A5
  Then: clean build, verify PASS

Phase B (documentation, 1.5h)
  B1 -> B2 -> B3 -> B4
  Then: verify pipeline still PASS

Phase C (data extensions, 3h)
  C1 (KB chunks) || C2 (1992 IO search) || C3 (extension cross-check)
  All independent

Phase D (investigations, 6h)
  D1 (social burden) -> D2 (productivity) -> D3 (exploitation)
  D4 (sensitivity) independent of D1-D3

Phase E (publication, 8h)
  E1 (LaTeX) requires D1-D3 results
  E2 (GitHub) after all code changes
  E3 (fresh test) last
```

## Session Mapping

| Session | Blocks | Hours | Output |
|---------|--------|-------|--------|
| Next | A (code consolidation) + B (docs) | 3.5 | Cleaner codebase, fewer files, current docs |
| +1 | C (data extensions) + D1-D3 (investigations) | 5-6 | KB findings, 3 publication figures |
| +2 | D4 (sensitivity) + E1 (LaTeX start) | 5-6 | Sensitivity matrix, paper draft |
| +3 | E1 (LaTeX finish) + E2 (GitHub) + E3 (test) | 4-5 | Published paper, clean repo |

**Total**: ~18-22 hours across 4 sessions

---

## What This Achieves

After all phases:
- **Codebase**: 8 fewer files (sub-scripts consolidated), all docstrings current, no dead code
- **Data**: 23 more KB chunks read, 1992 IO searched, extension cross-checked
- **Analysis**: Social burden rate post-1989, productivity decomposition, exploitation convergence, sensitivity matrix
- **Publication**: LaTeX paper with all results, clean GitHub repo, fresh-env tested
- **Documentation**: DECISION_LOG final, ASSUMPTIONS.md current, README complete

This is the difference between "a working pipeline" and "a complete research output."

---

*Plan authored 2026-05-09. All dependencies verified against current pipeline state (PASS, idempotent, V02 86/0).*
