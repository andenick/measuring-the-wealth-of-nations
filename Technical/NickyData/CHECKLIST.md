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

## Validation (15 validators, 0 FAIL)
- [x] V01 Reference values (26 PASS)
- [x] V02 Range checks (88 PASS)
- [x] V03 Continuity (29 PASS, 4 WARN)
- [x] V04 Completeness (26 PASS)
- [x] V05 Cross-series (2 PASS, 1 SKIP)
- [x] V06 Splice quality (7 PASS, 7 WARN, 4 SKIP)
- [x] V07 Extension overlap (11 PASS, 7 SKIP)
- [x] V08 Hash integrity (75 PASS, 1 WARN)
- [x] V09 Mohun cross-validation (6 WARN — expected methodology divergence)
- [x] V10 IO consistency (21 PASS, 8 WARN)
- [x] V11 External benchmarks (5 PASS, 1 WARN)
- [x] V12 NSW cross-study (2 PASS)
- [x] V13 Robin cross-validation (1 WARN)
- [x] V14 Unit consistency (4 PASS, 1 WARN)
- [x] V15 Data freshness (8 PASS, 2 WARN)

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
- [ ] Shiny app UI tabs for IO analysis, labor values, cross-study (pending R development)
- [ ] CH6_SERIES_MAPPING, STUDIES_SERIES_MAPPING in data_loader.R

## Remaining Items
- [ ] Methodology report: convert to LaTeX/PDF (Druck standard)
- [ ] Shiny app UI: new tabs for NSW, IO, cross-study, international
- [ ] API data vintage refresh (V15 WARNs: 2 sources >12 months old)
- [ ] Replication package for Zenodo/Harvard Dataverse
