# AS2 North Star

**The definitive strategy document for the AS2 replication and extension package.**

**Version**: 2.0 (Phase 1 — CD2-Aligned)
**Date**: February 23, 2026
**CD2 Alignment Note**: v2.0 incorporates lessons from CD2's completed workflow — API-first data ingestion, Anu Chopped format, catalog-driven provenance, and the transformation chain as a first-class architectural concept.

---

## 1. Mission Statement

AS2 is a meticulous, chapter-by-chapter replication and extension of every empirical claim in Shaikh & Tonak's *Measuring the Wealth of Nations: The Political Economy of National Accounts* (1994). The package will:

1. **Replicate** all book tables (Chapters 5-9) using the book's original data and methodology, confirming exact reproduction.
2. **Extend** every extendable series from the book's endpoint (~1989) through 2025 using modern API sources (BEA, FRED, BLS).
3. **Visualize** results in an interactive Shiny application that presents original vs. extended data with full provenance transparency.
4. **Document** every data transformation, splice decision, and methodological choice to a standard that permits independent verification by any economist.

The result is a living, auditable research instrument -- not a static dataset.

### 1.1 Relationship to Shaikh Tonak Project

AS2 subsumes and formalizes the existing `Shaikh Tonak` project (95% complete):
- **Phase 1** (NSW analysis, 1952-2025): Incorporated into Wave 1 / Chapter 6
- **Phase 2** (Productive labor extension, 2010-2023): Incorporated into Wave 1 / Chapter 5
- **Phase 3** (Book replication, 93.8% exact match, MAE=0.000937): Incorporated into Wave 1 / Chapter 5
- **Shiny App** (v2.5, modularized): Migrated to AS2/Technical/ShinyApp/
- **IO Matrices** (18 files, 1947-1977): Migrated to AS2/Inputs/IO_Matrices/

### 1.2 Relationship to CD2

AS2 follows the same architecture as CD2 (Shaikh 2016 replication):
- Same Anu Suite (all 5 tools, project-agnostic)
- Same Druck workspace standards (3-folder structure)
- Same provenance methodology (DPR/EPR/FPR)
- Same quality gates (Anu Review >= 85%)
- Different series prefix: **T-series** (table-centric) instead of CD2's S-series (figure-centric)

---

## 2. Non-Negotiable Principles

1. **Explicit over implicit.** Every data loading step parses explicitly; no silent defaults. Every splice point, rebase, and transformation is logged.
2. **Fail loudly.** If a series cannot be extended with confidence, it is flagged as blocked -- never silently approximated.
3. **Provenance first.** Every series has a DPR (Data Provenance Record). Every extension has an EPR (Extension Provenance Record). Every figure has an FPR (Figure Provenance Record).
4. **Read-only originals.** Source data in `Inputs/` is never modified. Processing happens in `Technical/`; results go to `Outputs/`.
5. **One sheet per file.** All Excel outputs follow the Druck one-sheet rule.
6. **Reproducibility over speed.** We do not cut corners to ship faster. Every chapter must pass its quality gate before moving to the next wave.

---

## 3. Definition of Done

### For a Replicated Table
- Original data loaded from `Inputs/BookTables/` or migrated authoritative data
- Values match book's reported figures within tolerance (0.1% for rates, 1% for absolute values)
- DPR exists documenting sources, transformations, and validation
- Table renders correctly in the Shiny app
- At least one automated test confirms the data path

### For an Extended Series
- EPR exists documenting: API source, splice year, splice method, transition analysis
- Transition quality passes: connection ratio 0.95-1.05, growth rate continuity <5% deviation, trend correlation >0.95
- Extended data available as CSV in the complete database
- Extenbook generated with Sheet 1 (data) and Sheet 2 (provenance)
- Shiny app renders both original and extended series with visual distinction

### For a Completed Chapter
- All empirical tables replicated
- All extendable series extended
- Chapter investigation document complete
- Anu Review score >= 85% (COMPLETE certification)
- All tests passing

---

## 4. Book Architecture and Empirical Scope

### 4.1 Chapter Classification

| Chapter | Title | Empirical Type | Series | Tables (Emp) | Extension |
|---------|-------|---------------|--------|--------------|-----------|
| 2 | Concepts: Marxian, SNA | Theoretical + 1 series | T201 (1) | 0 | Minimal |
| 3 | Classification: Productive/Unproductive | Conceptual figures | FPRs only | 0 | N/A |
| 4 | IO Framework | IO methodology | T401-T402 (2) | 2 | Needs concordance |
| 5 | Accounting Framework | Core: exploitation, labor, surplus value | T501-T516 (16) | 10 | Yes |
| 6 | Net Social Wage | NSW analysis | T601-T609 (9) | 6+ | Yes |
| 7 | IO Applications | IO labor values | T701-T703 (3) | 3 | Partial |
| 8 | Comparison | Wolff, Mage, Mohun comparisons | T801 (1) | 2 | Historical only |
| 9 | Summary | Derived from Ch5 | T901 (1) | 1 | Yes (derived) |
| **Total** | | | **~35** | **~24** | |

### 4.2 Data Source Hierarchy

```
1. Book Tables (Inputs/BookTables/) -- AUTHORITATIVE baseline
   |
2. Shaikh Tonak Authoritative Data -- Phase 1-3 results
   |
3. Tonak Benchmarks (Inputs/ExternalSources/) -- Validation reference
   |
4. Modern APIs -- EXTENSION sources
   ├── BEA (NIPA, Fixed Assets, IO tables)
   ├── FRED (interest, unemployment, CPI)
   └── BLS (employment, production workers, wages)
```

### 4.3 API Pull Script Architecture

AS2 uses dedicated ingest scripts to pull raw data from government APIs. Each script outputs one CSV per NIPA table to `Inputs/API_Data/{agency}/` with an accompanying `provenance.json`.

| Script | API | Tables Pulled | Output Directory | Purpose |
|--------|-----|---------------|------------------|---------|
| `pull_bea_nipa_ch05.py` | BEA | 1.7.5, 6.2D, 6.4B, 6.5B, 6.10B | `API_Data/BEA/` | Ch 5 employment + compensation |
| `pull_bea_nipa_ch06.py` | BEA | 2.1, 3.1, 3.2, 3.3 | `API_Data/BEA/` | Ch 6 NSW government accounts |
| `pull_bls_ces.py` | BLS | CES production/nonsupervisory by industry | `API_Data/BLS/` | Lp/L ratios (replaces placeholder) |
| `pull_fred_ch05.py` | FRED | TCU (capacity utilization) | `API_Data/FRED/` | Profit rate adjustment T514 |
| `pull_bea_fixed_assets.py` | BEA | Fixed Assets Table 4.1 | `API_Data/BEA/` | Capital stock K for r* |

All scripts follow the pattern:
- `PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent`
- API key from environment variable (`BEA_API_KEY`, `BLS_API_KEY`, `FRED_API_KEY`)
- One CSV per table with standardized column names
- `provenance.json` with timestamp, API URL, parameters, row count

### 4.4 Transformation Chain (NIPA-to-Marxian Pipeline)

The 7-stage transformation from raw NIPA accounts to Marxian categories is AS2's unique contribution vs CD2. Where CD2 maps figure data directly, AS2 must decompose national accounts through a principled classification pipeline.

| Stage | Name | Input | Output | Key Operation |
|-------|------|-------|--------|---------------|
| 1 | Raw NIPA Pull | BEA API | NIPA tables (1.7.5, 6.x, etc.) | API ingest, CSV storage |
| 2 | Sector Classification | NIPA industries | Productive (p) vs Unproductive (u) | IO-based classification per Ch 4 |
| 3 | Labor Decomposition | BLS CES + NIPA 6.x | Lp, Lu, L, ec_p, ec_u | Production worker ratios by industry |
| 4 | Value Decomposition | NIPA 1.7.5 + Stage 2 | TP*, C*_m, GFP, V*, S* | Table E.2 revenue accounts |
| 5 | Rate Construction | Stages 3-4 | e=S*/V*, Lp/L, V*/W, C*/V* | Table 5.7 key ratios |
| 6 | Extension Splicing | Book period + API data | 1948-2025 continuous series | Splice at 1989 with quality checks |
| 7 | Validation | Extended series | Pass/fail per tolerance | Book benchmarks, cross-chapter consistency |

This pipeline is documented in the Chapter 5 Investigation (Section 7) and implemented through the scripts in `Technical/scripts/calculate/`.

---

## 5. Chapter Wave Strategy

### Wave 1: Core Empirical (Chapters 5, 6, 9)
**Why first**: These chapters contain the book's empirical backbone -- exploitation rates, productive/unproductive labor, surplus value, and net social wage. The existing Shaikh Tonak project has Phase 1 (NSW), Phase 2 (productive labor), Phase 3 (book replication), and the authoritative exploitation rate 1948-2024 already done.

| Chapter | Series | Key Work |
|---------|--------|----------|
| 5 | T501-T516 | Replicate Tables 5.5-5.14; extend to 2025 |
| 6 | T601-T609 | Replicate NSW tables; extend using Phase 1 results |
| 9 | T901 | Derive summary table from Chapter 5 results |

**Entry gate**: Phase 1 (scaffold + data migration) complete

**Exit gate (sharpened v2.0)**:
- All 5 benchmark years for e (1948, 1958, 1967, 1977, 1989) within 0.1% of book values
- Table E.2 verified for at least 3 variables (TP*, CON*, GFP) across 1948-1989
- Real BLS/NIPA data replacing all placeholder values
- At least 5 DPRs complete for keystone series (T504, T506, T511, T512, T607)
- T_SERIES_CATALOG.json and ANU_CHOPPED_CATALOG.json initialized with Wave 1 entries
- Anu Review >= 85%

### Wave 2: IO and Structural (Chapters 4, 7)
**Why second**: IO matrix calculations require the SIC-NAICS concordance for post-1997 extension. Existing project has 18 IO matrix files for 1947-1977.

| Chapter | Series | Key Work |
|---------|--------|----------|
| 4 | T401-T402 | Reproduce A-matrix, B-matrix calculations |
| 7 | T701-T703 | Replicate labor value calculations; extend with modern IO tables |

**Entry gate**: Wave 1 certified
**Exit gate**: IO benchmarks match book, modern extensions documented, Anu Review >= 85%

### Wave 3: Comparative and Theoretical (Chapters 2, 3, 8)
**Why last**: Primarily documentation and FPRs. Minimal empirical content.

| Chapter | Series | Key Work |
|---------|--------|----------|
| 2 | T201 | Document alternative GFP measures |
| 3 | FPRs only | Conceptual figures (productive/unproductive classification diagrams) |
| 8 | T801 | Document comparison with Wolff, Mage, Mohun (no extension) |

**Entry gate**: Wave 2 certified
**Exit gate**: All chapters documented, all FPRs complete

---

## 6. Methodology Contract (Summary)

See `PHASE0_METHOD_CONTRACT.md` for the full contract.

### 6.1 Replication Tolerance
- **Rates** (exploitation, profit): <= 0.1% relative difference
- **Absolute values** (output, surplus): <= 1% relative difference
- **Integer data** (employment counts): exact match required

### 6.2 Splice Methods

| Method | When to Use |
|--------|-------------|
| `level_match` | Same agency, same concept, same methodology continues |
| `growth_rate_splice` | Different source; same concept; good overlap |
| `direct_append` | No overlap; low risk of level shift |
| `rebase_and_splice` | Series with different base years |

### 6.3 Splice Avoidance Years
Do not splice at: 1992 (SIC->NAICS), 2003 (BEA revision), 2013 (BEA revision), 2020 (COVID).

### 6.4 Transition Quality Thresholds

| Metric | Pass | Warn | Fail |
|--------|------|------|------|
| Connection ratio at splice | 0.95-1.05 | 0.90-0.95 or 1.05-1.10 | <0.90 or >1.10 |
| Growth rate continuity | <3% deviation | 3-5% | >5% |
| Trend correlation (5yr window) | >0.98 | 0.95-0.98 | <0.95 |

---

## 7. Validation and Review Gates

### 7.1 Per-Series Validation
- Value match against book tables (within tolerance)
- Transition quality check at splice point
- Automated test coverage

### 7.2 Per-Chapter Review (Anu Review 8 Dimensions)

| Dimension | Weight | Threshold |
|-----------|--------|-----------|
| DPR Completeness | 15% | 100% of series |
| EPR Completeness | 15% | 100% of extended series |
| Data File Integrity | 15% | CSV structure, columns, year ranges |
| Series Mapping | 15% | All series in data_loader |
| Chart Builder Integration | 10% | Tables render in Shiny |
| Test Coverage | 10% | Passing chapter tests |
| Catalog Consistency | 10% | Catalog entries match data |
| Knowledge Base Integration | 10% | HDARP linkages valid |

### 7.3 Certification Levels

| Level | Score | Meaning |
|-------|-------|---------|
| EXEMPLARY | >= 95% | Reference implementation |
| COMPLETE | >= 85% | Fully integrated, production ready |
| ADEQUATE | >= 70% | Functional with documented gaps |
| INCOMPLETE | < 70% | Blocked; cannot proceed to next wave |

**Minimum to proceed to next wave**: COMPLETE (>= 85%) for all chapters in current wave.

---

## 8. Risk Register

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|------------|------------|
| R1 | SIC-NAICS transition breaks IO continuity post-1997 | High | High | Use NBER concordance; bridge with 1992/1997 overlap |
| R2 | NIPA revisions change exploitation rate levels | High | Medium | Document vintage; compare pre/post revision |
| R3 | VA*/W=1.24 constant assumption (Phase 3) needs validation | Medium | Medium | Test sensitivity; compare with Mohun estimates |
| R4 | COVID outliers distort 2020-2021 extension | Medium | Confirmed | Flag COVID years; provide pre/post COVID trends |
| R5 | Book tables not fully machine-readable yet | Medium | Confirmed | Convert during Phase 1 to Anu Chopped format |
| R6 | Shiny app paths hardcoded to Shaikh Tonak project | Medium | Confirmed | Refactor to config-based paths during migration |
| R7 | NSW formula reconciliation across Tonak papers | Medium | Medium | Use 1987 paper as primary; document deviations |
| R8 | Phase 3 uses placeholder BLS data | Medium | Confirmed | Replace with actual BLS API data in Wave 1 |

---

## 9. Go/No-Go Gates

### Phase 0 -> Phase 1 (Scaffold + Migration)
- [x] North Star complete
- [x] Artifact Atlas complete
- [x] Chapter Intelligence Matrix complete
- [x] Gap/Blocker Register complete
- [x] Method Contract complete

### Phase 1 -> Wave 1 (First Extension Wave)
- [x] AS2 scaffold created (Inputs/, Technical/, Outputs/) — Session 1
- [x] Data migrated from Shaikh Tonak project — Session 1
- [x] Shiny app migrated and launches — Session 1
- [x] Chapter investigations complete (Ch 5, 6, 9) — Session 2
- [x] Paths normalized (config.R created) — Session 3
- [x] Anu Chopped CSVs created (7 Wave 1 core files) — Session 3
- [x] API pull script architecture in place (5 scripts) — Session 3
- [x] Catalogs initialized (T_SERIES, ANU_CHOPPED, DIVERGENCE) — Session 3
- [x] First DPRs created (5 keystone series) — Session 3
- [ ] Baseline tests pass — Session 4
- [ ] Real NIPA data replaces placeholder — needs BEA API key
- [ ] Real BLS data replaces placeholder — needs BLS API key

### Wave N -> Wave N+1
- [ ] All chapters in current wave at COMPLETE certification (>= 85%)
- [ ] All extended series pass transition quality thresholds
- [ ] No unresolved FAIL-level divergences
- [ ] User review and approval

### Final -> Deliverables
- [ ] All waves complete
- [ ] Cross-chapter consistency validated
- [ ] Full Extenbook set generated
- [ ] LaTeX methodology report compiled
- [ ] Final Anu Review: all chapters >= 85%

---

## 10. Success Criteria (Measurable)

| Metric | Target |
|--------|--------|
| Book tables replicated | All empirical tables in Ch 5-9 |
| Series extended to 2025 | >= 25/35 (remainder documented as historical-only or blocked) |
| DPR coverage | 100% |
| EPR coverage | 100% of extended series |
| FPR coverage | 100% of all figures |
| Anu Review score (all chapters) | >= 85% (COMPLETE) |
| Transition quality pass rate | >= 95% of extended series |
| Automated test coverage | >= 1 test per chapter |
| Shiny app renders all empirical tables | 100% |

---

## 11. Anu Chopped Format for AS2 (Pattern T)

AS2 adapts the Anu Chopped format for table-centric data. Unlike CD2's figure-centric Pattern S, AS2's Pattern T organizes around NIPA table structures.

### 11.1 File Structure

- **Row 1**: Metadata — source book table, NIPA table references, methodology notes, date range
- **Row 2**: Subseries IDs — T-series identifiers with suffixes (A=authoritative, B=BLS, C=combined, EXT=extended)
- **Row 3+**: Data — year in column 1, values in subsequent columns

### 11.2 Naming Convention

```
Table{chapter}_{table_number}_{Description}.csv
```

Examples:
- `Table5_7_KeyRatios.csv` — Book Table 5.7 exploitation rates
- `TableE2_RevenueAccounts.csv` — Appendix Table E.2 value accounts
- `Employment_1948_1989.csv` — Employment decomposition

### 11.3 Directory Structure

```
Inputs/ST_Chopped/
├── ch05/     # Chapter 5 tables
├── ch06/     # Chapter 6 tables
├── ch09/     # Chapter 9 tables
└── README.md
```

### 11.4 Example Header

```csv
# source=BookTable5.7 | nipa_refs=1.7.5,6.2D,6.4B | methodology=Shaikh-Tonak1994 | period=1948-1989
,T506A,T511A,T512A,T506,T511,T512
1948,1.70,0.57,0.54,1.70,0.57,0.54
```

---

## 12. Catalog-Driven Workflow

All data flows are tracked through three catalogs that serve as the single source of truth for data inventory.

### 12.1 T_SERIES_CATALOG.json

The master catalog of all 35 T-series. Schema per entry:

```json
{
  "series_id": "T506",
  "name": "Rate of Exploitation (e = S*/V*)",
  "chapter": 5,
  "book_table": "5.7",
  "formula": "S_star / V_star",
  "nipa_inputs": ["1.7.5", "6.2D"],
  "bls_inputs": ["CES production worker ratios"],
  "period_original": "1948-1989",
  "period_extended": "1948-2024",
  "status": "validated",
  "chopped_file": "ST_Chopped/ch05/Table5_7_KeyRatios.csv",
  "dpr_file": "docs/series/T506_DPR.md",
  "dependencies": ["T504", "T505"]
}
```

### 12.2 ANU_CHOPPED_CATALOG.json

Tracks all Anu Chopped CSV files. Schema per entry:

```json
{
  "filename": "Table5_7_KeyRatios.csv",
  "chapter": "ch05",
  "source": "shaikh_tonak_authoritative_1948_1989.csv",
  "columns": {
    "T506A": "Exploitation rate (authoritative)",
    "T511A": "Productive labor share (authoritative)"
  },
  "linked_figures": ["5.1", "5.2"],
  "linked_series": ["T506", "T511", "T512"]
}
```

### 12.3 DIVERGENCE_REGISTER.json

Documents known divergences from book methodology:

```json
{
  "id": "DIV-001",
  "series": "T514",
  "description": "r* uses total K (all sectors) instead of productive K*",
  "impact": "Profit rate level differs from book Table 5.11",
  "status": "open",
  "resolution": "Restrict K to productive sectors using IO classification"
}
```

---

*This document is the authoritative reference for AS2 development. All agents, sessions, and decisions must be consistent with its principles, methods, and gates.*

*AS2 North Star v2.0 - February 23, 2026*
