# Anu Replicator v3.0 — ST2 Data Replication Pipeline

Reproduces all data series from *Measuring the Wealth of Nations* (Shaikh & Tonak, 1994)
with extensions to 2024 using BEA/BLS API data.

## Architecture

The pipeline uses a **four-phase architecture**:

1. **Loading Phase (L##)** — Parses chopped CSV source files and external data into
   standardized `{SERIES_ID}_parsed.csv` files in `data/parsed-raw/`.
2. **Processing Phase (P##)** — Transforms parsed data into final series with book values,
   extensions, and cross-validation. Outputs to `data/final-data/series/`.
3. **Validation Phase (V##)** — Systematic verification of all outputs: reference values,
   range checks, continuity, completeness, cross-series identities, splice quality,
   extension overlap, and hash integrity. Outputs `VALIDATION_REPORT.json`.
4. **Manual Adjustment Phase (M##)** — Documented, justified corrections applied to
   final data. Outputs to `data/adjusted-final-data/` with full audit trail in
   `ADJUSTMENT_MANIFEST.json`.

After processing, optional export phases write Shiny-compatible CSVs, figures, a
replication report, and the `ANU_LEDGER.json` health dashboard.

```
Source CSVs ──► L01-L14 (Loading) ──► parsed-raw/
                                         │
                                         ▼
                P01-P15 (Processing) ──► final-data/series/
                                         │
                    ┌────────────────────┤
                    │                    │
                    ▼                    ▼
              Shiny CSVs          V01-V08 (Validation) ──► VALIDATION_REPORT.json
              Figures                    │
              Report                     ▼
              Ledger              M01-M## (Manual Adj) ──► adjusted-final-data/
```

## Running

```bash
python replicate.py                   # full pipeline (L + P + V)
python replicate.py --load-only       # loading phase only
python replicate.py --process-only    # processing phase only
python replicate.py --validate-only   # validation phase only (requires prior P run)
python replicate.py --manual-only     # manual adjustment phase only
python replicate.py --skip-validation # run L + P, skip V
python replicate.py --skip-manual     # run L + P + V, skip M (default)
python replicate.py --full            # all four phases: L + P + V + M
python replicate.py --series T506 T511  # specific series
python replicate.py --chapter 5       # all series for a chapter
python replicate.py --dry-run         # show plan, don't execute
python replicate.py --report          # generate report only
python replicate.py --ledger          # regenerate ANU_LEDGER.json
```

## Environment Requirements

- **Python**: 3.10+
- **Packages** (see `requirements.txt`):
  - `pandas >= 2.0`
  - `openpyxl >= 3.1`
  - `requests >= 2.28`
  - `python-dotenv >= 1.0`
  - `numpy` (used by IO/labor-value scripts; pulled in by pandas)
- **Optional**: API keys in `config/api_keys.env` for BEA/BLS data fetching

## Script Inventory

### Loading Scripts (`scripts/loading/`)

| Script | Series | Purpose |
|--------|--------|---------|
| L00 | — | Orchestrator: discovers and runs L01-L14 in order |
| L01 | T501-T503, T508-T509 | Revenue accounts |
| L02 | T504, T505 | Variable capital and surplus value |
| L03 | T506, T511, T512 | Key ratios (book + extended) |
| L04 | T515, T516 | Employment |
| L05 | T507, T510 | Composition ratios |
| L06 | T513, T514 | Profit rates |
| L07 | T601-T604 | Tax accounts |
| L08 | T605, T606 | Benefit accounts |
| L09 | T607-T609 | Net social wage |
| L10 | T901 | Summary indicators |
| L11 | T401, T402 | IO matrices |
| L12 | T701-T703 | Labor value inputs |
| L13 | T801 | Cross-study comparison |
| L14 | T201 | Alternative GFP measures |

### Processing Scripts (`scripts/processing/`)

| Script | Series | Priority | Purpose |
|--------|--------|----------|---------|
| P00 | — | — | Orchestrator (PRIORITY-ordered) |
| P01 | T501-T503, T508-T509 | 1 | Revenue aggregates + extension |
| P02 | T504 | 2 | Variable capital V* extension |
| P03 | T505 | 3 | Surplus value S* = GFP - V* |
| P04 | T506 | 2 | Rate of exploitation |
| P05 | T511, T512 | 1 | Labor shares |
| P06 | T515, T516 | 1 | Employment with BLS extension |
| P07 | T507, T510 | 1 | Composition ratios |
| P08 | T513, T514 | 4 | Profit rates |
| P09 | T601-T604 | 1 | Tax accounts |
| P10 | T605, T606 | 1 | Worker benefits |
| P11 | T607-T609 | 4 | Net social wage |
| P12 | T901 | 5 | Summary assembly |
| P13 | T401, T402 | 10 | IO matrix validation |
| P14 | T701-T703 | 11 | Labor values |
| P15 | T801, T201 | 12 | Cross-study comparison |

### Validation Scripts (`scripts/validation/`)

| Script | Purpose |
|--------|---------|
| V00 | Orchestrator: discovers and runs V01-V08, writes VALIDATION_REPORT.json |
| V01 | Reference value comparison against published book values |
| V02 | Range checks (value bounds by series type) |
| V03 | Continuity checks (YoY jump detection, splice year exclusion) |
| V04 | Completeness checks (NaN/gap detection in core period) |
| V05 | Cross-series consistency (accounting identities) |
| V06 | Splice quality (connection ratio, growth rate continuity) |
| V07 | Extension overlap (correlation in overlap period) |
| V08 | Hash integrity (SHA-256 of all input/output files) |

### Manual Adjustment Scripts (`scripts/manual/`)

| Script | Purpose |
|--------|---------|
| M00 | Orchestrator: reads ADJUSTMENT_MANIFEST.json, runs M01+ scripts |

### Exploration Scripts (`scripts/exploration/`)

| Script | Purpose |
|--------|---------|
| E01 | Wave 3 component tests (L13, L14, P15) |

## Output Locations

| Directory | Contents |
|-----------|----------|
| `data/parsed-raw/` | Intermediate parsed CSVs from loading phase |
| `data/final-data/series/` | Final series CSVs (book + combined columns) |
| `data/final-data/chopped/` | Anu Chopped format CSVs |
| `data/final-data/extenbooks/` | Series-level Excel workbooks |
| `data/final-data/shiny/` | Shiny-app-ready chapter CSVs and catalog |
| `data/final-data/figures/` | Generated figure data |
| `data/final-data/logs/` | PROCESS_LOG.json, VALIDATION_REPORT.json, HASH_MANIFEST.json |
| `data/final-data/reports/` | REPLICATION_REPORT.md |
| `data/adjusted-final-data/` | Manually adjusted series (when M## scripts run) |
| `data/scratch/` | Ephemeral exploration outputs |

## Error Handling

- Each L##, P##, V##, and M## script returns a result dict with `status` ("ok"/"pass"/"warn"/"fail")
- Orchestrators (L00/P00/V00/M00) catch unhandled exceptions per-script and continue
- `replicate.py` wraps each phase in try/except; loading failures do not block processing
- Validation failures do not block manual adjustment or export
- A final summary reports loaded/processed/validated counts
