# ST2 NickyData v7.0 — Ground-Up Rebuild Plan

**Date**: 2026-05-09
**Current state**: v6.0, 71 Python files in code/, 28 in utils/, 59 T/N-series + 3 analytical, PASS
**Goal**: Streamlined v7.0 pipeline that produces identical results in fewer, cleaner files with clear data flow, proper dependency management, and no accumulated technical debt

---

## Principles

1. **Archive, don't delete**: v6.0 code moves to `Technical/_archive/v6.0_code/` intact
2. **Output parity**: v7.0 must produce bit-identical T/N-series CSVs (verified by hash comparison)
3. **Single responsibility**: each script does ONE thing, named for what it produces
4. **Explicit dependencies**: no importlib hacks, no priority-ordering workarounds, no M01 feedback loops
5. **Data flows forward**: Load → Compute → Validate → Output, no circular reads
6. **Configuration over code**: series definitions, classifications, and parameters in JSON/YAML, not hardcoded dicts scattered across files

---

## Architecture: v6.0 vs v7.0

### v6.0 (current)
```
code/
  setup/      S01, S02 (2 scripts)
  loading/    L01-L18 + _naics_io_parser (16 scripts)
  processing/ P01-P21 + _sector_variable_capital + _P17_archived (19 scripts)
  validation/ V01-V15 (15 scripts)
  manual/     M00, M01, M02, M99 (4 scripts)
  analysis/   A01-A10 (10 scripts)
  outputs/    O01-O06 (6 scripts)
  exploration/ E01 (1 script)
= 71 scripts, 8 phases, auto-discovered by prefix pattern
```

**Problems**:
- Circular dependency: P05 writes T512, P02 reads T512, M01 reads both and rewrites both
- M01 feedback loop (fixed but fragile — requires reading "book" not "combined" column)
- Priority ordering (P04 must run after P03, requires PRIORITY constants)
- 4 dead/archived scripts (_P17, M00, M02, several __init__.py)
- Scattered classification dicts (NAICS codes in _naics_io_parser, NIPA65 in _naics_io_parser, BLS sector mapping in L04, industry descriptions in L06)
- No explicit dependency graph — order determined by filename sort + PRIORITY hack
- V02 range bounds hardcoded in Python, not in config
- Each L## script re-implements FRED/BEA fetch logic

### v7.0 (proposed)
```
pipeline/
  config/
    series_registry.json       (unchanged, single source of truth)
    classifications.json       (ALL sector classifications in one place)
    validation_config.json     (unchanged)
    api_sources.json           (FRED/BEA series IDs, endpoints, cache policy)
  
  sources/
    book_data.py               (reads ALL book-period CSVs: H.1, Table5_7, Employment, etc.)
    api_fetch.py               (generic FRED/BEA fetcher, reads api_sources.json)
    io_matrices.py             (SIC + NAICS IO parsing, reads classifications.json)
  
  compute/
    revenue.py                 (T501-T503: TP*, C*m, GFP*)
    variable_capital.py        (T504-T505: V*, S*)
    exploitation.py            (T506-T507: e, surplus ratio)
    composition.py             (T508-T510: CON*, IG*, C*/V*)
    labor_shares.py            (T511-T512: Lp/L, V*/W)
    employment.py              (T515-T516: Lp, Lu)
    profit_rates.py            (T513-T514: r*, r*_adj)
    taxes.py                   (T601-T604: personal, social, indirect, total)
    benefits.py                (T605-T606: govt benefits, services)
    nsw.py                     (T607-T609: NSW, NSW/V*, NSW/NI)
    io_analysis.py             (T401-T402, T701-T703: IO matrices, labor values)
    comparison.py              (T201, T801, T901: cross-study, summary)
    studies.py                 (N1001-N1704: all 26 external study series)
    analytical.py              (A07-A10: social burden, exploitation, productivity)
  
  validate/
    checks.py                  (ALL validators in one file, reads validation_config.json)
  
  output/
    master_db.py               (master database CSV/XLSX)
    figures.py                 (all 11 figures)
    chopped.py                 (Anu Chopped CSVs)
    extenbooks.py              (Anu Extenbook XLSX)
    shiny.py                   (Shiny data bridge)
  
  run.py                       (orchestrator, explicit DAG)
```

**Key differences**:
- **14 compute scripts** (was 19 P## + 4 M##) — M01/M99 logic folded into compute scripts
- **1 validation script** (was 15 V##) — all checks in one file with config-driven dispatch
- **1 source fetcher** (was 6 L## scripts with FRED/BEA logic) — generic API handler
- **1 classification config** (was dicts in 5 files) — centralized JSON
- **Explicit DAG** in run.py — no PRIORITY hacks or filename-sort ordering
- **No manual phase** — adjustments are part of computation, not a separate pass

---

## Detailed File Specifications

### config/classifications.json

Consolidates ALL sector classification data currently scattered across:
- `_naics_io_parser.py` CLASSIFICATION dict (67 NAICS codes)
- `_naics_io_parser.py` NIPA65_CLASSIFICATION dict (22 line numbers)
- `L06` INDUSTRY_CLASSIFICATION dict (19 industry descriptions)
- `_sector_variable_capital.py` PRODUCTIVE_LINES dict (13 line numbers)
- `P01_process_revenue.py` CLASSIFICATION import
- `A07` social burden rate sector lists

```json
{
  "naics_io": {
    "111CA": {"name": "Farms", "class": "productive"},
    "42": {"name": "Wholesale trade", "class": "trading"},
    "521CI": {"name": "Fed Reserve, credit intermediation", "class": "unproductive"},
    ...
  },
  "nipa_65_fte": {
    "4": {"name": "Agriculture", "class": "productive"},
    "35": {"name": "Wholesale trade", "class": "trading"},
    ...
  },
  "nipa_62_compensation": {
    "4": {"name": "Agriculture", "class": "productive"},
    ...
  },
  "bls_production_worker": {
    "CES1000000006": {"sector": "Mining", "type": "production"},
    "CES1000000001": {"sector": "Mining", "type": "total"},
    ...
  },
  "nsw_expenditure_groups": {
    "income_security": {"group": 1, "allocation": 1.0},
    "education": {"group": 2, "allocation": "labor_share"},
    "national_defense": {"group": 3, "allocation": 0.0},
    ...
  }
}
```

### config/api_sources.json

Consolidates ALL API fetch configuration:

```json
{
  "fred": {
    "base_url": "https://api.stlouisfed.org/fred/series/observations",
    "series": {
      "PAYEMS": {"name": "Total nonfarm employment", "frequency": "a", "start": "1948-01-01", "units": "thousands"},
      "GDPDEF": {"name": "GDP deflator", "frequency": "a", "start": "1929-01-01", "units": "index"},
      "USTRADE": {"name": "Trade employment", "frequency": "a", "start": "1948-01-01"},
      "CEU5500000001": {"name": "FIRE employment", "frequency": "a", "start": "1948-01-01"},
      "CEU9000000001": {"name": "Government employment", "frequency": "a", "start": "1948-01-01"},
      "TCU": {"name": "Capacity utilization", "frequency": "a", "start": "1967-01-01"}
    }
  },
  "bea": {
    "base_url": "https://apps.bea.gov/api/data",
    "datasets": {
      "fixed_assets": {"TableName": "FAAt403", "DataSetName": "FixedAssets", "Year": "ALL"}
    }
  }
}
```

### sources/book_data.py

Single module that reads ALL book-period data:

```python
def load_table_h1() -> pd.DataFrame:
    """42-year annual S*, VA*, V*, S*/V*, TP*, GFP*, P+, EC from digitized Table H.1."""

def load_table_5_7() -> pd.DataFrame:
    """42-year Lp/L, V*/W ratios from Table 5.7 KeyRatios CSV."""

def load_employment() -> pd.DataFrame:
    """42-year T515 (Lp), T516 (Lu) from Employment CSV."""

def load_revenue_accounts() -> pd.DataFrame:
    """14-year TP*, C*m, GFP* from Table E.2 RevenueAccounts CSV."""

def load_tax_accounts() -> pd.DataFrame:
    """38-year T601-T604 from Table 6.1 TaxAccounts CSV."""

def load_benefit_accounts() -> pd.DataFrame:
    """38-year T605-T606 from Table 6.2 BenefitAccounts CSV."""

def load_nsw() -> pd.DataFrame:
    """74-year T607, T609 from Table 6.3 NetSocialWage CSV."""

def load_io_matrices(year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """A-matrix and Leontief inverse for a single SIC benchmark year."""

def load_profit_rates() -> pd.DataFrame:
    """42-year T513, T514 from ProfitRates CSV."""

def load_composition() -> pd.DataFrame:
    """42-year T507, T510 from ExploitationComposition CSV."""

def load_mohun() -> pd.DataFrame:
    """42-year Mohun exploitation rates for cross-validation."""

def load_external_study(study_id: str) -> pd.DataFrame:
    """Load external study data by ID (turkey, cronin_nz, moos, etc.)."""
```

### sources/api_fetch.py

Generic FRED/BEA fetcher with caching:

```python
def fetch_fred(series_id: str, api_key: str = None) -> pd.Series:
    """Fetch any FRED series. Uses config/api_sources.json for parameters. Caches to raw-data/api/."""

def fetch_bea(dataset: str, api_key: str = None) -> pd.DataFrame:
    """Fetch any BEA dataset. Uses config/api_sources.json for parameters. Caches to raw-data/api/."""

def load_nipa_table(table_path: Path, line_filter: str = None) -> pd.DataFrame:
    """Load a pre-fetched NIPA CSV and optionally filter by LineDescription."""

def get_api_keys() -> dict:
    """Load FRED_API_KEY and BEA_API_KEY from api_keys.env."""
```

### sources/io_matrices.py

```python
def parse_sic_benchmark(year: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Parse SIC IO matrices. Returns (A_matrix, B_matrix, gross_output)."""

def parse_naics_benchmark(year: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Parse NAICS IO from BEA JSON. Returns (A_matrix, B_matrix, gross_output)."""

def compute_productive_ratios() -> pd.DataFrame:
    """Compute annual IO productive ratios (output, materials, employment) 1997-2024."""

def classify_sector(code: str) -> str:
    """Return 'productive', 'trading', 'unproductive', or 'government' from classifications.json."""
```

### compute/*.py — The Core Pipeline

Each compute module follows the same pattern:

```python
"""Module docstring with formulas and book references."""

import pandas as pd
from sources.book_data import load_table_h1
from sources.api_fetch import fetch_fred, load_nipa_table

DEPENDS_ON = ["revenue"]  # explicit dependency declaration

def compute() -> dict[str, pd.DataFrame]:
    """Compute all series in this module. Returns {series_id: DataFrame}."""
    ...
    return {"T504": t504_df, "T505": t505_df}
```

**Critical difference from v6.0**: The `DEPENDS_ON` list is read by `run.py` to build a proper DAG. No more PRIORITY constants or filename-sort ordering.

**M01 adjustment folded in**: Each compute module applies its own adjustments internally. For example, `variable_capital.py` computes V* and then applies the ec_u/ec_p adjustment in the same function — no separate M01 pass. The adjustment reads from book data + BEA data, never from its own previous output.

### compute/variable_capital.py (example of full module)

```python
"""T504 (V*) and T505 (S* = VA* - V*).

Book period: Table H.1 (V_star, S_star columns, billions).
Extension: V*[yr] = V*[1989] × (T512[yr] / T512[1989]) for 1990-1997,
           V*[yr] = W[yr] × T512[yr] for 1998+ (W from BEA NIPA T20100).
           ec_u/ec_p adjustment applied in-line (not a separate M01 pass).

Source: Appendix G methodology. DEC-020 documents the Table H.1 correction.
"""

DEPENDS_ON = ["labor_shares"]  # needs T512 for extension

def compute() -> dict[str, pd.DataFrame]:
    h1 = load_table_h1()
    t512 = _get_dependency("T512")  # from labor_shares.compute()
    w = load_nipa_table(NIPA_T20100_PATH, "compensation")
    ec_ratio = _compute_ec_ratio()  # inline, no M01
    
    # Book period
    v_star_book = h1["V_star"]
    s_star_book = h1["S_star"]
    
    # Extension with ec_u/ec_p adjustment applied immediately
    v_star_ext = _extend_v_star(v_star_book, t512, w, ec_ratio)
    s_star_ext = _extend_s_star(...)
    
    return {
        "T504": _build_output(v_star_book, v_star_ext),
        "T505": _build_output(s_star_book, s_star_ext),
    }
```

### validate/checks.py

All 15 current validators in one file, config-driven:

```python
def run_all_checks(series: dict[str, pd.DataFrame], config: dict) -> list[dict]:
    results = []
    results.extend(_check_reference_values(series, config))    # V01
    results.extend(_check_ranges(series, config))              # V02
    results.extend(_check_continuity(series, config))          # V03
    results.extend(_check_completeness(series, config))        # V04
    results.extend(_check_cross_series(series, config))        # V05
    results.extend(_check_splice_quality(series, config))      # V06
    results.extend(_check_extension_overlap(series, config))   # V07
    results.extend(_check_hash_integrity(series, config))      # V08
    results.extend(_check_mohun(series, config))               # V09
    results.extend(_check_io_consistency(series, config))      # V10
    results.extend(_check_external_benchmarks(series, config)) # V11
    results.extend(_check_nsw_cross_study(series, config))     # V12
    results.extend(_check_robin(series, config))               # V13
    results.extend(_check_units(series, config))               # V14
    results.extend(_check_freshness(series, config))           # V15
    return results
```

### run.py — Explicit DAG Orchestrator

```python
"""AS2 NickyData v7.0 — DAG-based orchestrator.

Builds dependency graph from DEPENDS_ON declarations, topologically sorts,
executes in order. No PRIORITY hacks or filename sorting.
"""

from compute import (
    revenue, variable_capital, exploitation, composition,
    labor_shares, employment, profit_rates,
    taxes, benefits, nsw, io_analysis, comparison, studies, analytical
)

COMPUTE_MODULES = [
    revenue, variable_capital, exploitation, composition,
    labor_shares, employment, profit_rates,
    taxes, benefits, nsw, io_analysis, comparison, studies, analytical
]

def build_dag() -> list:
    """Topological sort of compute modules by DEPENDS_ON."""
    ...

def run():
    # 1. Fetch all API data
    api_fetch.fetch_all()
    
    # 2. Run compute modules in dependency order
    all_series = {}
    for module in build_dag():
        result = module.compute()
        all_series.update(result)
        _write_series(result)
    
    # 3. Validate
    checks = validate.checks.run_all_checks(all_series, config)
    
    # 4. Generate outputs
    output.master_db.generate(all_series)
    output.figures.generate(all_series)
    output.chopped.generate(all_series)
```

---

## Migration Steps

### Step 1: Archive v6.0 (30 minutes)

```bash
mkdir -p Technical/_archive/v6.0_2026-05-09/
cp -r Technical/NickyData/code/ Technical/_archive/v6.0_2026-05-09/code/
cp -r Technical/NickyData/utils/ Technical/_archive/v6.0_2026-05-09/utils/
cp Technical/NickyData/run.py Technical/_archive/v6.0_2026-05-09/run.py
```

Also save the current output hashes for comparison:
```bash
python run.py --test-all  # baseline run
cp data/final-data/logs/HASH_MANIFEST.json Technical/_archive/v6.0_2026-05-09/HASH_MANIFEST_v6.json
```

### Step 2: Create v7.0 scaffold (1 hour)

Create the new directory structure:
```
pipeline/
  __init__.py
  config/
    classifications.json
    api_sources.json
  sources/
    __init__.py
    book_data.py
    api_fetch.py
    io_matrices.py
  compute/
    __init__.py
    (14 modules)
  validate/
    __init__.py
    checks.py
  output/
    __init__.py
    (5 modules)
  run.py
```

### Step 3: Build sources layer (2-3 hours)

Extract all data loading logic from L01-L18 into:
- `book_data.py`: Pure readers for book-period CSVs (no API calls, no computation)
- `api_fetch.py`: Generic FRED/BEA fetcher using `api_sources.json`
- `io_matrices.py`: SIC + NAICS IO parsing using `classifications.json`

**Test**: Each source function returns correct data for known years.

### Step 4: Build compute layer (4-6 hours)

Migrate processing logic from P01-P21 + M01/M99 into 14 compute modules.

**Order** (by dependency):
1. `employment.py` (T515, T516) — no upstream dependencies
2. `taxes.py` (T601-T604) — no upstream dependencies  
3. `benefits.py` (T605-T606) — no upstream dependencies
4. `revenue.py` (T501-T503) — no upstream dependencies
5. `labor_shares.py` (T511, T512) — depends on IO ratios
6. `variable_capital.py` (T504, T505) — depends on T512
7. `exploitation.py` (T506, T507) — depends on T504, T505
8. `composition.py` (T508-T510) — depends on T502, T504
9. `profit_rates.py` (T513, T514) — depends on T505, K*
10. `nsw.py` (T607-T609) — depends on T604, T605, T606
11. `io_analysis.py` (T401, T402, T701-T703) — IO matrices
12. `comparison.py` (T201, T801, T901) — depends on multiple
13. `studies.py` (N1001-N1704) — depends on some T-series
14. `analytical.py` (A07-A10) — depends on multiple

**For each module**:
1. Extract the relevant logic from v6.0 P## + L## scripts
2. Fold in M01/M99 adjustments (apply ec_u/ec_p inline, not as separate pass)
3. Add `DEPENDS_ON` declaration
4. Add `compute()` function returning `{series_id: DataFrame}`
5. Test: output matches v6.0 output for the same series

### Step 5: Build validation layer (1-2 hours)

Consolidate V01-V15 into single `checks.py` with config-driven dispatch.
Each check function takes `(series_dict, config)` and returns a list of results.
V02 range bounds come from `validation_config.json` (already mostly there).

### Step 6: Build output layer (1-2 hours)

Migrate O01-O06 into 5 output modules.
These are straightforward — they just format data into CSVs, XLSX, PNGs.

### Step 7: Build orchestrator (1 hour)

Write the DAG-based run.py that:
1. Reads `DEPENDS_ON` from each compute module
2. Topologically sorts
3. Executes in order
4. Passes results to validation + output

### Step 8: Verification (2 hours)

Compare v7.0 output against v6.0 baseline:
1. Hash every T*.csv and N*.csv from both runs
2. For each series: verify book column is identical, combined column matches within 0.001
3. Run v6.0 V01 reference values against v7.0 output
4. Verify: same 29 V01 PASS, same V02 86/0

### Step 9: Cleanup (1 hour)

Once verified:
1. Move old `code/` directory to `_archive/v6.0_code/` (already done in Step 1)
2. Update `run.py` at NickyData root to point to `pipeline/run.py`
3. Update any external references (Shiny app, documentation)
4. Final clean-build test: 3 consecutive PASS runs

---

## Effort Summary

| Step | What | Hours |
|------|------|-------|
| 1 | Archive v6.0 | 0.5 |
| 2 | Create scaffold | 1.0 |
| 3 | Sources layer | 2.5 |
| 4 | Compute layer | 5.0 |
| 5 | Validation layer | 1.5 |
| 6 | Output layer | 1.5 |
| 7 | Orchestrator | 1.0 |
| 8 | Verification | 2.0 |
| 9 | Cleanup | 1.0 |
| **Total** | | **~16 hours** |

**Sessions**: 3-4 sessions of 4-5 hours each.

---

## What v7.0 Eliminates

| v6.0 Problem | v7.0 Solution |
|---------------|--------------|
| M01 feedback loop | Adjustments inline in compute modules |
| PRIORITY ordering hack | Explicit DEPENDS_ON DAG |
| importlib sub-script loading | Direct Python imports |
| Scattered classification dicts | Single classifications.json |
| 6 different FRED/BEA fetch implementations | 1 generic api_fetch.py |
| 15 separate validator files | 1 checks.py with config dispatch |
| Stale files from previous runs causing failures | Clean data flow, no cross-run contamination |
| 71 code files | ~25 files (65% reduction) |

## What v7.0 Preserves

- All 59 T/N-series + 3 analytical series
- series_registry.json (unchanged)
- validation_config.json (unchanged)
- All book-period source CSVs (unchanged)
- All FRED/BEA cached API responses (unchanged)
- Digitized Table H.1 (unchanged)
- IO productive ratios methodology (unchanged)
- Every formula and data transformation (verified by hash comparison)

---

*Plan authored 2026-05-09. Based on complete audit of v6.0 codebase (71 Python files, 8 phases, 20 decision log entries, 17/40 KB chunks read).*
