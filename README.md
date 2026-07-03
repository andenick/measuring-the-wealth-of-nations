# Measuring the Wealth of Nations - Replication Package

![CI](https://github.com/andenick/measuring-the-wealth-of-nations/actions/workflows/replicate.yml/badge.svg)

Complete replication and extension of every empirical claim in
Shaikh & Tonak (1994), *Measuring the Wealth of Nations: The Political
Economy of National Accounts*, plus eight follow-up studies. All 64 data
series cover 1925-2025 (book period plus extension where applicable)
and are reproducible from the included loaders, processors, and
validators.

## Mission

Reconstruct, verify, and extend the empirical core of Shaikh & Tonak
(1994) under modern provenance discipline:

- 100% of values trace to a published source, cached API response, or
  documented derivation;
- every series has a Data Provenance Record (DPR) and, where extended
  past the original book window, an Extension Provenance Record (EPR);
- every output passes V03 validators against book benchmarks and
  cross-source identity checks before publication.

## Series Inventory (64 total)

| Prefix | Meaning                                  | Count |
| ------ | ---------------------------------------- | :---: |
| `S`    | Primary book series (Ch. 2, 4, 5, 6, 7, 8, 9) | 35 |
| `XS`   | Extra series — analytical aggregates + external follow-up studies | 29 |

The `XS` prefix supersedes the retired `AS` (analytical) and `ES` (external
follow-up) prefixes; `xs_class` distinguishes the former analytical aggregates
(`appendix`) from the follow-up-study series. Readers who referenced the legacy
`AS####` / `ES####` IDs can map them to current `XS####` IDs via
`MIGRATION/crosswalk.csv` (see `MIGRATION/PREFIX_SCHEME.md`).

Follow-up studies covered (`XS` series):

- Tonak (1984) - labor share, net tax
- Shaikh & Tonak (1987, 2002) - productive labor refinements
- Moos (2017) - accumulation
- Mohun (2005, 2013) - exploitation rate, productive / unproductive labor
- Karabacak & Tonak (2022) - Turkey
- Cronin (2001) - New Zealand

## Quick Start

```bash
# 1. Create a clean virtual environment
python -m venv .venv
source .venv/bin/activate         # Linux / macOS
# .venv\Scripts\activate          # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full replication pipeline (Makefile and Docker variants
#    are also provided; see INSTALL.md)
python build.py status

# 4. Run the test suite (93 passed / 2 skipped / 2 xfail expected)
pytest tests/
```

The orchestrator discovers and runs scripts in canonical phase order:
**S -> L -> P -> V -> M -> A -> O -> E** (Setup -> Load -> Process ->
Validate -> Manual -> Analysis -> Output -> Extend).

See `INSTALL.md` for environment setup details and (optional) API key
configuration for fresh data fetches.

## Repository Layout

```
Publish/
|-- README.md                  # this file
|-- VERSION.txt                # bundle version string (v2.0)
|-- LICENSE                    # MIT (Code) + CC-BY-4.0 (Data)
|-- CITATION.cff               # machine-readable citation
|-- INSTALL.md                 # setup details
|-- requirements.txt           # Python dependencies
|-- pyproject.toml             # project metadata
|-- Makefile                   # convenience targets (replicate, validate, viz)
|-- Dockerfile                 # reproducible build container
|-- build.py                   # build orchestrator + status reporter
|-- series_registry.json       # single source of truth (64 series)
|-- DIVERGENCE_REGISTER.json   # intentional methodology divergences (69 entries)
|-- Data/                      # 64 chopped CSVs (one per series, wide format)
|-- Extenbooks/                # 64 Excel workbooks (4 sheets per series)
|-- Docs/
|   |-- series/                # 149 DPR / EPR markdown docs
|   |-- decisions/             # framework decisions 0007, 0008
|   |-- methodology/           # methodology.md (replicator-facing narrative)
|   `-- precommit/             # pre-commit hook policy
|-- code/                      # L01 loaders, P02 processors, V03 validators, M04, A05, O06
|-- viz/                       # Plotly Dash / Shiny visualization apps
`-- tests/                     # 93 pass / 2 skip / 2 xfail regression + identity suite
```

## What's in This Release

- **64 chopped CSVs** (`Data/`) - canonical wide format (Row 1
  metadata, Row 2 column IDs, Row 3+ data).
- **64 extenbooks** (`Extenbooks/`) - human-readable Excel workbooks
  with 4 sheets per series (Data / Provenance / Research /
  Construction).
- **149 per-series docs** (`Docs/`) - DPRs for every series, EPRs
  where extension applies, decomposition notes for compound series.
- **185 pipeline scripts** (`code/`) - L01/P02/V03/M04/A05/O06 phase
  scripts plus shared `lib/` helpers.
- **Visualization app** (`viz/`) - Dash + Shiny apps for interactive
  exploration.
- **DIVERGENCE_REGISTER.json** - every intentional deviation from
  upstream sources and predecessor methodology (12 entries).

## Data License

Code is released under the **MIT License** (see `LICENSE`). Data
outputs in `Data/` and `Extenbooks/` are released under **Creative
Commons Attribution 4.0 International (CC BY 4.0)** - the data file
itself, not the upstream sources, which retain their own terms (BEA,
BLS, FRED, etc.).

## Citation

If you use this replication package, please cite both this package
and the original book:

> Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of
> Nations: The Political Economy of National Accounts*. Cambridge
> University Press.

A machine-readable citation is available in `CITATION.cff`.

## Reproducibility

Continuous Integration runs the full replicator in a clean Python
3.13 virtual environment on every push to `main` and on every pull
request; see `.github/workflows/replicate.yml`. A green build means:
all V03 validators PASS against book benchmarks and cross-source
identities.

## Methodology

See `methodology/methodology.md` for the conceptual narrative.
Per-series details live in `Docs/` (one DPR and, where applicable,
one EPR per series).

## Known Limitations

- **Chapter 7 labor-value series (S701, S702, S703)** are now
  first-class implementations (`proxy: false` in the registry),
  built from BLS CES sectoral employment, BEA Benchmark I-O matrices,
  and the Appendix F productive-share filter. They replace the v1.0
  matrix-structure proxies. Sector coverage is bounded by the eight
  Shaikh-Tonak productive sectors (Appendix G Table G.2); benchmark
  years without I-O coverage are reported as `nan` rather than
  interpolated. See `DIVERGENCE_REGISTER.json` entry **DIV-011**.
- Some series with `status: book_period_validated` cover only the
  book's original window (typically 1947-1989); extension to the
  present is documented in their EPR when applicable.
- All limitations are documented in per-series DPRs / EPRs and in
  `DIVERGENCE_REGISTER.json`.

## Known Data Quirks

- **S517 (Productive Capital Stock K\*) - net vs. gross.**
  Shaikh & Tonak (1994) Table 5.8 labels K\* as the "gross" private
  nonresidential capital stock, but the published book values match
  BEA Fixed Assets Table 4.1 **Net** Stock exactly at all 5 benchmark
  years (1948 = 292, 1958 = 551, 1967 = 871, 1980 = 3 800, 1989 =
  6 700 $B). The book's terminology is in error; the implementation
  uses net stock. BEA publishes no current-cost gross stock for
  private nonresidential fixed assets, so a gross-stock variant is
  not constructible from BEA sources. See `DIVERGENCE_REGISTER.json`
  entry **DIV-008** and `Docs/S517_EPR.md` Section 5 for the full
  divergence record.

## Version

**Current: v2.0** (see `VERSION.txt` and `CHANGELOG.md`). This is the
definitive release, following a comprehensive series-by-series review
(~50 series re-examined) and the D-batch of book-fidelity decisions.
Highlights of the current package:

- **Comprehensive review corrections** across ~50 series (provenance,
  units, content labels, and reference-value fixes), with the full audit
  trail recorded in `series_registry.json` and `DIVERGENCE_REGISTER.json`.
- **D-batch decisions** encoded: S514 rebuilt on the book's own
  division into `r*`/`u` components; the Chapter-7 `K*` series carry a
  replication-first primary column plus labelled variant columns;
  S515/S516 adopt the seam candidate (d); the net-social-wage extension
  uses the book-faithful **Candidate A** for 1952–1989; and
  XS1501–XS1504 are rebuilt on Mohun (2014) published shares.
- **Series-ID migration (`AS`/`ES` → `XS`)**: the 4 analytical and 25
  follow-up-study series adopt the canonical `XS` prefix (`xs_class`
  sectioning); legacy IDs map via `MIGRATION/crosswalk.csv`.
- **Chapter 7 proxy retired**: S701/S702/S703 are first-class
  labor-value series (`proxy: false`), built from BLS CES, BEA
  Benchmark I-O, and the Appendix F productive-share filter.
- **Provenance deliverables shipped**: per-observation
  `data/PROVENANCE_DICTIONARY.csv` (+ README and `PROVENANCE_COVERAGE.csv`),
  `data/COMPONENT_CHAINS.{csv,json}`, `data/S506_STEP_TABLE.csv`, and the
  master I-O concordance (`data/concordances/`).
- **DIVERGENCE_REGISTER.json: 69 entries** capturing every
  intentional deviation from upstream methodology.
- **93 passed / 2 skipped / 2 justified xfail** test suite (`tests/`)
  plus V03 validators driven off year-keyed `reference_values`;
  `anu-doctor` reports 0 errors / 0 warnings.
- **Reproducibility infrastructure**: `Dockerfile`, `Makefile`,
  `tests/`, CI, and `Docs/precommit/` ship with the bundle so a
  clean replicator can `docker build` or `make` the entire pipeline.
