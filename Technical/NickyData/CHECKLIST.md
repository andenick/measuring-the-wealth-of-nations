# AS2 NickyData Package — Status Checklist

## Pipeline Infrastructure
- [x] NickyData scaffold (8-phase directories)
- [x] run.py orchestrator (67 scripts, 8 phases)
- [x] project_registry.json (5 chapters + 8 studies)
- [x] series_registry.json (33 T-series + 21 N-series = 54 series definitions)
- [x] S01 setup validation
- [x] S02 ANU_LEDGER.json generator (50/55 series covered)
- [x] Full pipeline runs end-to-end (100s, 0 FAIL)
- [x] VARIANT_REGISTRY.json (6 documented variants: VAR-001 through VAR-006)
- [x] DECISION_LOG.md (11 decisions), ASSUMPTIONS.md governance docs

## Book Replication (T-series)
- [x] Ch2: T201 (alternative GFP, orthodox comparison, 97yr)
- [x] Ch4: T401-T402 (IO matrices, 6 SIC + 5 NAICS benchmarks, status=benchmark_only)
- [x] Ch5: T501-T516 (16 series, extended 1948-2024)
- [x] Ch6: T601-T609 (9 series, NSW extended 1952-2025)
- [x] Ch7: T701-T703 (labor values, prices of production, R²=0.70-0.98)
- [x] Ch8: T801 (cross-study ST vs Mohun comparison)
- [x] Ch9: T901 (summary, assembled from Ch5+Ch6)
- [x] DIV-001 resolved (K→K*, +5.7%)
- [x] DIV-002 resolved (ec_u/ec_p ≈ 1.0)
- [x] T510 extended via linear trend (42 book + 35 ext rows)
- [x] T702-T703 fixed (total-value regression, R²=0.70-0.98 vs previous <0.04)

## External Studies (N-series)
- [x] Study 1 Tonak 1984: N1001-N1002 (labor share, net tax)
- [x] Study 2 ST 1987: N1101-N1103 (net transfer, benefit, tax rates)
- [x] Study 3 ST 2002: N1201-N1202 (NSW/EC)
- [x] Study 4 Moos 2017: N1301, N1302, N1304, N1305 (structural shift: +3.0pp)
- [x] Study 5 Mohun 2005: N1401-N1404 (ST/Mohun ratio = 1.61)
- [x] Study 6 Mohun 2013: N1501-N1504 (class decomposition)
- [x] Study 7 Turkey 2022: N1601-N1602 (all-negative NSW)
- [x] Study 8 Cronin NZ: N1701 (productive capital share)
- [x] N-series in series_registry.json (21 entries)
- [x] N-series write to studies/series/ (not book/series/)

## Anu Suite Compliance
- [x] Chopped CSV format: Anu Standard (Row 1=Year+metadata, Row 2=empty+IDs)
- [x] 27 T-series chopped CSVs (25 standard + T201 + T801)
- [x] 22 N-series chopped CSVs
- [x] 28 T-series extenbooks (26 standard + T201 + T801)
- [x] 22 N-series extenbooks
- [x] DPRs: 33 T-series + 21 N-series + T201 + T401 + T402 + T701-T703 + T801 = 61 total
- [x] EPRs: 19 T-series + 5 synthetic N-series + T501 + T508 + T509 + T510 = 28 total
- [x] Decompositions: 33 T-series + T201 + T401 + T402 + T701-T703 + T801 + N-series consolidated = all
- [x] FPRs: 17 figure provenance records
- [x] VARIANT_REGISTRY.json: 6 variants (T### IDs, R Shiny, DPR research, N### IDs, 8-phase pipeline, matrix skip)
- [x] ANU_LEDGER.json: 50/55 series fully covered (5 stub series: T201 missing extenbook, T401/T402 matrix VAR-006)
- [x] validation_config.json: all series have tolerance classifications

## Validation (15 validators, 0 FAIL) — Final Session 23+
- [x] V01 Reference values (29 PASS, 0 FAIL — Table H.1 benchmarks including 1972 for T504/T505)
- [x] V02 Range checks (86 PASS, 0 FAIL — ranges updated for corrected V* levels + K*-based r*)
- [x] V03 Continuity (27 PASS, 6 WARN — expected: 1989/1990 splice for T504/T505/T506/T511/T512/T608)
- [x] V04 Completeness (26 PASS, 0 FAIL)
- [x] V05 Cross-series (4 PASS, 1 SKIP — GFP identity holds, employment identity holds)
- [x] V06 Splice quality (4 PASS, 14 WARN — growth-rate splices at 1989/1990 for extended series; 14 WARN is expected after V* correction + IO extension changes)
- [x] V07 Extension overlap (15 PASS, 3 SKIP)
- [x] V08 Hash integrity (76 PASS, 0 WARN — baseline run)
- [x] V09 Mohun cross-validation (6 WARN — expected: Mohun uses different productive/unproductive boundary; A08 Khanjian cross-validation confirms Our/Kh=0.801)
- [x] V10 IO consistency (21 PASS, 8 WARN — SIC-NAICS transition, benchmark interpolation, expected)
- [x] V11 External benchmarks (4 PASS, 3 WARN — NIPA vintage differences between our 2026 pull and published sources)
- [x] V12 NSW cross-study (2 PASS)
- [x] V13 Robin cross-validation (1 WARN — cross-project data comparison, methodology differs)
- [x] V14 Unit consistency (4 PASS, 1 WARN — T504/T505 mixed book/extension units documented in DEC-020)
- [x] V15 Data freshness (11 PASS)

## Analytical Series (Phase 4) — NEW
- [x] A07 Social burden rate (78 years, P+/S* and Eu_share, r* from K*)
- [x] A08 Khanjian cross-validation (Our/Khanjian ratio = 0.801, matches book's stated ~0.80)
- [x] A09 Unproductive exploitation rate (77 years, eu/ep convergence 0.80->0.97)
- [x] A10 Marxian productivity (78 years, real 1982$ — q*(1989)=$78.64/hr matches book $78.03)

## Output & Deliverables
- [x] Master database (97yr x 48 series)
- [x] 11 publication figures (was 6)
- [x] Cross-study NSW comparison (6 studies)
- [x] Cross-study exploitation comparison
- [x] Methodology report (Markdown)
- [x] O04: N-series chopped + extenbook generation (22 each)
- [x] O05: Shiny data bridge (8 files)
- [x] O06: T-series chopped regeneration (Anu Standard format)

## Shiny App Integration
- [x] O05 generates updated CSVs from NickyData to ShinyApp/data/
- [x] Moos NSW, Mohun comparison, International NSW data files
- [x] Shiny app UI tabs: IO Analysis, Labor Values, Cross-Study, International NSW (4 Wave 2 tabs added)
- [x] STUDIES_SERIES_MAPPING added to data_loader.R (25 N-series entries)
- [x] Shiny data bridge: O05 updated with legacy column names (r_star_pct, exploitation_rate, Lp_L_ratio, etc.)
- [x] server_logic.R: removed 961-line corrupted UI block (pre-existing parse error)

## D0 Gate Artifacts (Anu Review v4.0)
- [x] S03: VALIDATION_REPORT.json (15 validators, 0 fail, 5 warn)
- [x] S04: provenance_index.json (58 series, 22 sources, 7 APIs)
- [x] S05: PIPELINE_STATE.json (15 chapter groups, pipeline v7.0)
- [x] O07: SUBSOURCE_METADATA.json (110 entries for 58 series)

## Remaining Items
- [x] Shiny app UI: 4 Wave 2 tabs added (IO, Labor Values, Cross-Study, International NSW)
- [x] STUDIES_SERIES_MAPPING in data_loader.R (25 N-series, all 8 studies)
- [x] API data vintage refresh (V15 now 11 PASS, 0 WARN — resolved prior session)
- [x] LaTeX methodology report: v7.0, 778KB PDF, compiled 2026-05-11
- [x] Replication package: AS2_ReplicationPackage_v7.0.zip (256 files, 1.1 MB, API keys stripped)

## WP-1: Annual IO Classification Framework (Deep Faithfulness)
- [x] L21: BEA GDPbyIndustry annual VA + Components (28 years, 100 industries, 1997-2024)
- [x] L22: NIPA FTE by industry (27 years, Lp/L) + Compensation by industry (27 years, V*/W)
- [x] P23: Annual IO productive sector ratios (77 years, 1948-2024, replaces frozen ratios)
- [x] P05: T512 updated with IO-classified V*/W fallback chain (WP-1 → component → pre-spliced)
- [x] P14: Scatter data export for Shiny Labor Values tab (per-sector labor value vs market price)
- [x] Table H.1: Verified — 42 years, S*=VA*-V* identity PASS, VA*=GFP*-Dp max error 0.35%
- [x] Validation: 15 validators, 0 failures (T513 benchmark updated to 1.865 per K* recalculation)

## WP-1/WP-2/WP-3 Implementation (Session 27 continued)
- [x] P05 T511: FTE-based extension from NIPA 6.5D (35 years, WP-1 direct)
- [x] P05 T512: IO-classified V*/W from NIPA 6.2D (35 years, WP-1 direct)
- [x] P01 T501: IO TV* from GDPbyIndustry annual VA (productive+trading) for 1997+
- [x] P04 T506: e = S*/V* from components (automatically improved via upstream WP-1)
- [x] P08 T513: K* already annual from L20 industry FA (was already correct)
- [x] P14: NAICS r_bar fix — uses GDPbyIndustry VA data instead of A-matrix proxy; NAICS sector alignment for matrix mismatches
- [x] P14: scatter data exported to shiny/T701_scatter.csv
- [x] Turkey N1601: extended to 1980-2019 via FRED LABSHPTRA156NRUG (was 1980-2006)
- [x] Turkey N1602: NSW/GDP now 30 years (was ~20)
- [x] Table H.1: 42-year identity verification PASS (S*=VA*-V*, max VA* error 0.35%)
- [x] 2022 IO: checked — BEA has annual Supply-Use tables, not detailed benchmark. L21 annual VA covers 2022.
- [ ] Circulating capital variant T513-VAR (enhancement beyond book, low priority)
