# Measuring the Wealth of Nations - Replication Package

![CI](https://github.com/andenick/measuring-the-wealth-of-nations/actions/workflows/replicate.yml/badge.svg)

Complete replication and extension of every empirical claim in
Shaikh & Tonak (1994), *Measuring the Wealth of Nations: The Political
Economy of National Accounts*, plus eight follow-up studies. All 64 data
series span 1947-2025 (book-period replication 1948-1989 plus extension where applicable)
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

# 4. Package-integrity check (registry + every shipped data CSV load)
python tests/ci_smoke.py
```

> The `tests/` directory carries the development regression + identity
> suite (95 pass / 2 skip / 2 xfail) as run against the internal build
> tree; `tests/ci_smoke.py` is the self-contained check that validates
> this published bundle on its own.

The orchestrator discovers and runs scripts in canonical phase order:
**S -> L -> P -> V -> M -> A -> O -> E** (Setup -> Load -> Process ->
Validate -> Manual -> Analysis -> Output -> Extend).

See `INSTALL.md` for environment setup details and (optional) API key
configuration for fresh data fetches.

## Repository Layout

```
Publish/
|-- README.md                  # this file
|-- VERSION.txt                # bundle version string (v2.1)
|-- LICENSE                    # MIT (Code) + CC-BY-4.0 (Data)
|-- CITATION.cff               # machine-readable citation
|-- INSTALL.md                 # setup details
|-- requirements.txt           # Python dependencies
|-- pyproject.toml             # project metadata
|-- Makefile                   # convenience targets (replicate, validate, viz)
|-- Dockerfile                 # reproducible build container
|-- build.py                   # build orchestrator + status reporter
|-- series_registry.json       # single source of truth (64 series)
|-- DIVERGENCE_REGISTER.json   # intentional methodology divergences (73 entries)
|-- data/                      # 64 chopped CSVs (one per series, wide format)
|-- extenbooks/                # 64 Excel workbooks (4 sheets per series)
|-- docs/
|   |-- series/                # 149 DPR / EPR markdown docs
|   |-- decisions/             # framework decisions 0007, 0008
|   |-- methodology/           # methodology.md (replicator-facing narrative)
|   `-- precommit/             # pre-commit hook policy
|-- code/                      # L01 loaders, P02 processors, V03 validators, M04, A05, O06
|-- viz/                       # Plotly Dash / Shiny visualization apps
`-- tests/                     # 95 pass / 2 skip / 2 xfail regression + identity suite
```

## What's in This Release

- **64 chopped CSVs** (`data/`) - canonical wide format (Row 1
  metadata, Row 2 column IDs, Row 3+ data).
- **64 extenbooks** (`extenbooks/`) - human-readable Excel workbooks
  with 4 sheets per series (Data / Provenance / Research /
  Construction).
- **149 per-series docs** (`docs/`) - DPRs for every series, EPRs
  where extension applies, decomposition notes for compound series.
- **185 pipeline scripts** (`code/`) - L01/P02/V03/M04/A05/O06 phase
  scripts plus shared `lib/` helpers.
- **Visualization app** (`viz/`) - Dash + Shiny apps for interactive
  exploration.
- **DIVERGENCE_REGISTER.json** - every intentional deviation from
  upstream sources and predecessor methodology (73 entries).

## Data License

Code is released under the **MIT License** (see `LICENSE`). Data
outputs in `data/` and `extenbooks/` are released under **Creative
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

Continuous Integration installs this bundle into a clean Python 3.12
virtual environment on every push to `main` and on every pull request
(see `.github/workflows/replicate.yml`) and runs a package-integrity
check: the dependencies install, `series_registry.json` and the
pipeline state load, and every shipped `data/*.csv` parses and is
non-empty (`tests/ci_smoke.py`). A green build means the published
package installs cleanly and its data layer is intact.

The full V03 validation against book benchmarks and cross-source
identities (95 pass / 2 skip / 2 justified xfail; `anu-doctor` 0/0) is
run in the canonical build tree, where the intermediate build inputs
live — see `DIVERGENCE_REGISTER.json`, `PIPELINE_STATE.json`, and the
per-series `docs/`.

## What this bundle can and cannot reproduce

This package is a **published-outputs + provenance bundle**, not a from-raw
build tree. Concretely:

**You can, offline, with only `pip install -r requirements.txt`:**

- Install cleanly into a fresh Python 3.11+ venv (CI does this on every push).
- `python build.py status` — inspect the 9-stage pipeline state and gate marks.
- `python tests/ci_smoke.py` — verify the registry loads and every shipped
  `data/*.csv` parses and is non-empty. **A green run means the package installs
  cleanly and its published data layer is intact.**
- Read every value's lineage: `series_registry.json` (single source of truth),
  `data/PROVENANCE_DICTIONARY.csv` (per-observation),
  `data/COMPONENT_CHAINS.{csv,json}`, the 149 per-series `docs/series/*_DPR.md`
  / `*_EPR.md`, and `DIVERGENCE_REGISTER.json` (73 intentional divergences).

**You cannot, from this bundle alone, regenerate the numbers from raw sources.**
The intermediate build inputs (`data/final/`, cached agency responses, the
project checker) live in the maintainer build tree and are not shipped.
Therefore:

- `build.py chopped` / `build.py extenbooks` and `make build` **skip all series**
  when `data/final/` is absent — they are maintainer-side regenerators, not
  clean-room builders.
- The full V03 validation against book benchmarks (95 pass / 2 skip / 2 xfail;
  `anu-doctor` 0/0) is run in the maintainer tree, not here.
- Fresh BEA/BLS/FRED fetches require your own free API keys and network access
  (see `INSTALL.md`).

In short: **this bundle lets you audit and trust the published data and its
provenance; it does not let you rebuild the data from scratch.** That is an
intentional scope, and it is what a green CI badge attests to.

## Methodology

See `methodology/methodology.md` for the conceptual narrative.
Per-series details live in `docs/` (one DPR and, where applicable,
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
  6 700 $B). The net-capital column is retained as the headline series.
  **New in v2.1:** a book-faithful gross-capital variant `S517-GROSS-A`
  (with `S513-GROSS-A` / `S514-GROSS-A`) is now shipped for the **book
  period 1948–1989 only** — it reproduces the book's printed gross K\* /
  r\* directly (r\* at MAE 0.0025) and gives the profit-rate family its first
  non-tautological book anchor. Beyond the mid-1990s BEA discontinued the
  current-cost gross stock for private nonresidential fixed assets, so the
  gross variant is `nan` after the book period (not synthetically extended).
  See `DIVERGENCE_REGISTER.json` entries **DIV-008 / DIV-070 / DIV-058** and
  `docs/series/S517_EPR.md` Section 5 for the full divergence record.

## Version

**Current: v2.1** (see `VERSION.txt` and `CHANGELOG.md`). An additive
release on top of v2.0 — every pre-existing published cell is byte-identical;
new content appends as new columns, new series arms, and new sidecars.

**New in v2.1 — book-faithful profit rate, reconstructed exploitation, truth fixes:**

- **Book-faithful gross-capital profit-rate variants** (`S513-GROSS-A`,
  `S514-GROSS-A`, `S517-GROSS-A`, book period 1948–1989): the profit-rate
  family's first *non-tautological* book anchor — the printed book `r*` is
  reproduced at **MAE 0.0025 (42/42 years exact at 2 dp)**. The v2.0 net-capital
  headline series are retained unchanged (see `DIVERGENCE_REGISTER.json` DIV-070,
  DIV-058).
- **Reconstructed time-varying I-O-uplift (kIO) rate-of-exploitation arm**
  (`S506-EXT-MARX-KIO`): the frozen kIO = 1.5714 is replaced by an
  officially-sourced, backward-validated, uncertainty-banded annual series
  (kIO₁₉₉₂ ≈ 1.5696 → 1.731 by 2024; e ≈ 2.43 → 4.46). The frozen arm stays
  published as the conservative lower bound (DIV-071, DIV-028).
- **Uncertainty-band sidecars** under `data/bands/`: `S506_KIO_BAND.csv`,
  `S701_LAMBDA_BAND.csv`, `S702_LAMBDA_BAND.csv`.
- **λ / p\* labor-value series (`S701`, `S702`) publish at 3 significant figures**
  (inside the tightest F3 sensitivity bound) instead of false 15–17-digit precision.
- **Restored per-series author quotes** for 34 published series (loader-visible
  quotes 110 → 348; zero invented or dropped), guarded by a new hard test.
- **Truth fixes**: zero unexplained book cells (S601/S603 1964 → DIV-072/073);
  validator honesty (5 tautological anchors re-anchored to independent sources → 0);
  `XS002` de-hardcoded; the `appendix_F/` filter dir renamed `ch7_productive_filter/`.
- **`DIVERGENCE_REGISTER.json`: 73 entries** (was 69); gates **anu-doctor 0/0**,
  **pytest 95 pass / 2 skip / 2 xfail**, **per-series validators 60 PASS / 4 honest
  registered FAIL**.
- **New public artifact** `ANSWERS.md` — an answers-first brief at the repo root.

**Carried from v2.0** — a comprehensive series-by-series review
(~50 series re-examined) and the D-batch of book-fidelity decisions:

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
- **DIVERGENCE_REGISTER.json: 73 entries** capturing every
  intentional deviation from upstream methodology.
- **95 passed / 2 skipped / 2 justified xfail** test suite (`tests/`)
  plus V03 validators driven off year-keyed `reference_values`;
  `anu-doctor` reports 0 errors / 0 warnings.
- **Reproducibility infrastructure**: `Dockerfile`, `Makefile`,
  `tests/`, CI, and `docs/precommit/` ship with the bundle so a
  clean replicator can `docker build` or `make` the entire pipeline.
