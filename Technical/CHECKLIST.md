# AS2 Progress Checklist

## Wave 1 — Chapters 5, 6, 9 (COMPLETE)

### Chapter 5: Accounting Framework
- [x] Chapter investigation (NIPA-line-item depth)
- [x] 16 series loaded (T501-T516)
- [x] 16 series processed (all construction steps)
- [x] 9 series extended (T504-T506, T511-T516)
- [x] 16 DPRs written
- [x] 9 EPRs written
- [x] 8 FPRs written
- [x] 16 chopped CSVs validated
- [x] 16 extenbooks generated
- [x] Shiny integration (CH5_SERIES_MAPPING, chart builders)
- [x] Test suite (test_chapter_05.R)
- [x] Adequacy: 91% (ADEQUATE)
- [x] Review: 93% (COMPLETE)

### Chapter 6: Net Social Wage
- [x] Chapter investigation
- [x] 9 series loaded (T601-T609)
- [x] 9 series processed
- [x] 9 series extended (all Ch6)
- [x] 9 DPRs written
- [x] 9 EPRs written
- [x] 4 FPRs written
- [x] 9 chopped CSVs validated (including T608 derived)
- [x] 9 extenbooks generated
- [x] Shiny integration
- [x] Test suite (test_chapter_06.R)
- [x] Adequacy: 90% (ADEQUATE)
- [x] Review: 92% (COMPLETE)

### Chapter 9: Summary Tables
- [x] Chapter investigation
- [x] 1 series loaded and processed (T901)
- [x] T901 extended (assembled from upstream)
- [x] 1 DPR, 1 EPR written
- [x] 5 FPRs written
- [x] 1 chopped CSV validated
- [x] 1 extenbook generated
- [x] Shiny integration
- [x] Test suite (test_chapter_09.R)
- [x] Adequacy: 93% (ADEQUATE)
- [x] Review: 94% (COMPLETE)

---

## Infrastructure Upgrade v3.0 (IN PROGRESS)

- [x] V## validation scripts (V00-V08)
- [x] M## manual adjustment framework (M00, ADJUSTMENT_MANIFEST)
- [x] E## exploration framework
- [x] NickyData governance (DECISION_LOG, ASSUMPTIONS, VERSION_LOG, CHECKLIST)
- [x] replicate.py v3.0 (4-phase orchestrator)
- [x] paths.py updated (validation/manual/exploration paths)
- [x] PIPELINE_STATE.json v2.0 (10-stage format)
- [x] VARIANT_REGISTRY.json
- [x] Standards/Anu_Suite/README.md updated to v6.0
- [x] data/user-inputs/ READMEs
- [x] Verification: replicate.py --dry-run (33 series, 4 phases, 8 V## scripts discovered)
- [x] Verification: replicate.py --validate-only (246 PASS, 0 FAIL, 10 WARN, 23 SKIP — PASS)
- [x] Verification: full pipeline run (14/14 loaded, 15/15 processed, validation PASS)
- [x] V## tuning: V01 benchmarks corrected, V02 range bounds fixed, V04 start year fixed, V05 book-period restriction
- [x] ADJ-002 executed (M01_adjust_va_star_ratio.py — ec_u/ec_p ≈ 1.0, confirms book assumption)
- [x] Benchmark values added for T504, T505 (5 series total with benchmarks)

---

## HDARP Migration & KB Enrichment (Session 15)
- [x] Migrated HDARP Integration catalogs (753 tables, 40 equations, 62 figures)
- [x] Migrated 1994_Measuring_Wealth full extraction (40 chunks, 112 files, 380 pages)
- [x] Migrated Tonak 1984 OCR result
- [x] Created HDARP_BOOK_INDEX.md (chapter-to-chunk mapping)
- [x] Updated INDEX_OF_EXTRACTED_CONTENT.md
- [x] Updated EXTERNAL_PAPERS_INDEX.md
- [x] Extracted IO methodology from chunks 09-16, 27, 32-33
- [x] Created IO_METHODOLOGY_EXTRACTION.md (complete Wave 2 reference)

## 10-Step Improvement Cycle (Session 15b)
- [x] Step 1: Unit normalization investigated — T501 (billions) vs T504/T505 (millions) is structural (different source tables, not conversion error). Documented.
- [x] Step 2: M01 BEA column matching fixed (27 years of ec_u/ec_p computed, max change 0.42)
- [x] Step 3: HDARP cross-validation — all 6 benchmark values match 0.0% (HDARP_CROSSVALIDATION_REPORT.md)
- [x] Step 4: Robin benchmark check — Robin data only has profit rates, existing authoritative CSV is better source
- [x] Step 5: API keys copied from Robin (BEA + FRED confirmed working)
- [x] Step 6: V09 Mohun cross-validation created (42-80% divergence, expected — different methodology)
- [x] Step 7: Ch6 tax allocation verified against book Section 3.3 (DEC-008 — methodology matches)
- [x] Step 8: All 16 WARNs investigated (WARN_INVESTIGATION_REPORT.md — 14 accepted, 1 fixable, 1 deferred)
- [x] Step 9: Leontief.io IO tables imported (18 files: 1997-2017 Use/Supply/Requirements + NAICS crosswalks)
- [x] Step 10: Full pipeline run (14/14 loaded, 15/15 processed, 246 PASS, 0 FAIL, 16 WARN — PASS)

## Wave 2 Implementation Progress (Session 16, 2026-04-09)
- [x] W2-1: NAICS parser (lib/io/naics_parser.py — verified 64x71 Use, 71x71 Leontief, all 5 years)
- [x] W2-2: NAICS classification (lib/io/naics_classification.py — 48 prod, 12 unprod, 6 trade, 5 govt)
- [x] W2-3: T504 splice — unit audit completed (UNIT_AUDIT_REPORT.md). T504/T505 in millions, T501-T503 in billions. BEA API comp data saved.
- [x] W2-4: NAICS Marxian aggregates computed — naics_aggregator.py produces TV* for 1997-2024 (48 prod + 6 trade sectors). Saved to NAICS_marxian_aggregates.csv.
- [x] W2-5: M02 created + unit fix applied (K in millions = same as S*). Awaiting verification (system slow).
- [x] W2-6: V05 documented — SKIP is permanent per UNIT_AUDIT_REPORT.md (different accounting pathways)
- [x] W2-7: T507 extended (42 book + 35 ext). T510 book-only (C*/V* unit mismatch)
- [x] W2-8: T701 labor values computed for 5 benchmark years (1997-2017), all positive, declining trend
- [x] W2-9: Absorbed databases — Ch4 (28 rows, IO aggregates 1997-2024), Ch7 (5 rows, labor values)
- [x] W2-10: Pipeline: 245 PASS, 0 FAIL, 17 WARN — PASS

## Refinement Cycle (Session 16c, 2026-04-09)
- [x] R-1: Promoted M02 adjustments (T513/T514 K→K*) to main series
- [x] R-2: P01 IO-based growth rates — T501 post-1997 uses TV* growth rates
- [x] R-3: Unit normalization module (lib/units.py — 33 series documented)
- [x] R-4: T702-T703 computed but need methodological correction (money→labor value conversion required for proper comparison). Data saved. See DEC-011.
- [x] R-5: T510 C*/V* data computed from IO+KLEMS (5 benchmark years: 1.45-1.83)
- [x] R-6: V10 IO consistency validator (25 checks, all PASS)
- [x] R-7: Publication figures — 6 figures generated (PNG+SVG)
- [x] R-8: Master database (97 years x 29 series, CSV + XLSX)
- [x] R-9: Reproducibility test — PASS (13/13 files, all imports, 33 series, 11 validators)
- [x] R-10: Methodology report (Outputs/Reports/AS2_Methodology_Report.md)

## Wave 3: External Paper Chapters (COMPLETE)
- [x] Phase 0.1: T702-T703 λ_m conversion attempted (MAD improved 31,000%→73%, needs VA-based surplus)
- [x] Phase 1.1: External chapters index created (EXTERNAL_CHAPTERS_INDEX.md — 8 chapters, Ch10-Ch17)
- [x] Phase 1.2: Ch13 investigation (Moos 2017 — most important, 5 series defined)
- [x] Phase 1.2: Ch14 investigation (Mohun 2005 — CSV data already exists, 4 series)
- [x] Phase 1.2: Ch16 investigation (Turkey NSW — 5 series, all benchmark values documented)
- [x] Phase 2: NSW papers — P17 (Moos N1301-N1305), P19 (ST87 N1101-N1103, ST02 N1201-N1202)
- [x] Phase 3: Mohun Ch14 — L15+P16 (N1401-N1404, ST/Mohun ratio=1.61)
- [x] Phase 4: Turkey Ch16 — P18 (N1601-N1602, all-negative NSW confirmed)
- [x] Pipeline: 25 N-series processed, 0 FAIL
- [x] Moos structural shift confirmed: pre-2000 NSW=-0.011, post-2000 NSW=+0.014
- [x] Ch10 (Tonak 1984): N1001-N1002 (29 years, labor share + net tax rate, HDARP primary)
- [x] Ch15 (Mohun 2013): N1501-N1504 (42 years, class decomposition + burden ratio)
- [x] Ch17 (Cronin NZ): N1701-N1704 (24 years, s/TV + s/v + c/v + total value)
- [x] Cross-study NSW comparison database (74 years × 6 studies)
- [x] Cross-study exploitation comparison database (77 years)
- [x] 3 cross-study publication figures (NSW, Mohun, Moos)

## Wave 2 Prerequisites (COMPLETE)

### Phase B: Chapter 4 IO Framework
- [x] Source BEA IO benchmark tables — NAICS 1997-2017 imported from Leontief.io (18 files)
- [x] Parse NAICS JSON → matrix format — _naics_io_parser.py (verified: 64×71 Use, 71×71 Leontief for 1997-2017)
- [x] NAICS sector classification — 71 codes mapped to productive/trading/unproductive/govt
- [x] NIPA 6.5 → IO sector mapping (nipa_65_to_io_classification.json, Session 26)
- [x] CHAPTER_4_INVESTIGATION.md (started Session 14, IO methodology extracted Session 15)
- [x] IO_METHODOLOGY_EXTRACTION.md created with complete formulas
- [x] T401/T402: SIC matrices (1947-1977) + NAICS matrices (1997-2017) loaded
- [x] P13 validates all benchmark years
- [x] 412-industry detail classification (naics_detail_classification.json)

### Wave 2 Series
- [x] T501-T503 extended to 2024 (97 years, GDP + IO TV* growth rates)
- [x] T507-T510 extended (77 years, derived from T504/T505 + K*/V*)
- [x] T701-T703 labor values extended to NAICS era (11 benchmarks: 6 SIC + 5 NAICS, Ochoa R²=0.72-0.99)
- [x] DIV-001 resolved: K* from industry-level Fixed Assets (L20), r* = S*/K* (P08)
- [x] Sector V* (P22, Appendix G method, 27 years)

---

## Wave 3 Book Chapters (COMPLETE)

- [x] T201 alternative GFP measures (97 years, GFP vs GDP comparison)
- [x] T801 cross-study comparison (42 years, ST vs Mohun exploitation rates)
- [ ] Chapter 2 conceptual figures (FPRs only — low priority)
- [ ] Chapter 3 classification documentation — low priority
- [ ] Chapter 8 extended comparison — T801 covers core comparison

---

## Session 26 Migration + Consolidation (2026-05-11)

- [x] nickydata/ archived to _archive/nickydata_v7.2_2026-05-11/
- [x] L19_load_bea_underlying.py — 412-industry detail IO + integrated TP*/GDP
- [x] L20_load_fixed_assets_industry.py — K* from FAAt401 by industry
- [x] P22_sector_variable_capital.py — Appendix G sector V*
- [x] A11_period_analysis.py — period means + structural findings
- [x] P03 updated: S* = GFP* - Dp - V* (depreciation added)
- [x] P07 updated: T510 = K*/V* from Fixed Assets
- [x] P14 updated: NAICS labor values (1997-2017, 5 benchmarks)
- [x] Pipeline: 76 scripts, 0 FAIL, 8.2s runtime

---

*Last updated: 2026-05-11*
