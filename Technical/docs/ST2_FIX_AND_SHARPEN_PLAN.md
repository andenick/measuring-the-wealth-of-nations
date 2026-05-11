# ST2 Fix and Sharpen — Implementation Plan

**Date**: 2026-05-09
**Input**: ST2_FIX_AND_SHARPEN_LIST.md (24 items, ~12 hours)
**Goal**: Pipeline PASS, all warnings investigated, all dead code removed, analytical series extended to 2024, documentation current

---

## Execution Order

Items grouped into 8 work blocks, ordered by dependency and impact.

---

### Block 1: Pipeline PASS (40 minutes)

Fix the single failure + immediate cleanup to get back to green.

**1.1 Fix V02 range bounds (A1)**
- Read `code/validation/V02_range_checks.py`
- Find `RANGE_BOUNDS` and `SERIES_RANGE_OVERRIDES` dicts
- Update T504 range: [0, 15000] -> [0, 5000] (billions after H.1 correction)
- Update T505 range: [0, 30000] -> [0, 10000]
- If T506 or T513/T514 also fail: adjust their ranges
- Run `python run.py --test-all`, verify V02 = 0 FAIL

**1.2 Fix P04 stale benchmark (A2)**
- Edit `code/processing/P04_process_exploitation.py` line 6
- Change `1958: 1.83` to `1958: 2.01` in docstring
- Check for any hardcoded benchmark dict inside the code; update if found

**1.3 Re-baseline V08 hashes (C3)**
- Run V08 with reset/update to accept current file hashes as new baseline
- If V08 doesn't have a reset mode: delete the hash manifest and let it regenerate
- Check: `data/final-data/logs/HASH_MANIFEST.json` — delete and re-run

**Files**: V02_range_checks.py, P04_process_exploitation.py, HASH_MANIFEST.json
**Test**: `python run.py --test-all` → PASS, V02 0 FAIL, V08 0 WARN

---

### Block 2: Dead Code Cleanup (30 minutes)

Remove all references to deprecated artifacts.

**2.1 Remove Table5_7_Extended.csv dependency (B1)**
- `L03_load_key_ratios.py`: Remove the `ext_src = ST_CHOPPED / "ch05" / "Table5_7_Extended.csv"` block (lines 72-84). T506 comes from H.1, T511 from IO, T512 from V*/W. None need the extended CSV.
- `P04_process_exploitation.py`: Update docstring to remove Table5_7_Extended reference. Verify no code path loads it.
- `P05_process_labor_shares.py`: Update docstring. The fallback path to `ext_parsed` for T512 is already after the V*/W component path — keep as emergency fallback but add deprecation comment.
- Move `Inputs/ST_Chopped/ch05/Table5_7_Extended.csv` to `Technical/_archive/deprecated/Table5_7_Extended.csv`

**2.2 Clean L02 legacy fallback (B2)**
- In `L02_load_variable_capital.py`: The legacy fallback reads VariableCapital_SurplusValue.csv. Add prominent warning print if triggered. Or remove entirely since book_tableH1 should always exist now.

**2.3 Update L05/ExploitationComposition docstring (B3)**
- `L05_load_composition.py`: Add note that T510 reads from ExploitationComposition CSV (log-encoded K/V* values decoded with exp(-x))

**Files**: L03, P04, P05, L02, L05
**Test**: Pipeline PASS, no reference to Table5_7_Extended in runtime output

---

### Block 3: Validator Warning Investigation (1.5 hours)

Investigate every WARN, document whether expected or needs fixing.

**3.1 V03 Continuity: 6 WARN (C1)**
- Run pipeline, capture V03 output identifying which series and years
- Expected WARNs: 1989/1990 splice point, 1996 welfare reform (T605/T606), COVID 2020 (T607)
- For each: note "expected structural break" or "needs splice adjustment"
- If any are from the V* correction: check if the splice at 1989 is smooth

**3.2 V06 Splice Quality: 14 WARN (C2)**
- Capture V06 detail: which series, what CR values
- Focus on T504 (DEC-009 documented CR=0.81) — did it improve after H.1 correction?
- For each WARN: if CR > 0.90, document as acceptable; if CR < 0.80, investigate
- The increase from 7 to 14 WARNs may be because more series now have extensions (T601-T604 extended in Session 20)

**3.3 V09/V10/V11/V13/V14 warnings (C4-C7)**
- V09 Mohun: 6 WARN — expected methodology divergence, document
- V10 IO: 8 WARN — likely SIC-NAICS transition and benchmark interpolation
- V11 External: 3 WARN — likely NIPA vintage differences
- V13 Robin: 1 WARN — cross-project validation
- V14 Unit: 1 WARN — identify which series, fix if genuine unit issue

**Output**: Update CHECKLIST.md with current validator counts and explanations for each WARN category

---

### Block 4: K* and Production Worker Fixes (2 hours)

**4.1 Fix K* classification (D1)**
- BEA FAAt403 only has broad categories (Manufacturing, Farms, Financial, Nonfarm nonmanufacturing) — not enough for proper K*
- **New approach**: K* = K_total × ratio_productive_output from L11b
  - IO productive output ratio ≈ 0.55 (NAICS average)
  - K*_approx = K × 0.55
  - This is a standard proxy: productive sectors' share of output ≈ their share of capital
- Update L06b to use this approach instead of description matching
- Update P08 to use the ratio-based K*
- Verify: r* should increase by approximately 1/0.55 ≈ 1.8x vs current

**4.2 Fix P02b production worker fraction (D2)**
- Load BLS CES data by sector: production workers (CES*0006) / total employees (CES*0001)
- For manufacturing: ratio ≈ 0.68; for mining: ≈ 0.71; for construction: ≈ 0.65
- Compute weighted average across productive sectors
- Replace hardcoded 0.60 with actual BLS-derived ratio (~0.55-0.65 depending on year)
- Compare new sector V* with aggregate T504: should narrow the 32% gap

**4.3 Fix T511 to use employment ratio (D3)**
- In P05: change `_extend_t511_via_io()` to prefer `ratio_productive_employment` column from IO_productive_ratios.csv over `ratio_productive_output`
- The employment ratio (~0.60) is more appropriate than the output ratio (~0.55) for an employment share series

**Files**: L06b, P08, P02b, P05
**Test**: Pipeline PASS, K*/K ≈ 0.55 (not 1.0), T511 uses employment ratio

---

### Block 5: GDP Deflator + Real Productivity (1 hour)

**5.1 Fetch GDP deflator from FRED (D4)**
- Series: GDPDEF (GDP Implicit Price Deflator, index 2017=100)
- Fetch via FRED API (same infrastructure as PAYEMS)
- Save to `data/raw-data/parsed/gdp_deflator.csv`
- Rebase to 1982=100 (the book's base year): deflator_1982 = GDPDEF / GDPDEF[1982] × 100

**5.2 Apply deflator to A10 productivity**
- TPr = TP* / py (real total product in 1982 dollars)
- GFPr = GFP* / py
- GDPr = GDP / py
- q* = TPr / Hp (real Marxian productivity)
- y* = GFPr / Hp (real quasi-Marxian)
- y = GDPr / H (real orthodox)
- Compare with book Table J.1 values: q* should be ~$27.56/hr (1948) and ~$78.03/hr (1989)

**Files**: New L_fetch_deflator.py (or add to L04b), A10_marxian_productivity.py
**Test**: q*(1948) ≈ 27.6, q*(1989) ≈ 78.0 (matching book Table J.1)

---

### Block 6: Extend Analytical Series to 2024 (3 hours)

**6.1 Extend A07 social burden rate**
- For 1990-2024: need S* (from T505 combined), P+ (from NIPA: VA - EC)
- VA = NNP from NIPA 1.7.5 (already have GDP data in pipeline)
- EC = total compensation from NIPA T20100 (already have)
- P+ = VA - EC
- Eu_share = 1 - P+/S* (same formula as book period)
- r* = S* / K (from Fixed Assets, already have)
- Plot b trend: did it continue rising post-1989? Reverse under neoliberalism?

**6.2 Extend A09 unproductive exploitation**
- For 1990-2024: ep = T506 combined (extended S*/V*)
- ecu/ecp: use M01 ec_u/ec_p data (already computed for extension period)
- eu = (hu/hp)/(ecu/ecp) × (1 + ep) - 1
- hu/hp ≈ 0.99 (stable assumption, validated for book period)
- Key question: does eu/ep convergence continue or reverse?

**6.3 Extend A10 Marxian productivity**
- For 1990-2024: TP* from T501 combined, GFP* from T503 combined
- Lp from T515 combined, total employment from PAYEMS
- With GDP deflator from Block 5: compute real q*, y*, y
- Key question: does the q*/y ratio continue growing? What about post-2008 and post-COVID?

**Files**: A07, A09, A10
**Test**: All three produce 77 years (1948-2024). Key ratios at 2024 are reasonable.

---

### Block 7: Moos Investigation + Splice Checks (1.5 hours)

**7.1 Moos structural shift (F1)**
- Compute pre-2000 mean NSW/GDP and post-2000 mean NSW/GDP separately
- Our shift: +0.054; Moos published: +0.030
- Test NIPA vintage: compare our 2026-pulled NIPA data with approximate Moos-era (~2015) values
- Test E2 sensitivity: recompute with E2 at alpha=0.0, 0.1, 0.3, 0.5 — which alpha gives shift ≈ 0.030?
- Document finding: either "NIPA vintage explains gap" or "E2 allocation methodology differs"

**7.2 T504 splice quality check (F2)**
- After H.1 correction: what is the new CR at 1989/1990?
- Old: CR=0.81 (DEC-009). New should be different because V* levels changed by 9x.
- If CR improved: update DEC-009. If degraded: investigate.

**7.3 1990-1997 gap assessment (F3)**
- Document the quality of the 1990-1997 interpolation for each series
- Key series: T504 (log-linear ec_u/ec_p interpolation), T501/T502 (GDP proxy)
- Check: do any NIPA tables have industry detail before 1998?

**Output**: Updated DEC-009, Moos shift finding documented, gap assessment note

---

### Block 8: Documentation Update (1 hour)

**8.1 Update ASSUMPTIONS.md (E1)**
- ASM-D-002: "Open" → "Partially resolved (L06b fetches industry data, K* ≈ K × 0.55)"
- ASM-D-003: "Accepted" → "Superseded (T511 now IO-extended, T512 from V*/W components)"
- Add ASM-D-005: Table H.1 digitization source quality (some 1965-1969 values interpolated from Table I.1)

**8.2 Update CHECKLIST.md (E2)**
- Update all validator counts to current values
- Add sections for analytical series (A07-A10)
- Add Phase 4 completion items

**8.3 Update DECISION_LOG cross-references (E3)**
- DEC-002: Add "Partially resolved: K* ≈ K × IO_ratio (Block 4.1)"
- DEC-005: Add "Superseded: T511 now IO-extended (Step 10)"
- DEC-009: Update CR value after Block 7.2

**8.4 Update series_registry.json metadata (E4)**
- T504: source_file → "book_tableH1_1948_1989.csv"
- T505: same
- T506: validation reference_values → Table H.1 values (1958: 2.01, 1972: 1.99)
- T510: name already updated to "Value Composition of Capital (K/V*)"
- T511: extension method → "IO productive employment ratio"
- T512: extension method → "V*/W from components"

---

## Dependency Graph

```
Block 1 (pipeline PASS) ─────────> Block 2 (dead code cleanup)
                                        |
Block 3 (warnings) ───── parallel ──────┤
                                        |
Block 4 (K* + prod worker) ────────────>|
                                        |
Block 5 (deflator) ────────────────────>|
                                        ├──> Block 6 (extend analytical)
                                        |
Block 7 (investigations) ── parallel ───┤
                                        |
                                        └──> Block 8 (documentation)
```

**Parallel opportunities**:
- Blocks 1+3 can partially overlap (fix V02, then investigate remaining warnings)
- Blocks 4+5 are independent
- Block 6 depends on Blocks 4+5 (needs K* and deflator for full extensions)
- Block 7 is independent of everything except Block 1
- Block 8 should be last (captures final state)

---

## Session Plan

### Session A (~4 hours): Fix + Clean + Investigate
- Block 1: Pipeline PASS (40 min)
- Block 2: Dead code cleanup (30 min)
- Block 3: Validator warnings (1.5 hr)
- Block 7: Moos + splice checks (1.5 hr)

### Session B (~4 hours): Sharpen + Extend
- Block 4: K* and production worker fixes (2 hr)
- Block 5: GDP deflator + real productivity (1 hr)
- Block 6: Extend analytical series to 2024 (1 hr of session B, continue in C)

### Session C (~3-4 hours): Complete + Document
- Block 6: Finish extending A07/A09/A10 to 2024 (2 hr)
- Block 8: Documentation update (1 hr)
- Final pipeline run + fresh-env test (30 min)

---

## Expected Outcome

After all blocks:

| Metric | Current | Target |
|--------|---------|--------|
| Pipeline | FAIL (1) | **PASS** |
| V02 FAIL | 5 | **0** |
| V03 WARN | 6 | **6 (documented)** |
| V06 WARN | 14 | **14 (documented)** |
| V08 WARN | 13 | **0 (re-baselined)** |
| Dead code refs | 3 files | **0** |
| Analytical series | book only | **1948-2024** |
| Productivity | nominal | **real (1982$)** |
| K*/K | 1.000 (wrong) | **~0.55 (correct)** |
| Moos shift | unexplained | **documented** |
| ASSUMPTIONS.md | stale | **current** |
| CHECKLIST.md | stale | **current** |

---

*Plan authored 2026-05-09. 24 items, 8 blocks, ~12 hours across 3 sessions.*
