# RMWND Utilities API Reference

Auto-generated from docstrings in `Technical/code/utils/` via `inspect`. 
Run `python Technical/tools/gen_api_reference.py` to regenerate after touching any utils module.

> **Read-only contract**: every documented function here is safe to call from L01/P02/V03 
> scripts. None of these helpers write to `series_registry.json`, `PIPELINE_STATE.json`, 
> the LEDGER, the MANIFEST, or `SUBSERIES_PLAN.json`.

## Modules

- [`registry_validator`](#module-registry-validator) — Registry-backed benchmark/derived-statistic loader for V03 validators.
- [`bls_cache`](#module-bls-cache) — Cached BLS CES employment reader (productive vs total).
- [`series`](#module-series) — Parametrized building blocks: BookColumnLoader, BenchmarkValidator, pipeline glue.
- [`io`](#module-io) — IO helpers: book-table reader, registry loader, per-series CSV writers.
- [`paths`](#module-paths) — Canonical project paths (ROOT, DATA_*, REGISTRY, …).
- [`dpr_status_sync`](#module-dpr-status-sync) — Sync each `**Status**:` DPR header with the registry's series status.
- [`precommit_check`](#module-precommit-check) — Pre-commit checks for Decisions 0001-0008 (extenbook, refs, naming, chopped, verbatim, year-keys).

---

## Module: `registry_validator`

**Purpose:** Registry-backed benchmark/derived-statistic loader for V03 validators.

**Source:** `Technical/code/utils/registry_validator.py`


**Overview:**

Registry-backed benchmark loader for V03 validators.

Created 2026-05-24 per Decision 0002 (registry is the canonical source of truth
for `validation.reference_values`). The hyper-review flagged hardcoded benchmark
dicts inside V03 validator scripts as brittle: any change to the registry would
silently diverge from the validator's expectations. Routing every V03 through
`get_reference_values()` keeps both sides in lockstep.

Usage from a V03 script:

    from utils.registry_validator import get_reference_values
    benchmarks = get_reference_values("S506")  # -> {1948: 1.70, 1958: 2.01, ...}

The function:
- Loads `Technical/series_registry.json` once per process (cached).
- Reads `series[<SID>].validation.reference_values`.
- Coerces year keys to `int` and values to `float`.
- Filters out non-year keys (e.g., `1948_e` composite keys used by S901).
- Raises a clear KeyError if the series or its reference_values are missing.

NEVER write to the registry from this module. It is read-only.


### Functions

### `get_derived_statistics(sid: 'str') -> 'dict'`

Return `validation.derived_statistics` for a series per Decision 0008.

Decision 0008 split the v1.0 `validation.reference_values` field into two:

- `reference_values` (year-keyed scalars only, `{<year_int>: <float>}`)
- `derived_statistics` (free-form statistic names, `{<str>: <number>}`)

Examples of derived statistics: `mean`, `std`, `structural_shift`,
`n_negative`, `1959_1997_mean`, `1948_e`. Use this helper from V03
validators that need to consume those statistics; use
`get_reference_values()` for year-anchor checks.

Args:
    sid: Canonical series ID (e.g., "ES1601").

Returns:
    dict mapping statistic name to value. Returns an empty dict (not an
    error) for series that have no derived statistics, so callers can
    safely treat absence as "no stat-based checks to run".

### `get_reference_values(sid: 'str', *, year_keys_only: 'bool' = True) -> 'dict[int, float]'`

Return the benchmark dict for a series from the registry.

Args:
    sid: Canonical series ID (e.g., "S506").
    year_keys_only: If True (default), only include keys parseable as int
        years. Set False to keep composite keys like "1948_e" (S901 case).

Returns:
    dict mapping int year -> float value. May be empty if the series carries
    no reference values (returns empty dict, not error, to allow validators
    that don't rely on benchmarks).

### `get_tolerance_class(sid: 'str', *, default: 'Optional[str]' = None) -> 'Optional[str]'`

Return the tolerance class string from the registry, or `default`.


---

## Module: `bls_cache`

**Purpose:** Cached BLS CES employment reader (productive vs total).

**Source:** `Technical/code/utils/bls_cache.py`


**Overview:**

Read BLS CES cached CSV responses.

The BLS CES cache lives at:
  Inputs/ST2/Inputs/API_Data/BLS/bls_ces_production_workers.csv

Format: wide-by-series with first column `year`, then one column per BLS CES
series ID. Each cell is `production workers (thousands)` or `all employees
(thousands)` depending on the series.

Coverage notes (from the cache as of 2026-02-24):
  - CES0500000001 (total private all employees):       1948-2024
  - CES0500000006 (total private production workers):  1964-2024 (NA before)
  - CES0600000001 (goods-producing all employees):     1948-2024
  - CES0600000006 (goods-producing production workers):1948-2024
  - CES1000000006 (mining/logging production):         1948-2024
  - CES2000000006 (construction production):           1948-2024
  - CES3000000006 (manufacturing production):          1948-2024
  - CES1000000001/2000000001/3000000001 (all employees): 1948-2024

For Shaikh-Tonak's productive employment Lp, the productive super-sectors
covered in this 5-super-sector cache are the goods-producing sectors
(mining/logging + construction + manufacturing). The book's full Appendix C
concordance covers 85 SIC sectors and additionally includes transportation
& public utilities and productive services — that finer partition is NOT
in this cache. This divergence is documented in the EPR.


### Constants

| Name | Value |
|---|---|
| `BLS_CES_CACHE` | `D:\Arcanum\Projects\RMWND\Inputs\ST2\Inputs\API_Data\BLS\bls_ces_production_workers.csv` |
| `PRODUCTIVE_PROD_WORKER_SERIES` | `['CES1000000006', 'CES2000000006', 'CES3000000006']` |
| `ROOT` | `D:\Arcanum\Projects\RMWND\Technical` |
| `TOTAL_PRIVATE_ALL_EMPLOYEES` | `'CES0500000001'` |


### Functions

### `load_bls_ces() -> 'pd.DataFrame'`

Load the cached BLS CES production-workers wide table.

Returns DataFrame with `year` and one column per CES series ID, values
in thousands. NaN where the series is not published for that year.

### `productive_employment_annual() -> 'pd.DataFrame'`

Sum productive-sector production workers by year (thousands).

Returns DataFrame [year, value] over 1948-2024. `value` is the sum of
production workers across the 3 goods-producing super-sectors
(mining/logging + construction + manufacturing) that compose the
"productive" partition in the 5-super-sector BLS CES cache.

CAVEAT: This is a super-sector aggregation. The book's Appendix C uses
85 SIC sectors and additionally includes transportation/public utilities
and productive services. See S511/S515 EPRs for the documented divergence.

### `total_employment_annual() -> 'pd.DataFrame'`

Total private all-employees (thousands) by year, 1948-2024.

Used as the denominator L for the productive labor share Lp/L.


---

## Module: `series`

**Purpose:** Parametrized building blocks: BookColumnLoader, BenchmarkValidator, pipeline glue.

**Source:** `Technical/code/utils/series.py`


**Overview:**

Parametrized building blocks shared by per-series L##/P##/V## scripts.

Per the simplicity rule: each per-series script remains a thin, readable file
that declares its parameters and calls these helpers. The helpers don't hide
anything — they centralize the few mechanical steps that are identical across
every Ch5 series (read a wide CSV, project one column, validate against a
dict of benchmark years).


### Constants

| Name | Value |
|---|---|
| `TOLERANCES` | `{'dollar_series': {'rel': 0.01, 'abs': 1.0}, 'rate_series': {'rel': 0.001, 'a...` |


### Classes

### class `BenchmarkValidator`

Validates a per-series final CSV against a dict of {year: book_value}.


**Constructor:** `BenchmarkValidator(series_id: 'str', tolerance_class: 'str', benchmarks: 'dict[int, float]', subseries_filter: 'str | None' = None) -> None`


**Methods:**


- `run(self, final_csv: 'Path') -> 'dict'`
  
  _(no docstring)_


### class `BookColumnLoader`

Load one column from a digitized book table CSV (wide format with `year` index).

`unit_scale` divides raw values (e.g., 1000.0 converts millions→billions).
Defaults to 1.0 (no conversion). The DPR documents the conversion when
used so the provenance chain stays traceable.


**Constructor:** `BookColumnLoader(series_id: 'str', subseries_id: 'str', source_file: 'Path', source_column: 'str', units: 'str', unit_scale: 'float' = 1.0) -> None`


**Methods:**


- `load(self) -> 'pd.DataFrame'`
  
  _(no docstring)_



### Functions

### `cross_source_e2_check(series_id: 'str', h1_final_csv: 'Path', e2_file: 'Path', e2_column: 'str', subseries_filter: 'str', tolerance_class: 'str' = 'dollar_series') -> 'dict'`

Duplicate-source consistency check: compare H.1-derived series to E.2 for overlap years.

Used for S501-S510 (the revenue-account series): Table H.1 and Table E.2
should report identical values for 1948-1961. Any divergence indicates a
digitization error in one of the two tables.

### `run_pipeline_for_series(loader: 'BookColumnLoader', source_label: 'str') -> 'Path'`

Standard run sequence: load -> process -> write intermediate + final CSV.

### `standard_passthrough_processor(loader: 'BookColumnLoader', source_label: 'str') -> 'pd.DataFrame'`

Standard book-period processor: pass-through with stage + provenance columns.

Returns a frame ready to be written to intermediate/final. Use when the
book series IS the canonical published value (no transformation needed for
the book period; extension/splice stages add rows in later pipeline runs).


---

## Module: `io`

**Purpose:** IO helpers: book-table reader, registry loader, per-series CSV writers.

**Source:** `Technical/code/utils/io.py`


**Overview:**

IO helpers shared by loaders, processors, and validators.


### Functions

### `get_series_entry(series_id: 'str') -> 'dict'`

Return the registry entry for one series, raising if absent.

### `load_registry() -> 'dict'`

Load the canonical series registry.

### `read_book_table(path: 'Path') -> 'pd.DataFrame'`

Read a digitized book-table CSV.

Handles three header conventions seen in the project's source CSVs:
  1. Leading `#`-prefixed comment row (Ch5 tables: H.1, E.2, 5.7, E.3)
  2. Multi-row title headers ending in a column row starting with `year`
     (Ch6 tables: 6.1, 6.2, 6.3 — first row is title, second is source,
     third is column header)
  3. No header preamble — first row is the column header

Returns a DataFrame with the column-header row as columns.

### `write_series_csv(df: 'pd.DataFrame', series_id: 'str', *, stage: 'str' = 'intermediate') -> 'Path'`

Write a single-series CSV to data/{stage}/{series_id}.csv. Returns the path.

### `write_validation_result(series_id: 'str', result: 'dict') -> 'Path'`

Write a per-series validation result for S03 to roll up.


---

## Module: `paths`

**Purpose:** Canonical project paths (ROOT, DATA_*, REGISTRY, …).

**Source:** `Technical/code/utils/paths.py`


**Overview:**

Central path resolution for the replication pipeline.


### Constants

| Name | Value |
|---|---|
| `BOOK_TABLES` | `D:\Arcanum\Projects\RMWND\Technical\data\source\book_tables` |
| `CHOPPED_DIR` | `D:\Arcanum\Projects\RMWND\Technical\chopped` |
| `CONCORDANCES` | `D:\Arcanum\Projects\RMWND\Technical\data\source\concordances` |
| `DATA_FINAL` | `D:\Arcanum\Projects\RMWND\Technical\data\final` |
| `DATA_INTERMEDIATE` | `D:\Arcanum\Projects\RMWND\Technical\data\intermediate` |
| `DATA_RAW` | `D:\Arcanum\Projects\RMWND\Technical\data\raw` |
| `DATA_SOURCE` | `D:\Arcanum\Projects\RMWND\Technical\data\source` |
| `DOCS_SERIES` | `D:\Arcanum\Projects\RMWND\Technical\docs\series` |
| `EXTENBOOKS_DIR` | `D:\Arcanum\Projects\RMWND\Technical\extenbooks` |
| `EXTERNAL_STUDIES` | `D:\Arcanum\Projects\RMWND\Technical\data\source\external_studies` |
| `EXTERNAL_STUDIES_DIR` | `D:\Arcanum\Projects\RMWND\Technical\data\source\external_studies` |
| `LEDGER` | `D:\Arcanum\Projects\RMWND\Technical\ANU_LEDGER.json` |
| `PIPELINE_STATE` | `D:\Arcanum\Projects\RMWND\Technical\PIPELINE_STATE.json` |
| `REGISTRY` | `D:\Arcanum\Projects\RMWND\Technical\series_registry.json` |
| `RESEARCH_DIR` | `D:\Arcanum\Projects\RMWND\Technical\research` |
| `ROOT` | `D:\Arcanum\Projects\RMWND\Technical` |
| `VALIDATION_DIR` | `D:\Arcanum\Projects\RMWND\Technical\data\intermediate\validation` |


---

## Module: `dpr_status_sync`

**Purpose:** Sync each `**Status**:` DPR header with the registry's series status.

**Source:** `Technical/code/utils/dpr_status_sync.py`


**Overview:**

DPR Status Sync
================

Syncs each DPR file's `**Status**:` header line with the canonical
`status` field in series_registry.json.

Behavior per DPR
----------------
* Parse first line in the file that matches the regex
  ``^(?:- )?\*\*Status\*\*:\s*`?([A-Za-z0-9_]+)`?``.
* If the parsed status equals the registry status: skip (already correct).
* If different: rewrite that single line in place, preserving the original
  bullet style (``- **Status**: `value` ...`` vs ``**Status**: value ...``)
  and any trailing annotation (text in parens or after the value token).
* If no Status line exists at all: insert ``**Status**: <value>`` directly
  after the title block (line that starts with ``# `` plus one blank).

Constraints
-----------
* series_registry.json is read-only.
* Only DPR files in Technical/docs/series/ may be modified.
* All other content of each DPR is preserved byte-for-byte.

Usage
-----
    python Technical/code/utils/dpr_status_sync.py
        [--dry-run]
        [--registry PATH]
        [--series-dir PATH]


### Constants

| Name | Value |
|---|---|
| `DEFAULT_REGISTRY` | `D:\Arcanum\Projects\RMWND\Technical\series_registry.json` |
| `DEFAULT_SERIES_DIR` | `D:\Arcanum\Projects\RMWND\Technical\docs\series` |
| `PROJECT_ROOT` | `D:\Arcanum\Projects\RMWND` |
| `STATUS_LINE_RE` | `re.compile('^(?P<prefix>(?:-\\s+)?\\*\\*Status\\*\\*:\\s*)(?P<backtick_open>`...` |


### Functions

### `load_registry(path: 'Path') -> 'dict'`

_(no docstring)_

### `main(argv: 'list[str] | None' = None) -> 'int'`

_(no docstring)_

### `sync_dpr(dpr_path: 'Path', target_status: 'str') -> 'str'`

Returns one of: 'already-correct', 'synced', 'inserted', 'skipped'.


---

## Module: `precommit_check`

**Purpose:** Pre-commit checks for Decisions 0001-0008 (extenbook, refs, naming, chopped, verbatim, year-keys).

**Source:** `Technical/code/utils/precommit_check.py`


**Overview:**

Pre-commit check for RMWND Anu Framework Decisions 0001-0008.

Standalone, dependency-light enforcement of the eight binding decisions that
govern the RMWND replication project. Designed to be runnable either as a git
pre-commit hook (`--staged`) or manually across the whole project (`--all`).

Usage
-----
    # Whole-project audit (default if no git repo)
    python Technical/code/utils/precommit_check.py --all

    # Staged-file mode (git pre-commit hook default)
    python Technical/code/utils/precommit_check.py --staged

    # Ad-hoc subset (glob patterns relative to project root)
    python Technical/code/utils/precommit_check.py --files "Technical/chopped/*.csv"

Exit code: 0 on all PASS / WARN, 1 on any FAIL.

Authored 2026-05-23 for v1.1 Phase 2 framework infrastructure. Read-only with
respect to series_registry.json, PIPELINE_STATE.json, LEDGER, MANIFEST, and
SUBSERIES_PLAN.json — this script never writes data artifacts.

The eight checks
----------------
- Decision 0001: extenbook 4-sheet (or 5-sheet w/ Validation) canonical layout.
- Decision 0002: every registry series has non-empty validation.reference_values
  (allowed-empty only when derived_statistics is non-empty, per 0008).
- Decision 0003: extension binary invariant
  * extension == null  -> status MUST NOT be 'validated_book_and_extension' (FAIL)
  * extension != null  -> status SHOULD contain 'extension' (WARN — project may
    legitimately defer the upgrade until extension is actually executed; see
    project CLAUDE.md).
- Decision 0004: L01 / P02 / V03 compact naming `<phase>_<SID>[_<suffix>].py`.
- Decision 0005: chopped CSV wide format (row 1 # metadata, row 2 'Year', row 3+ data).
- Decision 0006: code is source of truth (heuristic always-PASS; documentation).
- Decision 0007: research JSON has >= 3 canonical verbatim_quote entries with
  required fields (entry_type, content/verbatim_quote, source_ref).
- Decision 0008: validation.reference_values keys parse as int years; values
  are finite floats. derived_statistics is unconstrained.


### Constants

| Name | Value |
|---|---|
| `ALLOWED_EXTENBOOK_SHEETS_5` | `['Data', 'Provenance', 'Research', 'Construction', 'Validation']` |
| `ALL_CHECKS` | `[('Decision-0001', <function check_decision_0001 at 0x00000186A6D8BC40>), ('D...` |
| `CANONICAL_EXTENBOOK_SHEETS` | `['Data', 'Provenance', 'Research', 'Construction']` |
| `PHASE_PREFIXES` | `('L01_', 'P02_', 'V03_', 'M04_', 'A05_', 'O06_', 'S00_')` |
| `PROJECT_ROOT` | `D:\Arcanum\Projects\RMWND` |
| `REGISTRY_PATH` | `D:\Arcanum\Projects\RMWND\Technical\series_registry.json` |
| `SCRIPT_PATH` | `D:\Arcanum\Projects\RMWND\Technical\code\utils\precommit_check.py` |
| `TECHNICAL_ROOT` | `D:\Arcanum\Projects\RMWND\Technical` |


### Classes

### class `Report`

_(no docstring)_


**Constructor:** `Report() -> 'None'`


**Methods:**


- `add(self, decision: 'str', level: 'str', path: 'str', message: 'str') -> 'None'`
  
  _(no docstring)_


- `counts(self) -> 'dict[str, int]'`
  
  _(no docstring)_


- `exit_code(self) -> 'int'`
  
  _(no docstring)_


### class `Result`

_(no docstring)_


**Constructor:** `Result(decision: 'str', level: 'str', path: 'str', message: 'str') -> 'None'`


**Methods:**


- `fmt(self) -> 'str'`
  
  _(no docstring)_



### Functions

### `check_decision_0001(files: 'Iterable[Path]', rpt: 'Report') -> 'None'`

_(no docstring)_

### `check_decision_0002(files: 'Iterable[Path]', rpt: 'Report') -> 'None'`

_(no docstring)_

### `check_decision_0003(files: 'Iterable[Path]', rpt: 'Report') -> 'None'`

_(no docstring)_

### `check_decision_0004(files: 'Iterable[Path]', rpt: 'Report') -> 'None'`

_(no docstring)_

### `check_decision_0005(files: 'Iterable[Path]', rpt: 'Report') -> 'None'`

_(no docstring)_

### `check_decision_0006(files: 'Iterable[Path]', rpt: 'Report') -> 'None'`

_(no docstring)_

### `check_decision_0007(files: 'Iterable[Path]', rpt: 'Report') -> 'None'`

_(no docstring)_

### `check_decision_0008(files: 'Iterable[Path]', rpt: 'Report') -> 'None'`

_(no docstring)_

### `discover_files(args: 'argparse.Namespace') -> 'tuple[list[Path], str]'`

Return (files, mode_label).

### `load_registry() -> 'dict | None'`

_(no docstring)_

### `main(argv: 'list[str] | None' = None) -> 'int'`

_(no docstring)_

