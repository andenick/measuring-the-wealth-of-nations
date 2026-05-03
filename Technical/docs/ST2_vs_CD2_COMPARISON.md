# ST2 vs CD2: Data Construction Comparison

**Generated**: 2026-03-21
**Purpose**: Side-by-side comparison of the two Anu Suite data construction projects

---

## 1. Source Books

| Dimension | ST2 | CD2 |
|-----------|-----|-----|
| **Book** | Shaikh & Tonak (1994) *Measuring the Wealth of Nations* | Shaikh (2016) *Capitalism: Competition, Conflict, Crises* |
| **Theoretical Framework** | Marxian national accounts: productive/unproductive labor, value categories, surplus value, Net Social Wage | Classical political economy: profit rates, competition, wages, prices, trade, growth |
| **Core Period** | US 1948-1989 | Global 1850-2015 |
| **Extension Period** | 1990-2025 | To 2025-2026 (where FRED/OECD sources permit) |
| **Geographic Scope** | United States only | United States primary, with OECD and global coverage |
| **Primary Sources** | BEA NIPA + BLS employment data | BEA NIPA, FRED, BLS, Penn World Tables, OECD STAN, FRB G-17, MeasuringWorth, Ibbotson, Shiller |

---

## 2. Scale Comparison

| Metric | ST2 | CD2 | Ratio |
|--------|-----|-----|-------|
| **Series (registry)** | 33 | 113 | 3.4x |
| **Subseries** | 60 | 292 | 4.9x |
| **Chapters covered** | 7 (Ch 2,4,5,6,7,8,9) | 13 (Ch 2,5,6,7,8,9,10,11,12,14,15,16,17) | 1.9x |
| **Unique figures** | 15 | 112 | 7.5x |
| **Loading scripts** | 17 | 62 | 3.6x |
| **Processing scripts** | 18 | 89 | 4.9x |
| **Series docs (DPRs, decomps, EPRs)** | 71 files | 72 files | ~1x |
| **Figure provenance reports** | 17 | 33 | 1.9x |
| **External source prefixes** | 10 | 178 | 17.8x |
| **Pipeline series (PIPELINE_STATE)** | 26 active | 43 active | 1.7x |
| **Review scores** | Ch5: v3.6, Ch6: v3.6, Ch9: v3.6 | Ch2: 97, Ch6: 90, Ch7: 89, Ch10: 86 | -- |

---

## 3. Data Construction Methodology

### ST2: Algebraic Chain from NIPA + BLS

ST2 constructs Marxian national accounting categories via a strict algebraic chain. Nearly every series is *derived* from NIPA line items and BLS employment ratios rather than downloaded directly:

```
TP* --> C* --> VA* --> V* --> S* --> e (exploitation rate)
```

- **T501** (Total Product TP*): Sum of productive-sector gross output from NIPA industry data
- **T502** (Constant Capital C*_m): Intermediate inputs to productive sectors
- **T503** (Value Added VA*): T501 - T502
- **T504** (Variable Capital V*): Productive-sector compensation adjusted by BLS employment ratios
- **T505** (Surplus Value S*): T503 - T504
- **T506** (Rate of Exploitation e): T505 / T504

Each step depends on the previous. Extension to post-1989 requires replicating the entire chain using modern NIPA equivalents (BEA GDP-by-Industry, BLS CES).

**Series notation**: `T###` (T for Tonak), subseries `T###-A` (book), `T###-B` (BEA extension), `T###-COMBINED`.

### CD2: Mixed Algebraic + Direct Source Downloads

CD2 draws from a much wider source base. Some series are direct downloads (FRED, Penn World Tables), others are algebraic composites from BEA NIPA tables, and some are multi-source spliced indexes spanning 150+ years:

- **S001** (Industrial Production): 4 raw subseries spanning 1860-2026, spliced via growth-rate matching at transition years (1919, 1985, 2010)
- **S026-S028** (Profit rate components): Algebraic composites built from 10 Tier-2 input tables (S206-S214, S013) using BEA NIPA/Fixed Assets data
- **S050-S059** (Interest rates, stock returns): Direct FRED/Ibbotson/Shiller downloads with minimal transformation

**Series notation**: `S###` (S for Shaikh), subseries `S###-A/B/C/D/...` with reindex transforms explicitly recorded (`S001-B = S001-A reindexed to 1958=100`).

### Concurrent Series

CD2's registry supports a "Concurrent Series" pattern (CS### prefix) designed for ratio series where numerator and denominator must be tracked separately. This pattern does not yet appear in the CD2 registry (0 CS-prefixed series found), but the architecture anticipates it.

ST2 handles ratio series (T513-T516: exploitation rates, profit rates) as standalone series with their own construction chains, without explicit numerator/denominator tracking in the registry.

---

## 4. Pipeline Architecture

### ST2: 4-Stage Pipeline

```
loaded --> processed --> extended --> validated
```

| Stage | Description | Current State |
|-------|-------------|---------------|
| **loaded** | Raw book data ingested into CSVs | 23/26 series |
| **processed** | Algebraic construction applied | 23/26 series |
| **extended** | Spliced to modern BEA/BLS data (post-1989) | 10/26 series |
| **validated** | Cross-checked against book benchmarks | 3/26 series |

Pipeline state tracked in `PIPELINE_STATE.json` with simple boolean flags per stage. Series organized into 3 waves:
- Wave 1: Ch5 value categories + Ch6 NSW + Ch9 (23 series)
- Wave 2: Ch4 + Ch7 (6 series)
- Wave 3: Ch2 + Ch8 (2 series)

### CD2: 6-Stage Pipeline

```
research --> ingestion --> extension --> replication --> output --> viz_audit
```

With sub-stages tracked per chapter:
- **stage_1_research**: research.json files created per series
- **stage_2_ingestion**: Registry entries + decomposition docs
- **stage_3_extension**: FRED/OECD API extensions configured and executed
- **stage_4_replication**: Clean-slate replicate.py run with reference-value validation
- **stage_5_output**: Chopped CSVs, extenbooks, figure CSVs, absorbed databases
- **stage_6_viz_audit**: Dash app integration and visual verification

Each chapter also receives an **anu_review** with a 12-dimension weighted score (D1-D12), yielding a numeric certification (85+ = COMPLETE, 95+ = EXEMPLARY).

### Replicator Differences

| Aspect | ST2 | CD2 |
|--------|-----|-----|
| Loading scripts | 17 (L01-L17) | 62 (L00-L24+) |
| Processing scripts | 18 (P01-P18) | 89 (P00-P27+) |
| Orchestrator | replicate.py | replicate.py (with --ledger auto-generation) |
| Absorbed databases | 3 chapter CSVs | 4 chapter CSVs (long format) |
| Two-tier structure | No | Yes (Tier 1 composites + Tier 2 input tables) |

### TRANSFORMATION_LOG.json

Both projects have a TRANSFORMATION_LOG.json, but they differ in maturity:

- **CD2**: Structured with `transform_id`, `formula`, `parameters`, `script_hash`, `input_files`, `output_files`, `validation_result` per transformation. Created early in the project (2026-01-26) and maintained as a formal audit trail.
- **ST2**: Uses `XLOG-###` identifiers with `operation`, `description`, `inputs`, `outputs`, `series_affected`. Created during Phase 3 processing. Less structured than CD2's version (e.g., no `formula` or `script_hash` fields).

---

## 5. Artifact Comparison

| Artifact Type | ST2 | CD2 | Notes |
|---------------|-----|-----|-------|
| **series_registry.json** | 33 series, 60 subseries | 113 series, 292 subseries | CD2 includes Tier 2 input tables |
| **PIPELINE_STATE.json** | 4-stage booleans per series | 6-stage status per chapter | Different granularity |
| **ANU_LEDGER.json** | 26 series, 87% coverage | 43 series, 99% doc health | CD2 auto-generated via --ledger |
| **TRANSFORMATION_LOG.json** | Present (XLOG format) | Present (structured T### format) | CD2 more mature |
| **Research JSONs** | 26 | 27+ (8+4+5+10) | Per-series methodology docs |
| **Decomposition MDs** | 26 | 21+ (8+4+5+10 Tier 1 only) | ST2 covers all series |
| **DPRs** | 26 | 21+ | Data Provenance Reports |
| **EPRs** | 19 | 20+ | Extension Provenance Reports |
| **FPRs** | 17 | 33 | Figure Provenance Reports |
| **Chopped CSVs** | 26 | 27+ (Tier 1 only) | Anu-standard atomic format |
| **Extenbooks (.xlsx)** | 26 | 27+ | 4-sheet workbooks |
| **Figure CSVs** | 18 | 33+ | Viz-ready figure data |
| **Review reports** | 3 (Ch5, Ch6, Ch9 at v3.6) | 4 (Ch2, Ch6, Ch7, Ch10) | CD2 uses 12-dimension scoring |
| **Chapter investigations** | 3 (Ch5, Ch6, Ch9) | 0 (uses review reports instead) | ST2 has deep NIPA investigations |
| **Dash/Shiny viz app** | Shiny integration | Dash app (multi-page) | Different frameworks |

---

## 6. What ST2 Can Learn from CD2

### TRANSFORMATION_LOG.json Structure
CD2's transformation log includes explicit `formula`, `parameters`, `script_hash`, and `validation_result` fields per transformation. ST2's XLOG entries are more narrative. Adopting CD2's structured format would improve auditability.

### 6-Stage Pipeline with Review Scoring
CD2's pipeline distinguishes between ingestion and replication as separate stages, and adds a formal **anu_review** pass with 12 weighted dimensions (D1 KB completeness through D12 documentation). ST2 could benefit from:
- An explicit "absorbed" stage to create standardized long-format chapter databases
- A numeric review scoring system (the v3.6 review reports are qualitative)

### Two-Tier Series Architecture
CD2 separates Tier 1 composites (which get full pipeline treatment) from Tier 2 input tables (which are loaded but not independently processed/documented). This would be useful for ST2's BLS employment tables and NIPA detail tables that feed into the algebraic chain but are not standalone analytical series.

### Auto-Generated Ledger
CD2's `replicate.py --ledger` flag auto-generates ANU_LEDGER.json from the current state of outputs. ST2's ledger appears to be manually maintained.

### Broader External Source Integration
CD2 integrates 178 unique source prefixes vs ST2's 10. While ST2's narrow source base (NIPA + BLS) is appropriate for its Marxian accounting scope, FRED API integration patterns from CD2 could streamline the extension pipeline.

---

## 7. What CD2 Can Learn from ST2

### Comprehensive 3-Way External Validation
ST2 validates its series against three independent reconstructions of the same Marxian categories:
- **Mohun (2005, 2014)**: Independent surplus-value calculations
- **Moos (2023)**: Updated productive/unproductive classification
- **Tonak's own data**: Original book tables as benchmark

This multi-scholar cross-validation methodology is absent from CD2, which relies on internal reference-value checks (book table values) without external scholar replication.

### Deep NIPA-Line-Item Investigation Documents
ST2 has dedicated investigation documents (e.g., `CHAPTER_5_INVESTIGATION.md`, `CHAPTER_6_INVESTIGATION.md`) that trace specific NIPA line items across table revisions, identify discontinuities, and document BEA methodology changes. These go beyond standard DPRs to address *why* specific NIPA tables changed over time.

CD2's documentation focuses on the series-level construction but does not systematically investigate upstream source methodology changes.

### NSW Comparison Methodology
ST2's Chapter 9 Net Social Wage (NSW) analysis provides a template for how to handle complex multi-component accounting identities where individual components can be validated independently and the aggregate checked for consistency. The approach of:
1. Building each component independently
2. Summing to the aggregate
3. Comparing the aggregate to known totals
4. Diagnosing residuals

...could be applied to CD2's Tier 1 composites (S026-S028), which are currently validated only at the composite level.

### Algebraic Chain as Test Harness
ST2's strict algebraic dependencies (each series derived from predecessors) create a natural regression test: if T501 changes, T502-T516 must all be recomputed and revalidated. CD2's more independent series structure means a change in one source does not automatically trigger downstream re-validation.

---

## Appendix: Key File Paths

| File | ST2 | CD2 |
|------|-----|-----|
| Series Registry | `Technical/series_registry.json` | `Technical/series_registry.json` |
| Pipeline State | `Technical/PIPELINE_STATE.json` | `Technical/PIPELINE_STATE.json` |
| Ledger | `Technical/ANU_LEDGER.json` | `Technical/ANU_LEDGER.json` |
| Transformation Log | `Technical/TRANSFORMATION_LOG.json` | `Technical/TRANSFORMATION_LOG.json` |
| Loading Scripts | `Technical/ANU_REPLICATOR/scripts/loading/` (17) | `Technical/ANU_REPLICATOR/scripts/loading/` (62) |
| Processing Scripts | `Technical/ANU_REPLICATOR/scripts/processing/` (18) | `Technical/ANU_REPLICATOR/scripts/processing/` (89) |
| Series Docs | `Technical/docs/series/` (71 files) | `Technical/docs/series/` (72 files) |
| Figure Docs | `Technical/docs/figures/` (17 files) | `Technical/docs/figures/` (33 files) |
| Review Reports | `Technical/docs/chapters/` | `Technical/docs/` |
