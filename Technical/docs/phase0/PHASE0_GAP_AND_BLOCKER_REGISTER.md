# Phase 0 Gap and Blocker Register

**Purpose**: Catalog every known gap, blocker, and open question that must be resolved before or during AS2 implementation.

**Version**: 1.0
**Date**: February 23, 2026

---

## 1. Data Gaps

### 1.1 Book Tables Not Fully Machine-Readable

| Table | Chapter | Description | Current State | Resolution Path |
|-------|---------|-------------|---------------|-----------------|
| Tables 5.5-5.8 | 5 | Core exploitation accounting | Phase 3 replicated 93.8% match; raw tables need Anu Chopped conversion | Convert authoritative CSVs to Anu Chopped format |
| Tables 5.9-5.14 | 5 | Detailed labor, surplus breakdowns | Some extracted via HDARP; not all in machine-readable CSV | Complete HDARP extraction; digitize remaining tables |
| NSW tables | 6 | Net social wage components | Phase 1 produced complete 1952-2025 series; book tables need cross-check | Validate Phase 1 output against book tables |
| IO application tables | 7 | Labor value calculations | IO matrices exist (1947-1977); application tables not extracted | Extract from book; compute from IO matrices |
| Summary table | 9 | Chapter 9 summary | Derived from Ch5; straightforward | Compute after Ch5 completion |

### 1.2 IO Benchmark Data for Modern Years

| Gap | Scope | Impact | Resolution |
|-----|-------|--------|------------|
| BEA IO tables for 1997-2022 benchmarks | Ch 4, Ch 7 | Cannot extend IO analysis past 1977 without modern tables | Download BEA Make/Use tables for 1997, 2002, 2007, 2012, 2017, 2022 |
| SIC-NAICS concordance for IO sectors | Ch 4, Ch 7 | 85-sector SIC (pre-1997) to NAICS (post-1997) mapping | Use NBER concordance + existing concordance file |

### 1.3 Extension Period API Data

| Gap | Scope | Resolution |
|-----|-------|------------|
| BEA NIPA tables for 1990-2025 | Ch 5, 6, 9 | Fetch via BEA API; key tables: 1.7.5, 1.12, 2.1, 3.1, 6.2-6.5 |
| BLS employment/production worker ratios | Ch 5 | Fetch via BLS API; CES data for production worker shares |
| Treasury/OMB data for NSW extension | Ch 6 | Phase 1 already extended to 2025; validate sources |

---

## 2. Methodology Gaps

### 2.1 SIC-NAICS Transition

| Question | Chapters Affected | Impact | Proposed Resolution |
|----------|-------------------|--------|---------------------|
| How to bridge SIC-based IO (pre-1997) to NAICS-based IO (post-1997)? | Ch 4, 7 | Cannot extend IO labor values without bridge | Use NBER SIC-NAICS concordance (already in Inputs); construct bridge matrix using 1992 and 1997 overlapping benchmarks |
| Which NAICS sectors map to Shaikh-Tonak productive/unproductive classification? | Ch 5, 7 | Affects all post-1997 calculations | Use Phase 3 concordance as starting point; validate against Mohun classification |

### 2.2 VA*/W = 1.24 Constant Assumption

| Question | Chapters Affected | Impact | Proposed Resolution |
|----------|-------------------|--------|---------------------|
| Phase 3 uses VA*/W = 1.24 as constant ratio for total economy value added per production worker. Is this valid for extension? | Ch 5 | Affects exploitation rate calculation for extended period | Test sensitivity: compute exploitation rate with VA*/W = 1.20, 1.24, 1.28; compare with Mohun estimates; document as assumption with bounds |

### 2.3 NSW Formula Reconciliation

| Question | Chapters Affected | Impact | Proposed Resolution |
|----------|-------------------|--------|---------------------|
| Shaikh & Tonak (1987) uses slightly different NSW formula than Shaikh & Tonak (1994) | Ch 6 | May cause discrepancy in NSW levels | Use 1994 book formula as primary; document deviations from 1987 paper; note any reconciliation in EPR |

### 2.4 Phase 3 Placeholder Data

| Question | Chapters Affected | Impact | Proposed Resolution |
|----------|-------------------|--------|---------------------|
| Phase 3 used placeholder BLS production/nonproduction ratios (create_placeholder_bls_ratios.py) | Ch 5 | Exploitation rate extension may shift when actual data used | Replace placeholders with actual BLS API data in Wave 1; re-run Phase 3 calculator; compare results |

---

## 3. Structural Issues

### 3.1 Path Hardcoding

| Issue | Location | Impact | Resolution |
|-------|----------|--------|------------|
| Shiny app references Shaikh Tonak paths | `ShinyApp/R/server_logic.R` | App won't launch from AS2 | Refactor all paths to use `here()` or config file |
| Test files may use absolute paths | `ShinyApp/test_app.R` | Tests fail outside original environment | Replace with relative paths |
| Phase 3 scripts reference `../data/` | `Phase3_Replication/src/*.py` | Scripts fail from new location | Update imports to use AS2-relative paths |

### 3.2 Data Format Conversion

| Issue | Current State | Target State | Resolution |
|-------|--------------|--------------|------------|
| No Anu Chopped CSVs exist | Data in ad-hoc CSV formats | All series in Anu Chopped format (header row 0 = metadata, row 1 = columns, row 2+ = data) | Convert during Phase 1 using anu-chopped spec |
| Shiny data files use various column naming | 15 CSV files with inconsistent naming | Standardized column names per T-series ID | Normalize during Shiny migration |

### 3.3 Missing Artifacts

| Artifact | Expected | Currently Exists | Gap |
|----------|----------|-----------------|-----|
| ANU_CHOPPED_CATALOG.json | 1 | 0 | Create during Phase 1 |
| T_SERIES_CATALOG.json | 1 | 0 | Create during Phase 1 |
| DPR documents | ~35 | 0 | Create during waves |
| EPR documents | ~25 (extendable series) | 0 | Create during waves |
| FPR documents | ~24 | 0 | Create during waves |
| Anu Review reports | 9 (one per chapter) | 0 | Create after each chapter |
| TRANSFORMATION_LOG.json | 1 | 0 | Initialize during Phase 1 |
| DIVERGENCE_REGISTER.json | 1 | 0 | Initialize during Phase 1 |

---

## 4. Blocker Summary by Wave

### Wave 1 (Chapters 5, 6, 9)
- **Hard blockers**: 0
- **Soft blockers**: Placeholder BLS ratios need replacement; book tables need Anu Chopped conversion
- **Risks**: VA*/W constant assumption; NSW formula reconciliation
- **Status**: READY TO START (after Phase 1 scaffold/migration)

### Wave 2 (Chapters 4, 7)
- **Hard blockers**: SIC-NAICS concordance for IO extension; modern BEA IO tables needed
- **Soft blockers**: IO labor value calculation scripts need refactoring
- **Risks**: IO methodology changes across BEA benchmark years
- **Status**: BLOCKED ON IO CONCORDANCE (must resolve before wave begins)

### Wave 3 (Chapters 2, 3, 8)
- **Hard blockers**: 0
- **Soft blockers**: Mohun/Wolff/Mage comparison data formatting
- **Risks**: Historical-only data cannot be extended (Ch 8)
- **Status**: READY (primarily documentation work)

---

## 5. Resolution Priority Queue

| Priority | Item | Effort | Wave Impact |
|----------|------|--------|-------------|
| P1 | Convert authoritative CSVs to Anu Chopped format | 2 hours | Wave 1 |
| P2 | Replace placeholder BLS ratios with actual API data | 3 hours | Wave 1 |
| P3 | Refactor Shiny app paths for AS2 | 4 hours | All waves |
| P4 | Validate Phase 1 NSW against book tables | 2 hours | Wave 1 |
| P5 | Build SIC-NAICS IO bridge matrix | 8 hours | Wave 2 |
| P6 | Download modern BEA IO tables (1997-2022) | 4 hours | Wave 2 |
| P7 | Test VA*/W sensitivity analysis | 2 hours | Wave 1 |
| P8 | Format Mohun/Wolff/Mage comparison data | 2 hours | Wave 3 |

---

## 6. Dependency Chain

```
Phase 0 (this session)
  └─> Phase 1 (scaffold + data migration + Anu Chopped conversion)
        └─> Wave 1 (Ch 5, 6, 9)
              ├─ Needs: Anu Chopped CSVs, actual BLS data, NIPA extension
              └─> Wave 2 (Ch 4, 7)
                    ├─ Needs: SIC-NAICS bridge, modern IO tables
                    └─> Wave 3 (Ch 2, 3, 8)
                          ├─ Needs: Wave 2 certified
                          └─> Final deliverables
```

---

*Gap and Blocker Register v1.0 - February 23, 2026*
*Updated as part of AS2 Phase 0 deliverables.*
