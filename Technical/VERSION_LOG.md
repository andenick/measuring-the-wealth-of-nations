# AS2 Version Log

Evolutionary version history of the AS2 project, following the snake-shedding model.

---

## v7.0.0 — Pipeline Consolidation + NAICS Extension (2026-05-11)

**Scope**: Merge nickydata/ innovations into code/ pipeline, NAICS labor values, K* from Fixed Assets, archive dual implementation

**Changes**:
- **Migration**: nickydata/ v7.2 archived; all innovations ported to code/ pipeline
  - L19: 412-industry detail IO (UnderlyingGDPbyIndustry) + integrated TP*/GDP series
  - L20: K* from Fixed Assets by industry (FAAt401 classified by sector)
  - P22: Sector-level V* per Appendix G (16 productive sectors, BLS CES + NIPA 6.2D/6.5D)
  - A11: Period analysis (8 canonical eras) + structural findings JSON
- **P03**: S* = GFP* - Dp - V* (depreciation from book H.1 + GFP-growth extension)
- **P07**: T510 = K*/V* from industry Fixed Assets (replaces linear trend)
- **P14**: NAICS labor values for 1997-2017 (5 benchmarks, Ochoa R²=0.85-0.99)
- **P08**: K*-based r* = S*/K* using L20 output
- **Config**: nipa_65_to_io_classification.json (23 NIPA 6.5D lines classified)
- **Cleanup**: 5 diagnostic scripts deleted, bea_gdpbi dead fetch removed, methodology.json S* formula corrected, 4 hardcoded constants extracted to config
- **Validation**: All V01-V05 fixes confirmed in place, 0 FAIL across 15 validators
- Pipeline: 76 scripts, 0 FAIL, 8.2s runtime, single canonical implementation

---

## v6.0.0 — NickyData Architecture (2026-04-09)

**Scope**: Complete restructuring to NickyData v1.1, pipeline verification, validation enrichment

**Changes**:
- Migrated from ANU_REPLICATOR to NickyData architecture (8-phase: S/L/P/V/M/A/O/E)
- Created run.py orchestrator (57 scripts discovered, all 8 phases)
- Fixed import paths (lib→utils, 4 critical + 55 code files)
- Created project_registry.json (5 book chapters + 8 external studies)
- External papers renamed from "Chapters 10-17" to "Studies 1-8"
- Book series in data/final-data/book/, studies in data/final-data/studies/
- Created S01 setup validation, A01-A04 analysis scripts
- Created V11 external benchmark validator (5 PASS — Turkey, Mohun, Moos, Tonak)
- T702-T703 r_bar improved from 4-6 to 1.5-2.5 (VA-based surplus)
- Fresh CHECKLIST.md for NickyData
- Study DPRs written (8 studies documented)
- Pipeline: 11 validators, 0 FAIL, full end-to-end in 51s
- Previous version archived at _archive/v5.0_2026-04-09/

---

## v5.0.0 — External Paper Chapters + Cross-Study Analysis (2026-04-09)

**Scope**: 8 external paper chapters (Ch10-Ch17), 20+ new series, cross-study comparison

**Changes**:
- 8 external paper chapters defined (EXTERNAL_CHAPTERS_INDEX.md)
- Ch10 (Tonak 1984): N1001-N1002 (labor share, net tax rate, 29 years)
- Ch11 (ST 1987): N1101-N1103 (net transfer, benefit, tax rates, 34 years)
- Ch12 (ST 2002): N1201-N1202 (NSW/GDP, NSW/EC, 46 years)
- Ch13 (Moos 2017): N1301-N1305 (NSW/GDP, NSW/EC, structural shift confirmed: pre-2000=-1.1%, post-2000=+1.4%)
- Ch14 (Mohun 2005): N1401-N1404 (exploitation, productive labor, ST/Mohun ratio=1.61)
- Ch15 (Mohun 2013): N1501-N1504 (unproductive labor class decomposition, burden ratio)
- Ch16 (Turkey 2022): N1601-N1602 (labor share, NSW — ALL 40 years negative, -1.1% mean)
- Ch17 (Cronin NZ 2001): N1701 (productive capital share, post-1984 reform decline)
- Cross-study NSW comparison database (6 studies, 74 years)
- Cross-study exploitation comparison database (77 years)
- Pipeline: 20 processed series, 263 PASS, 0 FAIL
- New scripts: L15, P16-P20, O03

---

## v4.1.0 — Refinement Cycle + Deliverables (2026-04-09)

**Scope**: Adjustment promotion, IO validation, master database, methodology report

**Changes**:
- M99: T513/T514 K→K* adjustments promoted to main series
- lib/units.py: 33 series units documented with conversion functions
- V10: IO consistency validator (25 checks, all PASS — A-matrix, Leontief, classification)
- O02: Master database generated (97 years x 29 series, CSV + XLSX)
- Methodology report written (Outputs/Reports/AS2_Methodology_Report.md)
- Pipeline: 10 validators, 261 PASS, 0 FAIL

---

## v4.0.0 — Wave 2 Implementation (2026-04-09)

**Scope**: NAICS IO integration, divergence resolution, labor values, series extension

**Changes**:
- NAICS parser, classification, aggregator: 3 new modules in lib/io/
- DIV-001 RESOLVED: M02 adjusts r* by +2.5-7.9% (financial sector capital exclusion)
- DIV-002 already resolved (Session 15): M01 confirms ec_u/ec_p ≈ 1.0
- T507 extended to 2024 (surplus ratio derived from T504/T505)
- T701 labor values computed for 5 NAICS benchmark years (1997-2017)
- Unit audit completed: T504/T505 in millions, T501-T503 in billions (documented)
- BEA API compensation data fetched (97 years, 1929-2025)
- NAICS Marxian aggregates: productive GO for 1997-2024
- Both ADJUSTMENT_MANIFEST pending items resolved (0 pending)
- Pipeline: 245 PASS, 0 FAIL, 17 WARN

---

## v3.3.0 — Wave 2 Infrastructure (2026-04-09)

**Scope**: NAICS IO parser + sector classification for Wave 2

**Changes**:
- Created `lib/io/naics_parser.py` — parses BEA InputOutput API JSON into pandas DataFrames
  - Functions: parse_bea_io_json, extract_use_matrix, extract_leontief, get_sector_labels, compute_technical_coefficients_naics, compute_leontief_inverse_naics
  - Verified: 64×71 Use matrix, 71×71 Leontief inverse for all 5 benchmark years (1997-2017)
- Created `lib/io/naics_classification.py` — NAICS sector classification
  - 71 NAICS codes mapped to productive/trading/unproductive/govt following Appendix B
  - Functions: classify_naics_sectors, get_productive_sector_codes, save_classification_csv
- All 10 improvement cycle steps completed (Steps 1-10 from previous plan)
- Wave 2 Steps 1-2 of 10 complete; Steps 3-10 ready for implementation

---

## v3.2.0 — 10-Step Improvement Cycle (2026-04-08)

**Scope**: Data accuracy improvements, validation enrichment, Wave 2 data acquisition

**Changes**:
- Fixed M01 BEA column matching — now computes ec_u/ec_p from 27 years of actual NIPA 6.2D data (max change 0.42 vs constant assumption)
- API keys copied from Robin (BEA, FRED, BLS confirmed working)
- Created V09_mohun_crossvalidation.py — automated cross-study comparison (42-80% expected divergence)
- Imported 18 NAICS IO table files from Leontief.io (1997-2017: Use, Supply, Total Requirements)
- Copied ISIC-NAICS crosswalks from Leontief.io to Inputs/Concordances/
- Full pipeline verification: 14/14 loaded, 15/15 processed, 246 PASS, 0 FAIL, 16 WARN
- Documented unit mismatch finding (T501 billions vs T504/T505 millions — structural, different source tables)

---

## v3.1.0 — HDARP Migration + KB Enrichment (2026-04-08)

**Scope**: Migrate complete book HDARP extraction + IO methodology research

**Changes**:
- Migrated HDARP Integration catalogs from Shaikh Tonak (753 tables, 40 equations, 62 figures)
- Migrated full 1994_Measuring_Wealth extraction (40 chunks, 380 pages, 112 files)
- Migrated Tonak 1984 OCR result to external_papers/
- Created HDARP_BOOK_INDEX.md for chapter-to-chunk navigation
- Updated INDEX_OF_EXTRACTED_CONTENT.md and EXTERNAL_PAPERS_INDEX.md
- Extracted complete IO methodology from chunks 09-16, 27, 32-33
- Created IO_METHODOLOGY_EXTRACTION.md (formulas, sector classification, NIPA references)
- KB coverage: 47% → 95%+ (all chapters now accessible via HDARP extraction)

---

## v3.0.0 — Infrastructure Upgrade (2026-04-08)

**Scope**: Full Anu Suite v6.0 alignment + NickyData governance integration

**Changes**:
- Added V## validation phase (V00-V08: reference values, range checks, continuity, completeness, cross-series, splice quality, extension overlap, hash integrity)
- Added M## manual adjustment phase (M00 orchestrator, ADJUSTMENT_MANIFEST.json)
- Added E## exploration phase (migrated _test_wave3.py to E01)
- Upgraded replicate.py from v1.0 to v3.0 (4-phase: L/P/V/M + new CLI flags)
- Upgraded PIPELINE_STATE.json from v1.1 to v2.0 (10-stage format)
- Created DECISION_LOG.md (6 backfilled entries)
- Created ASSUMPTIONS.md (8 categorized assumptions)
- Created CHECKLIST.md (Wave 1/2/3 progress tracking)
- Created VARIANT_REGISTRY.json (3 project variants)
- Updated Standards/Anu_Suite/README.md (v2.2 to v6.0)
- Organized data/user-inputs/ with READMEs

---

## v2.1.0 — Wave 1 Polish (2026-03-30, Session 14)

**Scope**: Phase A implementation + Phase B start

**Changes**:
- Anu Review v4.0: scored Ch5=93%, Ch6=92%, Ch9=94%, Project=93%
- Fixed 9 PIPELINE_STATE.json extension flag mismatches
- T504 gap interpolation (1990-1997)
- marxian_accounts.py: year-varying VA*/W support (DIV-002 partial fix)
- L08/P10 extended for T605/T606 (1952-2025)
- TOLERANCE_THRESHOLDS.md created
- Inputs/ flattened (Druck compliant)
- 11 HDARP narrative chunks added to KB (188->199 files)
- CHAPTER_4_INVESTIGATION.md started (Phase B)

---

## v2.0.0 — Wave 1 Complete (2026-03-22, Sessions 10-13)

**Scope**: All 26 Wave 1 series through full pipeline

**Changes**:
- Chapter 9 completed (T901 summary assembly)
- All 26 chopped CSVs validated
- All 26 extenbooks generated
- 17 FPRs completed
- Adequacy reports: Ch5=91, Ch6=90, Ch9=93
- Anu Review v3.6: project score 94.39%

---

## v1.5.0 — Chapter 6 Complete (2026-03-20, Sessions 7-9)

**Scope**: Net Social Wage chapter

**Changes**:
- 9 Chapter 6 series (T601-T609) through full pipeline
- NSW comparison review (Cronin NZ, Karabacak Turkey)
- 4 Ch6 FPRs
- External papers integrated (Cronin 2001, Karabacak-Tonak 2022)

---

## v1.2.0 — Chapter 5 Extensions (2026-02-25, Sessions 5-6)

**Scope**: Extension of Chapter 5 series to 2024

**Changes**:
- 9 series extended (T504-T506, T511-T516) with BEA/BLS API data
- 9 EPRs created with faithfulness scoring
- EXTENSION_LOG.json initialized
- api_config.json created
- data_coverage_matrix.csv created

---

## v1.0.0 — Chapter 5 Replication (2026-02-24, Sessions 3-4)

**Scope**: Anu Replicator built, Ch5 book-period data replicated

**Changes**:
- ANU_REPLICATOR scaffold (L00-L10, P00-P12, lib/, config/)
- 16 Chapter 5 series replicated (1948-1989)
- series_registry.json created (33 entries)
- 16 DPRs, 8 FPRs
- Shiny app migrated and functional (11 tabs)
- replicate.py v1.0 (L+P phases)
- Benchmark validation: 93.8% match with Table 5.8

---

## v0.5.0 — Phase 0 + Investigations (2026-02-23, Sessions 1-2)

**Scope**: Project scaffold, intelligence gathering

**Changes**:
- Directory scaffold (Druck-compliant 3-folder structure)
- 5 Phase 0 anchor documents (North Star, Artifact Atlas, Chapter Matrix, Gap Register, Method Contract)
- 3 chapter investigations (Ch5, Ch6, Ch9) at NIPA-line-item depth
- Data migration from Shaikh Tonak project
- Anu Suite v2.2 ported from CD2
- T_SERIES_CATALOG.json, ANU_CHOPPED_CATALOG.json, DIVERGENCE_REGISTER.json initialized

---

*Last updated: 2026-04-08*
