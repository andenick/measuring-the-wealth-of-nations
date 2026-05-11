# ST2 Anu Processing Plan — Opus Agent Execution

**Date**: 2026-05-06
**Goal**: Complete all KB reading, research JSON creation, artifact fixes, and DEC-012 verification using Opus agents before final integration.

---

## Round 1: Create 7 Missing T-Series Research JSONs (5 Opus agents)

Each agent reads the relevant HDARP chunks and writes a research JSON.

| Agent | Series | KB Chunks to Read | Output |
|-------|--------|-------------------|--------|
| 1 | T201 | chunks 03-05 (Ch2-3), chunk 26 (App A), `page_030_theoretical_content.md`, `page_040_production_distinction.md` | `Technical/research/T201_research.json` |
| 2 | T401, T402 | chunks 09-12 (Ch4), chunk 32 (App F, IO tables), chunk 27 (App B, SIC), `page_060_sectoral_structure.csv` | `Technical/research/T401_research.json`, `T402_research.json` |
| 3 | T701, T702 | chunks 14-15 (Ch5 IO integration), chunk 31 (App E, capital stock), chunk 33 (App G, profit rates), `page_100_labor_values.tex` | `Technical/research/T701_research.json`, `T702_research.json` |
| 4 | T703 | chunks 34-36 (App I exploitation, App J productivity), chunk 33 (App G), DEC-011 in DECISION_LOG.md | `Technical/research/T703_research.json` |
| 5 | T801 | chunk 24 (Ch7 findings), chunk 26 (App A orthodox comparison), chunk 38 (App M Mage comparison) | `Technical/research/T801_research.json` |

**Format reference**: Read `Technical/research/T501_research.json` first for the canonical structure.
**Rule**: Only cite substantive KB files (HDARP chunk full_transcription.md, named .csv/.tex files). Never cite page stubs (`text/page_201.md` through `page_399.md`).

---

## Round 2: Audit & Update 26 Existing T-Series Research JSONs (5 Opus agents)

Each agent reads a batch of existing research JSONs, cross-checks against DECISION_LOG.md and series_registry.json, and updates them.

| Agent | Series | What to Check | Key Decisions to Verify |
|-------|--------|---------------|------------------------|
| 1 | T501-T504 | Stub references in kb_sources_searched, subseries match registry, construction chain accuracy | DEC-007 (SIC-NAICS interpolation), DEC-009 (T504 splice CR=0.81) |
| 2 | T505-T510 | Same protocol | DEC-002 (total K not K*), DEC-010 (DIV-001 blocked), DEC-003 (VA*/W constant) |
| 3 | T511-T516 | Same protocol | DEC-005 (BLS CES proxy, 78%/76% faithfulness) |
| 4 | T601-T607 | Same protocol + read narrative_chunk_18-20_ch6.md | DEC-006 (1996 welfare reform), DEC-008 (tax allocation p.64) |
| 5 | T608-T609, T901 | Same protocol | NSW formula documentation completeness |

**Protocol per JSON**:
1. Read existing JSON
2. Remove any references to stub files (page_201–399 pattern)
3. Add missing DEC-### references from DECISION_LOG.md
4. Verify subseries_affected matches current series_registry.json subseries
5. Verify methodology_summary is accurate to current pipeline state
6. Write updated JSON back

---

## Round 3: Create 26 N-Series Research JSONs (5 Opus agents)

Each agent reads the relevant external paper KB content and creates research JSONs.

| Agent | Study | Series | KB Source | Files to Read |
|-------|-------|--------|-----------|---------------|
| 1 | Studies 1-2 (Tonak 1984, S&T 1987) | N1001-N1002, N1101-N1103 | `external_papers/state_welfare/1984_Tonak_State_Revenues/` (51 files), `productive_labor/1987_Shaikh_Tonak_Social_Wage_Myth/full_transcription.md` | chunk full_transcriptions + DPRs for these series |
| 2 | Studies 3-4 (S&T 2002, Moos 2017) | N1201-N1202, N1301-N1305 | `state_welfare/2002_Shaikh_Tonak_Welfare_State/full_transcription.md`, `state_welfare/2017_Moos_NSW_21st_Century/` (4-level) | full_transcription + equations + table_descriptions |
| 3 | Studies 5-6 (Mohun 2005, 2013) | N1401-N1404, N1501-N1504 | `productive_labor/2005_Mohun_US_1964_2001/full_transcription.md`, `2013_Mohun_Unproductive_1964_2010/full_transcription.md` | full_transcriptions + existing DPRs |
| 4 | Study 7 (Turkey 2022) | N1601-N1602 | `international/2022_Karabacak_Tonak_NSW_Turkey/` (4-level), `turkstat_indicators_1923_2011/chunk_027_summary.md` + Table 20.37 CSV | full_transcription + HDARP Turkey tables |
| 5 | Study 8 (Cronin NZ 2001) | N1701-N1704 | `international/2001_Cronin_New_Zealand/` (6-file HDARP: body_text, equations, figures, tables, notes, SUMMARY) | All 6 files in Cronin directory |

**Each agent must also reference**: DEC-012 (no synthetic data), the relevant DPR for each series, and DECISION_LOG.md entries (DEC-013 for Moos, DEC-014 for Turkey).

---

## Round 4: Fix Artifact Gaps (3 Opus agents)

| Agent | Task | Files to Create/Update |
|-------|------|----------------------|
| 1 | Create 3 missing DPRs (N1702, N1703, N1704) using N1701_DPR.md as template + Cronin KB SUMMARY.md + series_registry.json reference values | `Technical/docs/studies/N1702_DPR.md`, `N1703_DPR.md`, `N1704_DPR.md` |
| 2 | EPR ledger reconciliation: read all 28 EPR files, check extension status in series_registry.json, produce reconciliation report | Update `ANU_LEDGER.json` EPR fields |
| 3 | DEC-012 verification: read P18, P20 scripts for np.random; verify Tonak/Turkey/Cronin source CSVs exist; verify N1001/N1601 DPR status fields | Update DPRs + registry construction descriptions if needed |

---

## Round 5: Regenerate Ledger + Run Review (2 Opus agents)

| Agent | Task |
|-------|------|
| 1 | Regenerate ANU_LEDGER.json by scanning all artifacts (research JSONs, DPRs, EPRs, chopped, extenbooks, decompositions). Add VAR-007 to VARIANT_REGISTRY.json. |
| 2 | Run 59-series audit against 13 anu-review dimensions. Score each series. Produce `Technical/docs/ST2_REVIEW_REPORT.md` with per-series scorecards, chapter aggregates, gap analysis. |

---

## Execution Summary

| Round | Agents | Duration | Creates |
|-------|--------|----------|---------|
| 1 | 5 Opus | ~15 min | 7 research JSONs |
| 2 | 5 Opus | ~15 min | 26 updated research JSONs |
| 3 | 5 Opus | ~15 min | 26 new research JSONs |
| 4 | 3 Opus | ~10 min | 3 DPRs + ledger fixes + DEC-012 verification |
| 5 | 2 Opus | ~10 min | Updated ledger + REVIEW_REPORT.md |
| **Total** | **20 agents across 5 rounds** | **~65 min** | **59 research JSONs + 3 DPRs + ledger + review** |

---

## Integration Phase (after all rounds complete)

Once all processing is done:
1. Run `python run.py` — verify 0 FAIL maintained
2. Run `python run.py --report` — check series count reflects all 59
3. Commit all new artifacts to git
4. Update HANDOFF_DOCUMENTATION.md with session summary
5. Proceed to Phases 4-6 of the ST2 completion plan (Shiny tabs, LaTeX, Zenodo)
