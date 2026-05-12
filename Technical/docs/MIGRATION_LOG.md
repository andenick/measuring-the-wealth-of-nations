# ST2 Migration Log

## Migration from Shaikh Tonak Project

- **Date**: 2026-03-21
- **Source project**: ../Shaikh Tonak/
- **Target project**: ./
- **Method**: File copy (originals preserved in source project)

---

### 1. Moos NSW Reconciliation (2 files)

**Target**: `Inputs/ExternalSources/Moos/`

Reconciled Moos NSW data used for cross-validation of exploitation rate estimates.

- `[2025.12.05] moos_nsw_reconciled.csv`
- `[2025.12.05] moos_summary.json`

### 2. Authoritative Exploitation Rate Data (5 files)

**Target**: `Inputs/ExternalSources/Shaikh_Tonak_Authoritative/`

Canonical Shaikh-Tonak exploitation rate series covering 1948-1989 (original study period) and the extended 1948-2024 range.

- `README.md`
- `[2025.12.05] shaikh_tonak_authoritative_1948_1989.csv`
- `[2025.12.05] shaikh_tonak_authoritative_1948_1989.json`
- `[2025.12.05] shaikh_tonak_authoritative_1948_2024.csv`
- `[2025.12.05] shaikh_tonak_authoritative_1948_2024.json`

### 3. Phase 2 Productive Labor Key Outputs (4 files)

**Target**: `Inputs/ExternalSources/Shaikh_Tonak_Phase2/`

Productive labor analysis outputs from Phase 2, including industry-level breakdowns and validation checks.

- `plausibility_checks.csv`
- `productive_labor_aggregates_2010_2023.csv`
- `productive_labor_by_industry_2010_2023.csv`
- `validation_results_2010.csv`

### 4. NSW Calculator Scripts — Reference Only (4 files)

**Target**: `Inputs/ExternalSources/Shaikh_Tonak_Framework/`

Core NSW (Net Social Wage) calculator implementations from the original project, migrated for reference. These document the computational methodology used in the first project.

- `[2025.10.02] nsw_calculator_final.py`
- `[2025.10.02] nsw_calculator_tonak_2000.py`
- `[2025.10.08] nsw_with_io_integration.py`
- `[2025.10.16] nsw_calculator_marxian_taxes.py`

---

**Total**: 15 files migrated across 4 categories. All originals remain intact in the source project.
