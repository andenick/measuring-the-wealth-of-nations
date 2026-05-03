# AS2 Artifact Atlas

**Purpose**: Canonical inventory of every artifact relevant to the AS2 replication and extension package for Shaikh & Tonak (1994) *Measuring the Wealth of Nations*.

**Scope**: Maps the full corpus from the existing `Shaikh Tonak` project into a navigable reference for AS2 development. Every artifact is classified by type, indexed by canonical path, and cross-referenced to its chapter/series/table dependencies.

**Version**: 1.0 (Phase 0)
**Date**: February 23, 2026

---

## 1. Artifact Taxonomy

| Code | Type | Description |
|------|------|-------------|
| SRC | Source Data | Read-only originals in Inputs/ |
| KB | Knowledge Base | HDARP extractions (text, tables, figures, equations) |
| CAT | Catalog | JSON/CSV catalogs mapping series, tables, subsources |
| SCR | Script | Python/R processing and validation scripts |
| STD | Standard | Anu Suite templates, validation scripts, methodology specs |
| DOC | Documentation | Investigations, methodology notes, handoffs |
| APP | Application | Shiny app code and runtime assets |
| OUT | Output | Deliverables, Extenbooks, reports, PDFs |

---

## 2. Primary Source Corpus (SRC)

### 2.1 The Book

| Artifact | Original Path | Format | Notes |
|----------|--------------|--------|-------|
| Full book (page images) | `Shaikh Tonak/shaikh_tonak_1994/page_images/` | 227 MB of page scans | HDARP processing complete |
| Extracted text (50+ pages) | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/text/` | Markdown per page | OCR complete |
| Extracted tables | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/tables/` | CSV | 9+ tables extracted |
| Extracted equations | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/equations/` | LaTeX/TeX | 8+ equation files |

### 2.2 Authoritative Datasets (from Shaikh Tonak project)

| Artifact | Original Path | AS2 Target | Format | Notes |
|----------|--------------|------------|--------|-------|
| Exploitation rate 1948-1989 | `Shaikh Tonak/Technical/data/authoritative_shaikh_tonak/*1948_1989.csv` | `Inputs/BookTables/ch05/` | CSV (8.3K) | Book-period replication |
| Exploitation rate 1948-2024 | `Shaikh Tonak/Technical/data/authoritative_shaikh_tonak/*1948_2024.csv` | `Inputs/BookTables/ch05/` | CSV (11K) | Extended series |
| IO matrices (A, L, Z) | `Shaikh Tonak/Technical/data/IO_Matrices/` | `Inputs/IO_Matrices/` | CSV (1.3 MB) | 6 benchmark years: 1947, 1958, 1963, 1967, 1972, 1977 |
| NIPA book period | `Shaikh Tonak/Technical/data/NIPA_Book_Period/` | `Inputs/NIPA/` | CSV + Parquet (96K) | Core NIPA variables 1948-1989 |
| Mohun comparison | `Shaikh Tonak/Technical/data/Mohun/` | `Inputs/ExternalSources/Mohun/` | CSV (252K) | 16 files: employment, exploitation, wages |
| SIC-NAICS concordance | `Shaikh Tonak/Technical/Phase3_Replication/data/Concordances/` | `Inputs/Concordances/` | CSV (16K) | IO-85 to NIPA-13 mapping |

### 2.3 Tonak Benchmark Sources

| Artifact | Original Path | AS2 Target | Notes |
|----------|--------------|------------|-------|
| Shaikh & Tonak (2002) Rise and Fall of Welfare State | `Shaikh Tonak/Knowledge_Base/FromTonak/` | `Inputs/ExternalSources/Tonak_Benchmarks/` | 8.6 MB PDF |
| Shaikh & Tonak (1987) Myth of Social Wage | `Shaikh Tonak/Knowledge_Base/FromTonak/` | `Inputs/ExternalSources/Tonak_Benchmarks/` | 5.2 MB PDF |
| NSW comparisons (EAT/NA) | `Shaikh Tonak/Knowledge_Base/FromTonak/NSWComparisons-EAT_NA.docx` | `Inputs/ExternalSources/Tonak_Benchmarks/` | 686K docx |
| Appendix N sources | `Shaikh Tonak/Knowledge_Base/FromTonak/Appendix N_Sources.docx` | `Inputs/ExternalSources/Tonak_Benchmarks/` | 15K docx |

### 2.4 BEA IO Methodology (Reference)

| Artifact | Original Path | Notes |
|----------|--------------|-------|
| BEA 1947 IO Benchmark | `Shaikh Tonak/Inputs/BEA_1947_IO_Benchmark.pdf` | 3.3 MB |
| BEA 1958 IO Benchmark | `Shaikh Tonak/Inputs/BEA_1958_IO_Benchmark_Goldman.pdf` | 12 MB |
| BEA 1963 IO Benchmark | `Shaikh Tonak/Inputs/BEA_1963_IO_Benchmark.pdf` | 14 MB |
| BEA 1967 IO Benchmark | `Shaikh Tonak/Inputs/BEA_1967_IO_Benchmark.pdf` | 15 MB |
| BEA 1977 IO Benchmark | `Shaikh Tonak/Inputs/BEA_1977_IO_Benchmark.pdf` | 19 MB |
| BEA 2024 NIPA Handbook | `Shaikh Tonak/Inputs/BEA_2024_NIPA_Handbook.pdf` | 4.4 MB |
| NBER SIC-NAICS Concordance | `Shaikh Tonak/Inputs/NBER_SIC_NAICS_Concordance.pdf` | 403K |

*Note: BEA PDFs remain in Shaikh Tonak/Inputs/ as reference-only. Too large to copy; reference by path.*

---

## 3. Knowledge Base (KB)

### 3.1 Book Extraction (HDARP)

| Artifact | Original Path | AS2 Target | Notes |
|----------|--------------|------------|-------|
| Page text (50+ files) | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/text/` | `Technical/Knowledge_Base/text/` | Markdown per page |
| Tables (9+ CSV) | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/tables/` | `Technical/Knowledge_Base/tables/` | Extracted data tables |
| Equations (8+ files) | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/equations/` | `Technical/Knowledge_Base/equations/` | LaTeX format |
| Figures (3+ files) | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/figures/` | `Technical/Knowledge_Base/figures/` | Markdown descriptions |
| Content index | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/INDEX_OF_EXTRACTED_CONTENT.md` | `Technical/Knowledge_Base/` | Master index |
| Key findings | `Shaikh Tonak/shaikh_tonak_1994/extracted_content/SUMMARY_KEY_FINDINGS.md` | `Technical/Knowledge_Base/` | Research summary |

### 3.2 HDARP Extractions

| Artifact | Path | Notes |
|----------|------|-------|
| HDARP extractions (18 MB) | `Shaikh Tonak/Knowledge_Base/HDARP_Extractions/` | 23/51 documents processed |
| Tonak/Moos materials (43 MB) | `Shaikh Tonak/Knowledge_Base/TonakMoos/` | Comparative analysis |
| Tonak (1984) dissertation | `Shaikh Tonak/Knowledge_Base/[1984] Tonak...` | 19 MB, processed |
| Cronin (2001) | `Shaikh Tonak/Knowledge_Base/[2001] Cronin...` | 2.9 MB, processed |

---

## 4. Catalogs (CAT)

### 4.1 To Be Created for AS2

| Catalog | Target Path | Purpose |
|---------|------------|---------|
| ANU_CHOPPED_CATALOG.json | `Technical/` | Master catalog of all Anu Chopped CSVs |
| T_SERIES_CATALOG.json | `Technical/` | All T-series with chapter, table, source mapping |
| FIGURE_CATALOG.json | `Technical/` | All figures with series dependencies |
| TRANSFORMATION_LOG.json | `Technical/` | Running log of all data operations |
| DIVERGENCE_REGISTER.json | `Technical/` | Splice failures and resolutions |

### 4.2 Existing Shaikh Tonak Data Assets

| Asset | Path | Notes |
|-------|------|-------|
| Shiny app data (15 CSV) | `Shaikh Tonak/Technical/ShinyApp/data/` | Includes employment, exploitation, profit rates |
| Validation targets | `Shaikh Tonak/Technical/data/Validation_Targets/` | Book-match benchmarks |
| Data inventory | `Shaikh Tonak/Technical/data/DATA_INVENTORY.md` | Comprehensive data listing |
| Data series registry | `Shaikh Tonak/Technical/data/DATA_SERIES_REGISTRY.md` | Time series documentation |

---

## 5. Standards and Methodology (STD)

All at `AS2/Technical/Standards/Anu_Suite/` (ported from CD2, project-agnostic).

### 5.1 Anu Suite Components

| Component | Path | Purpose |
|-----------|------|---------|
| anu-standard | `anu-standard/` | DPR/FPR creation, compliance validation |
| anu-extension | `anu-extension/` | EPR, 10-step extension workflow, divergence handling |
| anu-chopped | `anu-chopped/` | CSV format specification for machine-readable data |
| anu-extenbook | `anu-extenbook/` | Excel Extenbook generation (Sheet 1: data, Sheet 2: provenance) |
| anu-review | `anu-review/` | 8-dimension chapter review and scoring |
| Unified Standard | `ANU_STANDARD_UNIFIED.md` | v2.2 consolidated specification |

### 5.2 Key Templates

| Template | Component | Use |
|----------|-----------|-----|
| DPR_TEMPLATE.md | anu-standard | Data Provenance Record |
| FPR_TEMPLATE.md | anu-standard | Figure Provenance Record |
| EPR_TEMPLATE.md | anu-extension | Extension Provenance Record |
| TRANSITION_ANALYSIS_TEMPLATE.md | anu-extension | Splice quality analysis |
| REVIEW_REPORT_TEMPLATE.md | anu-review | Chapter review |

---

## 6. Scripts (SCR)

### 6.1 Migrated from Shaikh Tonak Phase 3

| Script | Original Path | AS2 Target | Purpose |
|--------|--------------|------------|---------|
| marxian_variable_calculator.py | `Phase3_Replication/src/` | `scripts/calculate/` | Core Marxian calculations |
| calculate_hp_coefficients.py | `Phase3_Replication/src/` | `scripts/calculate/` | HP filter coefficients |
| calculate_lambda_star.py | `Phase3_Replication/src/` | `scripts/calculate/` | Lambda* calculations |
| calculate_sector_employment.py | `Phase3_Replication/src/` | `scripts/calculate/` | Sector employment |
| week3_employment_tables.py | `Phase3_Replication/src/` | `scripts/calculate/` | Employment tables |
| week4_variable_capital.py | `Phase3_Replication/src/` | `scripts/calculate/` | Variable capital (v) |
| week5_surplus_value.py | `Phase3_Replication/src/` | `scripts/calculate/` | Surplus value (s) |
| week6_integration_validation.py | `Phase3_Replication/src/` | `scripts/validate/` | Cross-validation |
| io_matrix_inversion.py | `Phase3_Replication/src/` | `scripts/calculate/` | IO matrix operations |
| create_final_deliverables.py | `Phase3_Replication/src/` | `scripts/calculate/` | Output generation |
| validate_all_prototype_outputs.py | `Phase3_Replication/src/` | `scripts/validate/` | Validation suite |

### 6.2 To Be Created for AS2

| Script | Target Path | Purpose |
|--------|------------|---------|
| ingest_nipa.py | `scripts/ingest/` | NIPA table ingestion from BEA API |
| ingest_bls.py | `scripts/ingest/` | BLS employment data ingestion |
| ingest_io.py | `scripts/ingest/` | BEA IO table ingestion |
| extend_ch05.py | `scripts/extend/` | Chapter 5 series extension |
| extend_ch06.py | `scripts/extend/` | Chapter 6 NSW extension |

---

## 7. Application (APP)

### 7.1 Shiny App (Migrated from Shaikh Tonak)

| Component | Original Path | AS2 Path | Notes |
|-----------|--------------|----------|-------|
| Main app | `ShinyApp/app.R` (12K) | `Technical/ShinyApp/app.R` | Needs path refactoring |
| Server logic | `ShinyApp/R/server_logic.R` (106K) | `Technical/ShinyApp/R/server_logic.R` | Core calculations |
| UI tabs | `ShinyApp/R/ui_tabs.R` (33K) | `Technical/ShinyApp/R/ui_tabs.R` | Tab definitions |
| Lineage viz | `ShinyApp/R/lineage_viz.R` (16K) | `Technical/ShinyApp/R/lineage_viz.R` | Data lineage |
| Server routing | `ShinyApp/server.R` (845B) | `Technical/ShinyApp/server.R` | Routing |
| UI definition | `ShinyApp/ui.R` (4.5K) | `Technical/ShinyApp/ui.R` | Interface |
| Data files (15 CSV) | `ShinyApp/data/` (105K) | `Technical/ShinyApp/data/` | Runtime data |

### 7.2 Known Path Issues (to fix during migration)
- `server_logic.R` may reference `Shaikh Tonak/` paths
- Some data files use hardcoded absolute paths
- Need AS2-specific config for project root resolution

---

## 8. Outputs (OUT)

### 8.1 Existing (from Shaikh Tonak, reference only)

| Output | Path | Notes |
|--------|------|-------|
| Phase 1 NSW reports | `Shaikh Tonak/Outputs/Phase1_NSW/` | 17 LaTeX PDFs |
| Phase 2 Productive Labor | `Shaikh Tonak/Outputs/Phase2_Productive_Labor/` | 4 CSVs, 7 PNGs, 4 PDFs |
| Phase 3 Replication | `Shaikh Tonak/Outputs/Phase3_Replication/` | Validation data |
| Deliverables for Tonak | `Shaikh Tonak/Outputs/Deliverables_for_Tonak/` | Packaged versions |

### 8.2 To Be Created for AS2

| Output | Target Path | Purpose |
|--------|------------|---------|
| Complete Database | `Outputs/Data/COMPLETE_DATABASE/` | Master 1948-2025 dataset |
| Anu Extenbooks | `Outputs/Anu_Extenbooks/` | Per-series Excel workbooks |
| Figures | `Outputs/Figures/` | Publication-quality figures |
| Reports | `Outputs/Reports/` | LaTeX reports |
| Deliverables | `Outputs/Deliverables/` | Packaged deliverables |

---

## 9. Cross-Reference Map

```
Chapter (Ch2-Ch9)
  └── Book Tables (Tables 5.5-5.14, NSW tables, IO tables, etc.)
        └── T-Series (T201, T401-T402, T501-T516, T601-T609, T701-T703, T801, T901)
              └── Source Data
                    ├── Book Tables (Inputs/BookTables/)
                    ├── Shaikh Tonak Authoritative (migrated)
                    ├── Tonak Benchmarks (Inputs/ExternalSources/)
                    └── API Extensions (Inputs/API_Data/)
              └── Scripts (scripts/calculate/, scripts/extend/)
              └── Provenance (DPR, EPR, FPR docs)
              └── Validation (tests/)
        └── Knowledge Base (HDARP extractions)
  └── Chapter Investigation (docs/chapters/)
```

---

## 10. Migration Checklist

### Must-Copy (data-critical)
- [x] Anu Suite (all 5 tools from CD2)
- [ ] Authoritative exploitation rate CSVs
- [ ] IO matrices (18 files)
- [ ] Mohun comparison data (16 files)
- [ ] NIPA book period data
- [ ] SIC-NAICS concordance
- [ ] Tonak benchmark files (6 files)

### Must-Migrate (refactor paths)
- [ ] Shiny app (app.R + R/ modules + data/)
- [ ] Phase 3 calculation scripts (19 Python files)
- [ ] Validation scripts
- [ ] Book extraction content

### Reference-Only (link, don't copy)
- BEA IO benchmark PDFs (92 MB; keep in Shaikh Tonak/Inputs/)
- Page images from book (227 MB; keep in shaikh_tonak_1994/)
- Archive/ (11 GB; historical versions)

### Create Fresh
- All Phase 0 docs (this atlas, North Star, matrix, gaps, method contract)
- T_SERIES_CATALOG.json
- ANU_CHOPPED_CATALOG.json
- All DPR/EPR/FPR documents
- TRANSFORMATION_LOG.json
- Complete database
- Anu Extenbooks
- Anu Review reports

---

*Generated as part of AS2 Phase 0 deliverables.*
*Artifact Atlas v1.0 - February 23, 2026*
