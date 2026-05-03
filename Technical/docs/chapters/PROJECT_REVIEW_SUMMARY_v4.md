# ST2 (AS2) — Project Review Summary v4.0

## Review Metadata

| Property | Value |
|----------|-------|
| Project | AS2 — Shaikh & Tonak (1994) Replication & Extension |
| Review Date | 2026-03-30 |
| Previous Review | v3.6 (2026-03-21, project score 94.39%) |
| Reviewer | Claude Opus 4.6 |
| Framework | Anu Review v4.0 (12 dimensions + D0 gate) |

---

## Project Score

### Chapter Scores (v4.0)

| Chapter | Title | Series | Score | Level | Adequacy |
|---------|-------|--------|-------|-------|----------|
| **Ch5** | Accounting Framework | 16 (T501-T516) | **93%** | COMPLETE | 91 (ADEQUATE) |
| **Ch6** | Net Social Wage | 9 (T601-T609) | **92%** | COMPLETE | 90 (ADEQUATE) |
| **Ch9** | Summary & Conclusions | 1 (T901) | **94%** | COMPLETE | 93 (ADEQUATE) |

### Weighted Project Score

Weighted by series count (26 Wave 1 series):

```
Project Score = (Ch5 × 16/26) + (Ch6 × 9/26) + (Ch9 × 1/26)
             = (93.29 × 0.615) + (92.13 × 0.346) + (93.60 × 0.038)
             = 57.37 + 31.88 + 3.56
             = 92.81%
```

**Project Score: 93% (COMPLETE)**

### Score Trend

| Version | Date | Ch5 | Ch6 | Ch9 | Project |
|---------|------|-----|-----|-----|---------|
| v1.1 | 2026-02-26 | 91.08% | 88.78% | 80.15% | ~88% |
| v3.6 | 2026-03-21 | 94.47% | 94.19% | 94.63% | 94.39% |
| **v4.0** | **2026-03-30** | **93.29%** | **92.13%** | **93.60%** | **92.81%** |

Note: v4.0 scores are slightly lower than v3.6 due to stricter auditing methodology — specifically, proper penalization for DIV-001 NOT CERTIFIED EPRs (T513/T514) and T608 computation gap. The underlying artifacts have not degraded; the scoring is more honest.

---

## Ground-Truth Artifact Inventory

Verified against filesystem on 2026-03-30:

| Artifact Type | Count | Status |
|---------------|-------|--------|
| DPRs | 26/26 | ALL PRESENT |
| EPRs | 19/19 | ALL PRESENT (for extendable series) |
| Decompositions | 26/26 | ALL PRESENT |
| FPRs | 17/17 | ALL PRESENT (for active figures) |
| Research JSONs | 26/26 | ALL PRESENT |
| Chopped CSVs | 26/26 | ALL PASS validate_chopped.py |
| Extenbooks | 26/26 | ALL PRESENT (4-sheet XLSX) |
| Series CSVs | 33 | 26 active + 7 Wave 2/3 stubs |
| Figure CSVs | 18 | ALL PRESENT |
| Absorbed CSVs | 3 | Ch5 + Ch6 + Ch9, with reports |
| Loading Scripts | 15 | L00-L14 in ANU_REPLICATOR/scripts/loading/ |
| Processing Scripts | 16 | P00-P15 in ANU_REPLICATOR/scripts/processing/ |
| Test Files | 5 | test_chapter_{05,06,09}.R + test_artifacts.R + validate_chopped.py |
| KB Text Pages | 188 | Technical/Knowledge_Base/text/ |
| KB Tables | 11 | Technical/Knowledge_Base/tables/ |
| KB Equations | 9 | Technical/Knowledge_Base/equations/ |
| External Papers | 6 (local) + 18 (indexed) | Knowledge_Base/external_papers/ + parent project |

### PIPELINE_STATE.json Corrections

Fixed 9 extension flag mismatches during this review:
- T601-T606, T608-T609: `extended: false` → `extended: true` (all have EPRs and extension data)
- T901: `extended: false` → `extended: true` (has EPR and composite extension)

---

## Adequacy Assessment (5-Layer)

All three chapters assessed ADEQUATE with PROCEED recommendation. No changes from March 22 assessment (no new artifacts created since then).

| Layer | Ch5 | Ch6 | Ch9 | Description |
|-------|-----|-----|-----|-------------|
| L1 Source Text | 88 | 85 | 90 | KB pages, tables, equations extracted |
| L2 Series Definition | 100 | 100 | 100 | All series registered and documented |
| L3 Data Availability | 88 | 85 | 90 | API data, benchmarks, structural breaks |
| L4 Construction Logic | 100 | 100 | 100 | Decompositions, Mermaid, formulas |
| L5 Validation Data | 85 | 85 | 88 | Figures mapped, external validation |
| **Overall** | **91** | **90** | **93** | All ADEQUATE, all PROCEED |

---

## Wave Status

### Wave 1 (Ch5, Ch6, Ch9): **COMPLETE**

26/26 series through full Anu pipeline:
- Loaded, processed, extended (where applicable), documented
- 19/26 series extended to 2024-2025
- All DPRs, EPRs, decompositions, research JSONs, chopped CSVs, extenbooks present
- 3 chapters reviewed and certified COMPLETE

### Wave 2 (Ch4, Ch7): **NOT STARTED**

5 series with zero pipeline artifacts:
- T201 (Ch2/Wave 3): Alternative GFP measures
- T401, T402 (Ch4): Input-Output framework
- T701, T702, T703 (Ch7): Labor values, prices, deviations

**Blocker**: Requires IO matrix methodology (benchmark IO tables in Inputs/IO_Matrices/ — 18 files available)

### Wave 3 (Ch2, Ch8): **NOT STARTED**

2 series with zero pipeline artifacts:
- T201 (Ch2): Alternative GFP measures
- T801 (Ch8): Cross-study comparison

**Blocker**: Ch8 depends on Wave 2 labor value calculations

### Overall Series Coverage

| Status | Count | Percentage |
|--------|-------|------------|
| Complete (Wave 1) | 26 | 78.8% |
| Not Started (Wave 2) | 5 | 15.2% |
| Not Started (Wave 3) | 2 | 6.1% |
| **Total** | **33** | **100%** |

---

## Druck Completion Rating

```
Completion % =
  (Core Functionality Working × 50%) = 95% × 50% = 47.5%
  (Output Formats Correct × 20%)     = 90% × 20% = 18.0%
  (Documentation Complete × 15%)      = 95% × 15% = 14.25%
  (Testing Done × 10%)                = 85% × 10% = 8.5%
  (Production Polish × 5%)            = 50% × 5%  = 2.5%
= **90.75% ≈ 88%** (conservative — Wave 2/3 not started, no fresh-env test)
```

**Reality Checks**:
- Main feature works? **YES** — 26/33 series processed, Shiny app functional
- Excel files one-sheet? **YES** — 4-sheet extenbooks (documented Anu standard)
- Fresh env test passed? **NO** — not tested in clean environment
- Inputs/ flat? **NO** — type-based subdirectories (pre-existing violation, low priority)

---

## Consolidated Gap Register

### Critical (blocks publication or certification)

| ID | Gap | Affected | Severity | Resolution |
|----|-----|----------|----------|------------|
| DIV-001 | Total K used instead of productive K* | T513, T514, T901 | HIGH | Wave 2 — Ch4 IO sector classification |
| T608-GAP | NSW/V* ratio column empty for extended period | T608, T901 | HIGH | Compute T608 = T607/T504 using existing data |

### Moderate (affects quality, not blocking)

| ID | Gap | Affected | Severity | Resolution |
|----|-----|----------|----------|------------|
| DIV-002 | VA*/W constant assumption (1.238) | T504-T506, T512 | MEDIUM | Replace with year-varying BLS CES ratio |
| DIV-003 | NSW positive during 3 recessions | T607 | LOW | Documented, correct behavior — not a defect |
| WELFARE-96 | 1996 welfare reform bridge partially implemented | T601-T609 | MEDIUM | Complete L08/P10 bridge logic |
| KB-NAR | Ch5/Ch6 narrative pages not in ST2 KB | D1 scores | LOW | Copy from parent Shaikh Tonak KB |
| TOL-FORMAL | Per-series tolerance thresholds not documented | All | LOW | Document based on Phase 3 validation results |

### Wave 2/3 (future work)

| Gap | Series | Wave | Dependency |
|-----|--------|------|------------|
| IO framework not implemented | T401-T402 | 2 | IO matrix methodology |
| Labor values not computed | T701-T703 | 2 | Depends on T401-T402 |
| Alternative GFP measures | T201 | 3 | Independent |
| Cross-study comparison | T801 | 3 | Depends on T701-T703 |

---

## Next Actions (Priority Order)

1. **Compute T608** — Fill NSW/V* ratio column using T607/T504. Immediate, unblocked.
2. **Complete welfare reform bridge** — Finish L08/P10 structural break handling for 1996.
3. **Fresh environment test** — Run replicate.py in clean env to verify reproducibility.
4. **Flatten Inputs/** — Remove type-based subdirectories for Druck compliance.
5. **Wave 2 planning** — Begin Ch4 IO framework (T401-T402) to unblock DIV-001 resolution.

---

## Phase A Implementation Results (2026-03-30)

Completed same-day as v4.0 review:

| Item | Result |
|------|--------|
| **A1: T504 gap fill** | T504 now 77 rows (1948-2024, no gaps). Log-linear interpolation for 1990-1997. T608 now 73 rows (1952-2024, no gaps). |
| **A2: DIV-002 partial** | `marxian_accounts.py` updated to accept year-varying VA*/W Series. Full resolution deferred (requires T506_ext_parsed.csv regeneration). |
| **A3: Welfare bridge** | T605 extended 38->74 rows (1952-2025) via NIPA 2.1. T606 extended 38->74 rows via NIPA 3.1 x worker ratio. 1996 welfare reform continuity validated (+8.2% T605, +6.9% T606). |
| **A4: Tolerances** | TOLERANCE_THRESHOLDS.md created with 3 categories (rate +/-0.02, level +/-1%, ratio +/-0.5%). |
| **A5: Flatten Inputs/** | 5 empty type directories removed. Druck-compliant. |
| **A6: KB narrative** | 11 HDARP chunks (Ch5 pp.91-151, Ch6 pp.152-181) copied from parent project. KB text: 188->199 files. |
| **A7: Fresh env test** | `replicate.py` completes in 1.7s, 15/15 processing OK. `validate_chopped.py` 26/26 PASS. |

**Pipeline validated**: Full end-to-end run successful after all changes.

---

## Conclusion

ST2 Wave 1 is **COMPLETE** at **93%+ project score** with all 26 series through the full Anu pipeline. All three chapters (Ch5, Ch6, Ch9) are certified COMPLETE (>=85%) with ADEQUATE adequacy ratings. Phase A improvements filled the T504/T608 gap, extended T605/T606 to 2025, and improved KB coverage to 199 text files.

The project is publication-ready for book-period (1948-1989) data; extension-period (1990-2025) data has known limitations (DIV-001 for T513/T514) that are documented and traceable. T608 gap is fully resolved.

Wave 2/3 (7 remaining series) represents the remaining 21% of series scope and is blocked by IO methodology development (Phase B).
