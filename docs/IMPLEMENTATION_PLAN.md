# Implementation Plan — Full Build to v1.0 Release

**Scope**: every concrete task needed to take this project from the current state (35/62 series PASS, 11 commits, Wave 5 partial close) to the public v1.0 GitHub Release.

**Style**: each task is independently executable. Pick any task whose prerequisites are satisfied and you can complete it without guessing the next step. Each task lists:
- **Prereqs**: which other tasks must be complete first
- **Inputs**: data and files needed
- **Steps**: ordered actions
- **Deliverables**: files produced
- **Acceptance**: a single check that confirms the task is done
- **Effort**: rough wall-clock estimate (one focused session = 90 minutes)

**Tracking**: tasks use a hierarchical ID (`P.S.N` = Phase.Subphase.Task). Track completion with the GitHub Issues list or by checking off in this file.

**Overall task count**: 142 tasks across 10 phases.

---

## How to read this plan

```
[1.A.1]  ← task ID
**Task**: short description
- Prereqs: 1.A.2  ← what must be done first
- Inputs: ...
- Steps:
   1. concrete action
   2. concrete action
- Deliverables: path/to/file
- Acceptance: `python ... --check` returns 0
- Effort: 30m
```

---

## Phase 1 — Pipeline Orchestration & API Infrastructure (foundation)

Goal: build the run.py, API clients, and caching layer that every subsequent phase depends on. Nothing in this phase unlocks a single series by itself, but everything downstream needs it.

### 1.A — `run.py` orchestrator

**[1.A.1]** Read ST2's existing `run.py` end-to-end
- Prereqs: none
- Inputs: `D:/Arcanum/Projects/RMWND/Inputs/ST2/Technical/NickyData/run.py`
- Steps:
  1. Read it fully. Note its `discover_scripts()` pattern, phase ordering (S→L→P→V→M→A→O→E), CLI flags (`--validate-only`, `--from`, `--list`, `--report`)
  2. Note its dependency-aware ordering: how it sorts L## by file naming, how it handles P## that depend on prior L##
  3. List in a comment what behavior we'll keep, what we'll change for the new S/ES/AS prefix scheme
- Deliverables: notes in scratchpad (not committed)
- Acceptance: can describe ST2's orchestrator structure in two paragraphs without re-reading
- Effort: 30m

**[1.A.2]** Design new run.py CLI surface
- Prereqs: 1.A.1
- Inputs: ST2 design notes
- Steps:
  1. Decide the CLI: `python run.py [--validate-only|--test-all|--from <phase>|--series <SID>|--list|--report|--health]`
  2. Document in a comment block at the top of the future `run.py` file
  3. Sketch the phase order: S00_setup → L01_loaders → P02_processors → V03_validators → M04_manual → A05_analysis → O06_output
- Deliverables: CLI surface documented
- Acceptance: design choice documented in `code/run.py` header comment block (placeholder)
- Effort: 20m

**[1.A.3]** Implement `code/run.py` (phase discovery + orchestration)
- Prereqs: 1.A.2
- Inputs: `series_registry.json` (for series-aware modes)
- Steps:
  1. Walk `code/S00_setup`, `code/L01_loaders`, `code/P02_processors`, `code/V03_validators`, `code/M04_manual`, `code/A05_analysis`, `code/O06_output` in order
  2. For each `*.py`, dynamically import it and call its `run()` function
  3. Aggregate return values for `--report`
  4. `--validate-only` runs only V03_*
  5. `--series S###` runs only the scripts for that series (regex-match `{SID}_`)
  6. Print a summary table at the end: per-script status, per-series PASS/FAIL counts
- Deliverables: `code/run.py`
- Acceptance: `python run.py --list` enumerates every script; `python run.py --validate-only` reproduces the current 35 PASS count
- Effort: 90m

**[1.A.4]** Add `--health` mode for cross-cutting checks
- Prereqs: 1.A.3
- Steps:
  1. `--health` runs S01_validate_environment, then `/anu-doctor`-equivalent registry consistency checks
  2. Reports: registry schema valid, all referenced source files exist, no stale T###/N#### references, no synthetic data flags
- Deliverables: extended `run.py`
- Acceptance: `python run.py --health` prints PASS for all current checks
- Effort: 30m

### 1.B — API key infrastructure

**[1.B.1]** Create `data/user-inputs/api_keys.env.template`
- Prereqs: none
- Steps:
  1. Add empty placeholders for `BEA_API_KEY=`, `BLS_API_KEY=`, `FRED_API_KEY=`
  2. Comments above each line linking to the agency's signup page
- Deliverables: `data/user-inputs/api_keys.env.template`
- Acceptance: file present, gitignored copy `api_keys.env` recognized as separate
- Effort: 10m

**[1.B.2]** Update `.gitignore` for the env file
- Prereqs: 1.B.1
- Steps:
  1. Add `data/user-inputs/api_keys.env` and `data/user-inputs/*.env` (but NOT `*.env.template`)
  2. Add `data/raw/` (large API cache — gitignored, regenerable)
- Deliverables: updated `.gitignore`
- Acceptance: `git check-ignore data/user-inputs/api_keys.env` returns the path; `git check-ignore data/user-inputs/api_keys.env.template` does NOT
- Effort: 10m

**[1.B.3]** Write `code/utils/secrets.py` — env-loader helper
- Prereqs: 1.B.1
- Steps:
  1. `load_api_keys() -> dict[str, str]` reads `data/user-inputs/api_keys.env`
  2. Returns dict of `{BEA_API_KEY: ..., BLS_API_KEY: ..., FRED_API_KEY: ...}`
  3. Raises a descriptive error if a key is missing and a required mode (test-all, extension-fetch) is invoked
  4. `--validate-only` mode does NOT require keys (works against cached data)
- Deliverables: `code/utils/secrets.py`
- Acceptance: `from utils.secrets import load_api_keys; load_api_keys()` returns a dict (possibly with empty values) without raising
- Effort: 30m

### 1.C — BEA NIPA client

**[1.C.1]** Write `code/utils/bea.py` — base BEA API client
- Prereqs: 1.B.3
- Steps:
  1. `BEAClient` class with `__init__(api_key: str)` and rate-limit handling (100 req/min cap)
  2. Method `get_nipa(table_name: str, frequency: str = "A", year_range: tuple[int, int] | None = None) -> pd.DataFrame`
  3. Endpoint: `https://apps.bea.gov/api/data/`
  4. Cache responses to `data/raw/bea/{dataset}/{table_name}_{years}.json`
  5. Exponential backoff on 429/503
  6. Returns DataFrame in long format: year, line_number, line_description, value
- Deliverables: `code/utils/bea.py`
- Acceptance: with valid `BEA_API_KEY`, `BEAClient(key).get_nipa("T10105", year_range=(1929, 2024))` returns a non-empty DataFrame and writes the cache file
- Effort: 90m

**[1.C.2]** Add NIPA Table 1.1.5 (GDP components) fetch
- Prereqs: 1.C.1
- Steps:
  1. Write a thin script `code/L01_loaders/L00_fetch_nipa_t10105_gdp.py` that fetches Table 1.1.5 and caches
  2. Run once to populate cache
- Deliverables: `code/L01_loaders/L00_fetch_nipa_t10105_gdp.py`, cache file `data/raw/bea/nipa/T10105_1929_2024.json`
- Acceptance: cache file exists, 96 annual rows for GDP
- Effort: 20m

**[1.C.3]** Add NIPA Table 2.1 (Personal Income) fetch
- Prereqs: 1.C.1
- Same pattern as 1.C.2
- Acceptance: cache file exists for T20100
- Effort: 15m

**[1.C.4]** Add NIPA Table 1.10 (Corporate Profits) fetch
- Prereqs: 1.C.1
- Same pattern
- Acceptance: cache file exists for T11000
- Effort: 15m

**[1.C.5]** Add NIPA Fixed Assets Table 4.1 (Net Stock by Industry) fetch
- Prereqs: 1.C.1
- Note: this is BEA Fixed Assets dataset, not NIPA — adapt the client method
- Add `get_fixed_assets(table_name: str, ...)` method
- Acceptance: cache file exists for Table_4_1_*
- Effort: 30m

**[1.C.6]** Add BEA Benchmark I-O Use/Make tables fetch
- Prereqs: 1.C.1
- Note: separate dataset `InputOutput`. Each benchmark year (1947, 1958, 1963, 1967, 1972, 1977, 1982, 1987, 1992, 1997, 2002, 2007, 2012, 2017) is fetched separately
- Acceptance: 14 benchmark years cached, ~50MB total
- Effort: 90m

### 1.D — BLS CES client

**[1.D.1]** Write `code/utils/bls.py` — base BLS API client
- Prereqs: 1.B.3
- Steps:
  1. `BLSClient` class with public API (`https://api.bls.gov/publicAPI/v2/timeseries/data/`)
  2. Method `get_series(series_id: str, start_year: int, end_year: int)`
  3. Free tier limit: 25 series/day; paid tier 500 — design for free tier
  4. Cache to `data/raw/bls/{series_id}_{years}.json`
- Deliverables: `code/utils/bls.py`
- Acceptance: `BLSClient(key).get_series("CES0000000001", 1948, 2024)` returns DataFrame
- Effort: 60m

**[1.D.2]** Fetch BLS CES production worker series
- Prereqs: 1.D.1
- Steps:
  1. Series ID list: total nonfarm production workers, manufacturing production workers, sectoral breakouts
  2. Identify which BLS series IDs map to S&T's productive-labor categories (per book Appendix E.3 → BLS concordance)
- Deliverables: cache files for ~10 BLS series
- Acceptance: data covers 1948–2024 for primary series
- Effort: 60m

### 1.E — FRED client

**[1.E.1]** Write `code/utils/fred.py` — base FRED API client
- Prereqs: 1.B.3
- Steps:
  1. `FREDClient` with `get_series(series_id: str)` method
  2. Cache to `data/raw/fred/{series_id}.csv`
- Deliverables: `code/utils/fred.py`
- Acceptance: `FREDClient(key).get_series("GDPDEF")` returns DataFrame
- Effort: 45m

**[1.E.2]** Fetch FRED TCU (capacity utilization)
- Prereqs: 1.E.1
- Acceptance: cache file `data/raw/fred/TCU.csv` exists, covers 1967–2024 (TCU starts 1967)
- Effort: 10m

**[1.E.3]** Fetch FRED GDPDEF (GDP deflator)
- Prereqs: 1.E.1
- Acceptance: cache file `data/raw/fred/GDPDEF.csv` exists
- Effort: 10m

### Phase 1 milestone

Commit: `"Phase 1: pipeline orchestrator + BEA/BLS/FRED API clients"`. All API caches populated, `python run.py --health` GREEN.

---

## Phase 2 — K\* (Capital Stock) infrastructure

Goal: source the productive constant capital stock and the SIC↔NAICS concordance. Unblocks S510, S513, S514, S702, AS001.

### 2.A — SIC↔NAICS productive/unproductive concordance

**[2.A.1]** Locate the book's Appendix C concordance
- Prereqs: none
- Inputs: `Inputs/Salvaged/book_text_1994/`
- Steps:
  1. Read pages 200–250 looking for the productive-sector classification table
  2. Extract the SIC 2-digit codes flagged as productive
  3. If not in salvaged extraction, fall back to ST2's `Inputs/Concordances/` or `Mohun/mohun_industry_classification.csv` as a starting reference
- Deliverables: notes (and possibly a new HDARP run targeting these pages)
- Acceptance: produced a list of productive SIC codes that the book endorses
- Effort: 45m

**[2.A.2]** Write `data/source/concordances/sic_to_naics_productive_classification.csv`
- Prereqs: 2.A.1
- Steps:
  1. Columns: `sic_code, sic_description, naics_code, naics_description, productive (1/0), source (book/Mohun/our_judgment), notes`
  2. Populate from 2.A.1 + BEA's official SIC-NAICS bridge tables
  3. Document every borderline judgment in the `notes` column
- Deliverables: `data/source/concordances/sic_to_naics_productive_classification.csv`
- Acceptance: ≥95% of SIC 2-digit codes have a `productive` assignment with `source` populated
- Effort: 90m

**[2.A.3]** Write `code/utils/concordance.py`
- Prereqs: 2.A.2
- Steps:
  1. `load_productive_concordance() -> pd.DataFrame`
  2. `partition_by_productive(df: pd.DataFrame, sector_col: str) -> tuple[pd.DataFrame, pd.DataFrame]` — returns (productive_df, unproductive_df)
  3. `productive_naics() -> list[str]` and `productive_sic() -> list[str]` helper accessors
- Deliverables: `code/utils/concordance.py`
- Acceptance: importable, returns the concordance DataFrame
- Effort: 30m

**[2.A.4]** Write `docs/methodology/productive_classification_NAICS.md`
- Prereqs: 2.A.3
- Steps:
  1. Document the productive/unproductive boundary used in this project
  2. Reference book Appendix C
  3. Note divergences from book (post-1997 NAICS introduces new categories)
  4. Compare against Mohun's classification (narrower boundary — explain why we use Shaikh-Tonak's broader one)
- Deliverables: `docs/methodology/productive_classification_NAICS.md`
- Acceptance: explains every choice an auditor might query
- Effort: 60m

### 2.B — K\* (productive constant capital stock) loader

**[2.B.1]** Write `code/L01_loaders/L01_K_star.py`
- Prereqs: 2.A.3, 1.C.5
- Steps:
  1. Load cached BEA Fixed Assets Table 4.1 from `data/raw/bea/fixed_assets/`
  2. Apply `partition_by_productive` from `concordance.py`
  3. Sum productive sector net stock by year, 1925–2024
  4. Convert to billions of current USD if necessary
  5. Emit subseries `K_STAR-A`
- Deliverables: `code/L01_loaders/L01_K_star.py`
- Acceptance: produces 100 rows (1925–2024); 1948 value within 10% of book Table H.2 if H.2 found, else within 10% of ST2's `K_star_by_industry.csv` total
- Effort: 90m

**[2.B.2]** Register K\* in the registry
- Prereqs: 2.B.1
- Steps:
  1. Add `K_STAR` entry to `series_registry.json` (decide: bare `K_STAR` or prefixed `S517-K_STAR`)
  2. Recommend: prefix as `S517` to keep the S### scheme; mark as `content_type: time_series`, `units: billions_usd`, `status: validated`
  3. Update the prefix_scheme block if needed (no — `S517` fits existing scheme)
- Deliverables: registry entry
- Acceptance: `python -c "import json; print(json.load(open('series_registry.json',encoding='utf-8'))['series']['S517'])"` returns the entry
- Effort: 20m

**[2.B.3]** Write `code/P02_processors/P02_K_star.py` (pass-through)
- Prereqs: 2.B.1
- Standard processor pattern, no transformation
- Acceptance: `data/final/S517.csv` produced with 100 rows
- Effort: 15m

**[2.B.4]** Write `code/V03_validators/V03_K_star.py`
- Prereqs: 2.B.3
- Steps:
  1. Range check: K\* > 0 in every year
  2. Monotonicity: K\* should monotonically increase (with possible small dips in deep recessions)
  3. Benchmark check against book Table H.2 or ST2 K_star total, at 1948 and 1989
- Deliverables: `code/V03_validators/V03_K_star.py`
- Acceptance: V03 PASS
- Effort: 30m

**[2.B.5]** Write `docs/series/S517_DPR.md`
- Prereqs: 2.B.4
- Standard DPR template, documenting the concordance choices
- Effort: 30m

### Phase 2 milestone

Commit: `"Phase 2: K* productive capital stock + SIC-NAICS concordance"`. K\* time series live; concordance documented.

---

## Phase 3 — I-O Matrix Infrastructure

Goal: load BEA Benchmark Use/Make/Z tables, compute A and B matrices per benchmark year. Unblocks S401, S402, S701, S702, S703.

### 3.A — I-O matrix loader

**[3.A.1]** Inspect cached BEA Benchmark I-O file structure
- Prereqs: 1.C.6
- Steps:
  1. Open `data/raw/bea/io/{year}/` for one year (e.g., 1972)
  2. Identify the row × column structure of Use, Make, and Z tables
  3. Note sector count (Detailed ~400, Summary ~71)
  4. Decision point: Detailed or Summary? Document the choice
- Deliverables: notes
- Acceptance: can describe the matrix schema in one paragraph
- Effort: 45m

**[3.A.2]** Write `code/utils/io_matrix.py`
- Prereqs: 3.A.1, 2.A.3
- Steps:
  1. `load_benchmark(year: int) -> dict[str, pd.DataFrame]` returns `{"Use": ..., "Make": ..., "Z": ...}`
  2. `compute_A_matrix(Use, Make) -> pd.DataFrame` — A = Use × Make^-1 × (output diagonal)^-1 (verify exact formula from book Appendix B)
  3. `compute_B_matrix(A) -> pd.DataFrame` — B = (I - A)^-1
  4. `restrict_to_productive(matrix, naics_codes) -> pd.DataFrame`
- Deliverables: `code/utils/io_matrix.py`
- Acceptance: A-matrix for 1972 has max eigenvalue < 1 (Hawkins-Simon condition); leontief_max_dev < 0.001 vs ST2's T401.csv value
- Effort: 180m (3 hours — the most involved single task)

**[3.A.3]** Write tests for `code/utils/io_matrix.py`
- Prereqs: 3.A.2
- Steps:
  1. `code/tests/test_io_matrix.py` (start of a tests/ dir)
  2. Tests: Hawkins-Simon at every benchmark year; A matrix shape matches sector count; B = (I-A)^-1 verified by `B × (I - A) ≈ I`
- Deliverables: tests file
- Acceptance: `pytest code/tests/test_io_matrix.py` GREEN
- Effort: 60m

### 3.B — S401 (A-matrix summary metrics)

**[3.B.1]** Write `code/L01_loaders/L01_S401_a_matrix.py`
- Prereqs: 3.A.2
- Steps:
  1. Loop over benchmark years (1947, 1958, 1963, 1967, 1972, 1977, 1982, 1987, 1992, 1997, 2002, 2007, 2012, 2017)
  2. For each, load Use+Make, compute A, restrict to productive, then compute summary metrics:
     - `n_sectors`, `sparsity`, `max_eigenvalue`, `condition_number`, `leontief_max_dev`, `n_productive`, `n_unproductive`
  3. Emit one row per year
- Deliverables: `code/L01_loaders/L01_S401_a_matrix.py`
- Acceptance: produces a 14-row DataFrame with all summary columns populated
- Effort: 60m

**[3.B.2]** Write `code/P02_processors/P02_S401_a_matrix.py`
- Prereqs: 3.B.1
- Pass-through emit
- Effort: 15m

**[3.B.3]** Write `code/V03_validators/V03_S401_a_matrix.py`
- Prereqs: 3.B.2
- Steps:
  1. Validates all rows have `max_eigenvalue < 1.0`
  2. Cross-check `leontief_max_dev` against ST2's T401.csv values
- Acceptance: V03 PASS
- Effort: 30m

**[3.B.4]** Write `docs/series/S401_DPR.md` (update from pending)
- Prereqs: 3.B.3
- Effort: 30m

### 3.C — S402 (B-matrix summary metrics)

**[3.C.1]** Write `code/L01_loaders/L01_S402_b_matrix.py`
- Prereqs: 3.A.2
- Same shape as S401 but using B = (I-A)^-1; metrics: `max_b_element`, `column_sum_max`, `eigenvalue_structure`
- Effort: 45m

**[3.C.2]** P02, V03, DPR for S402
- Prereqs: 3.C.1
- Standard pattern
- Effort: 60m total

### Phase 3 milestone

Commit: `"Phase 3: I-O matrix loader + S401/S402 (37/62 PASS)"`. (37 = 35 current + S517 + S401 + S402 = 38; if S401/S402 each PASS, milestone is 38/62.)

---

## Phase 4 — Ch5 extension activation (10 EPRs)

Goal: extend the 10 documented-EPR Ch5 series to 2024 by fetching post-1989 data and splicing per each EPR's methodology.

Each task in this phase follows the same shape; I document the first in detail and abbreviate the rest.

### 4.A — S501 Total Product extension

**[4.A.1]** Extend `L01_S501_total_product.py` to fetch BEA GDP-by-Industry
- Prereqs: 1.C.1, 2.A.3
- Steps:
  1. Add a second loader function `load_extension()` that fetches BEA GDP-by-Industry (NAICS, value added by detailed industry) 1997–2024
  2. Apply productive partition from concordance
  3. Sum to annual aggregate in billions USD
  4. Emit subseries `S501-B`
- Deliverables: updated `L01_S501_total_product.py` with both `load()` (book) and `load_extension()` (BEA)
- Acceptance: `data/intermediate/S501.csv` now has both `S501-A` (1948–1989) and `S501-B` (1997–2024) rows
- Effort: 60m

**[4.A.2]** Extend `P02_S501_total_product.py` with splice
- Prereqs: 4.A.1
- Steps:
  1. Load S501-A and S501-B from intermediate
  2. Apply growth-rate splice: rebase S501-B so its 1997 value equals the implied 1997 value of S501-A (using S501-A's 1989 value × cumulative GDP growth 1989→1997 if S501-A doesn't reach 1997, or directly if it does)
  3. For the 1990–1997 SIC-NAICS gap, log-linearly interpolate between S501-A[1989] and S501-B[1997]
  4. Emit `S501-COMBINED` as the final 1948–2024 series
  5. Write provenance for each year: book / interpolated / extension
- Deliverables: updated P02
- Acceptance: S501-COMBINED spans 77 rows (1948–2024); 1989 value matches S501-A within 1e-6; 1997 value matches S501-B within 1e-6 after rebase
- Effort: 90m

**[4.A.3]** Extend `V03_S501_total_product.py` with V06+V07
- Prereqs: 4.A.2
- Steps:
  1. V06 transition quality: connection ratio at splice in [0.95, 1.05]
  2. V07 overlap correlation: if there's any overlap year (likely not, since book ends 1989 and BEA starts 1997 in NAICS), document `not_applicable`
  3. V14 unit consistency: both subsources in billions USD
- Acceptance: V03 PASS with extension checks GREEN
- Effort: 30m

**[4.A.4]** Update `S501_DPR.md` and `S501_EPR.md`
- Prereqs: 4.A.3
- Steps:
  1. DPR: update Status to `validated_book_and_extension`
  2. EPR: mark every activation checkbox `[x]` and record splice quality metrics
- Effort: 30m

### 4.B–4.J — S504, S505, S506, S511, S512, S513, S514, S515, S516 extensions

Same pattern as 4.A. Each ~150 minutes total (60m loader + 90m splice). Order:

- **4.B**: S504 (V*) — extension via S511 × S512 × total wage bill (BEA NIPA 2.1)
- **4.C**: S505 (S*) — extension via VA* - V* (S503 - S504)
- **4.D**: S506 (e) — extension via e = 1.238/(V*/W) - 1 (the book's `VA*/W ≈ const` assumption)
- **4.E**: S511 (Lp/L) — extension via BLS CES productive worker share (sectoral)
- **4.F**: S512 (V*/W) — extension via S504 / EC
- **4.G**: S513 (r*) — gated on Phase 2 (K\*); extends via S505 / (K\* + S504)
- **4.H**: S514 (r*_adj) — gated on Phase 2 (TCU); extends via S513 × TCU/100
- **4.I**: S515 (Lp) — extension via BLS CES sectoral employment under productive partition
- **4.J**: S516 (Lu) — derived = total CES employment - S515 extension

Each task `4.{B–J}.{1,2,3,4}` corresponds to loader / processor / validator / DPR+EPR update.

**Effort per series**: 150–180m × 9 series = ~25 hours, ~3 sessions.

### Phase 4 milestone

Commit: `"Phase 4: Ch5 extensions complete — 10 series spanning 1948–2024"`. The flagship deliverable. After this phase 38/62 → 38/62 (extensions don't add new series, but they elevate 10 from book-only to full-period).

---

## Phase 5 — Ch6 + Ch2/4/7/8 + Wave 4 follow-ups

Goal: complete the remaining S### and ES### series.

### 5.A — S607 extension splice (single task)

**[5.A.1]** Activate S607 NSW extension
- Prereqs: none (data already on disk)
- Steps:
  1. Copy `Inputs/ST2/Inputs/ST_Chopped/ch06/Table6_3_Extended.csv` (already done)
  2. Add `load_extension()` to `L01_S607_net_social_wage.py` reading the Extended table for 1990–2024
  3. Extend P02 to emit S607-COMBINED (S607-A 1952–1989 + S607-B 1990–2024)
  4. Extend V03 with V06 overlap check at 1989
  5. Update DPR and EPR
- Deliverables: updated L01/P02/V03
- Acceptance: S607-COMBINED spans 73 rows (1952–2024); 1989 overlap value matches in both subsources within 1e-6; documents NSW turning POSITIVE in early 1990s
- Effort: 90m

### 5.B — Quick wins: Mohun 2013 (ES1501-1504)

**[5.B.1]** Copy Mohun 2013 source CSV
- Prereqs: none
- Steps:
  1. Inspect `Inputs/ST2/Inputs/ExternalSources/Mohun/mohun_unproductive_decomposition_1948_1989.csv`
  2. Copy to `data/source/external_studies/Mohun_unproductive_decomposition_1948_1989.csv`
- Acceptance: file in tree
- Effort: 15m

**[5.B.2–5.B.5]** Implement ES1501, ES1502, ES1503, ES1504 (4 tasks)
- Pattern: BookColumnLoader for the first three; ES1504 derived as ES1503 / ES1402's Lp count (need Mohun's Lp_total)
- Effort: 60m total

### 5.C — ST 1987 ratios (ES1101-1103)

**[5.C.1]** Register S617 (Employee Compensation, EC) as a series
- Prereqs: none
- Steps:
  1. Add S617 to registry — load from Table H.1 column `EC`
  2. Write L01/P02/V03 trio
- Effort: 60m

**[5.C.2–5.C.4]** Implement ES1101, ES1102, ES1103 as derived ratios
- Prereqs: 5.C.1
- Steps:
  1. ES1101 = (S605 + S606 - S604) / S617 (Net Transfer Rate)
  2. ES1102 = (S605 + S606) / S617 (Social Benefit Rate)
  3. ES1103 = S604 / S617 (Social Tax Rate)
  4. P02 derived processors, V03 round-trip checks
- Effort: 90m total

### 5.D — ST 2002 (ES1201, ES1202)

**[5.D.1]** Implement ES1201 = S607 / GDP
- Prereqs: 1.C.2 (NIPA 1.1.5 cached)
- L01 loads GDP from BEA cache; P02 computes ratio; V03 endpoint check
- Effort: 60m

**[5.D.2]** Implement ES1202 = S607 / S617 (NSW/EC)
- Prereqs: 5.C.1
- Effort: 30m

### 5.E — Moos 2017 (ES1301, ES1302, ES1304, ES1305)

**[5.E.1]** Copy Moos `nsw_reconciled` CSV
- Prereqs: none
- Already evaluated; copy to `data/source/external_studies/Moos_nsw_reconciled.csv`
- Effort: 10m

**[5.E.2]** ES1301 = Moos nsw1 / GDP
- Prereqs: 1.C.2, 5.E.1
- Effort: 45m

**[5.E.3]** ES1302 = Moos nsw1 / compensation
- Prereqs: 5.E.1, 5.C.1
- Effort: 30m

**[5.E.4]** ES1304 = ES1301 - ES1201 (Moos vs ST delta over 1959–1997 overlap)
- Prereqs: 5.D.1, 5.E.2
- Effort: 30m

**[5.E.5]** ES1305 = structural shift indicator
- Prereqs: 5.E.2
- Approach: piecewise linear regression on ES1301; report pre/post-2000 slope difference
- Effort: 60m

### 5.F — Karabacak Turkey 2022 (ES1601, ES1602)

**[5.F.1]** Read Karabacak & Tonak (2022) paper PDF
- Prereqs: none
- Inputs: `Inputs/ST2/Inputs/ExternalSources/Turkey2022/` references the paper; find or fetch the actual PDF
- Steps:
  1. Identify the exact formula for Turkey labor share + NSW
  2. Map paper variables to available data: World Bank, OECD, FRED Turkey data
- Effort: 60m

**[5.F.2]** ES1601 Turkey Labor Share
- Prereqs: 5.F.1
- Likely: WB structural data → compensation / GDP ratio
- Effort: 60m

**[5.F.3]** ES1602 Turkey NSW/GDP
- Prereqs: 5.F.1
- Likely: OECD taxes + WB government consumption - WB compensation transfers
- Effort: 90m

### 5.G — S201 (Alternative GFP)

**[5.G.1]** Implement S201 from BEA NIPA 1.1.5
- Prereqs: 1.C.2
- Compute GFP_GDP_ratio and FP_NDP_ratio using S503 (already built)
- Effort: 60m

### 5.H — Ch7 (S701-S703, gated on Phase 3)

**[5.H.1]** S701 Labor Values
- Prereqs: 3.A.2 + 1.D.2
- Compute λ = l × B per benchmark year
- Effort: 90m

**[5.H.2]** S702 Prices of Production
- Prereqs: 5.H.1, Phase 4 S513 extended
- Solve p = (a₀(1+r) + Ap)
- Effort: 90m

**[5.H.3]** S703 Value-Price Deviations
- Prereqs: 5.H.1, 5.H.2
- Compute (p - λ) / λ × 100
- Effort: 30m

### 5.I — S801 Cross-Study Comparison

**[5.I.1]** Implement S801
- Prereqs: Wave 4 Mohun complete (already done at 35/62 close)
- Merge S506, S511, ES1401, ES1402 into one wide CSV
- Effort: 60m

### Phase 5 milestone

Commit: `"Phase 5: Remaining series — 62/62 PASS"`. Every registry entry validated.

---

## Phase 6 — AS001 + AS004 (analytical)

### 6.A — AS001 Social Burden Rate

**[6.A.1]** Implement AS001
- Prereqs: 1.C.4 (NIPA 1.10 cached), Phase 2 K\* complete
- Steps:
  1. b = 1 - Pn/S505 (where Pn = NIPA corporate profits productive-restricted)
  2. Validate against book Table 7.1 endpoints (0.56 → 0.66)
- Effort: 90m

### 6.B — AS004 Marxian Productivity

**[6.B.1]** Implement AS004
- Prereqs: 1.D.2 (BLS hours), 1.E.3 (GDPDEF), Phase 4 S501/S503 extensions
- Steps:
  1. q* = (S501-COMBINED / GDPDEF) / Hp
  2. y* = (S503-COMBINED / GDPDEF) / Hp
  3. y  = (GDP / GDPDEF) / total_hours
  4. Where Hp = BLS productive worker count × hours per worker
- Effort: 120m

### Phase 6 milestone

Commit: `"Phase 6: AS001 + AS004 (complete analytical layer)"`.

---

## Phase 7 — Visualization (`/anu-visualize`)

### 7.A — Framework choice and scaffold

**[7.A.1]** Confirm framework: Dash (recommend) vs R Shiny
- Decide; document in `viz/README.md`
- Effort: 15m

**[7.A.2]** Invoke `/anu-visualize init`
- Prereqs: 7.A.1
- Produces scaffold under `viz/`
- Effort: 30m

### 7.B — Per-tab implementation

**[7.B.1]** Ch5 Exploitation Accounting tab
- Wire S501–S516 chopped CSVs as data sources
- Effort: 90m

**[7.B.2]** Ch6 NSW tab
- Wire S601–S609 (including S607-COMBINED extension)
- Effort: 60m

**[7.B.3]** Ch2/4/7/8/9 Special Topics tab
- Wire S201, S401, S402, S701, S702, S703, S801, S901
- Effort: 90m

**[7.B.4]** External Studies tab (4 sub-tabs: ST/Mohun, Moos, Karabacak Turkey, Cronin NZ)
- Wire all 25 ES series
- Effort: 120m

**[7.B.5]** Analytical Derivations tab
- Wire AS001–AS004
- Effort: 45m

### 7.C — Methodology panel + Validation widget

**[7.C.1]** Per-series click-through methodology panel
- Renders DPR markdown + research JSON entries + construction Mermaid
- Effort: 90m

**[7.C.2]** Validation Health widget
- Reads `VALIDATION_REPORT.json` and renders per-chapter PASS/FAIL summary
- Effort: 60m

### 7.D — Deploy

**[7.D.1]** Test locally
- `python viz/app.py` on localhost:8050
- Effort: 30m

**[7.D.2]** Deployment plan (Heroku/Render/PythonAnywhere)
- Decide free-tier host; document in README
- Effort: 60m

### Phase 7 milestone

Commit: `"Phase 7: anu-visualize Dash app — all 62 series live"`. D10 ≥80.

---

## Phase 8 — Publication

### 8.A — Public-facing top-level docs

**[8.A.1]** Write `README.md` (public-facing)
- Audience: developers cloning the repo
- Sections: overview, quick start, data sources, methodology link, citation, license
- Effort: 60m

**[8.A.2]** Write `INSTALL.md`
- Requirements, dependency install, API key setup, troubleshooting
- Effort: 45m

**[8.A.3]** Write `CITATION.cff`
- Machine-readable citation: this replication package + Shaikh & Tonak (1994) original
- Effort: 30m

**[8.A.4]** Choose and add `LICENSE`
- Recommend MIT
- Effort: 10m

**[8.A.5]** Write `codemeta.json`
- Software metadata for catalog services
- Effort: 30m

### 8.B — Methodology PDF

**[8.B.1]** Scaffold LaTeX in `docs/methodology/`
- `methodology.tex` master file with section includes for each chapter
- Effort: 30m

**[8.B.2]** Write methodology section per chapter
- Each: introduction, data sources, formulas, validation summary
- 6 sections × 45m = 270m
- Effort: 270m

**[8.B.3]** Methodology section on external studies
- One section covering all 8 study groups
- Effort: 90m

**[8.B.4]** Methodology section on divergences from ST2
- Reference `MIGRATION/divergences_from_ST2.md`
- Effort: 30m

**[8.B.5]** Build PDF
- `latexmk -pdf docs/methodology/methodology.tex`
- Output: `Outputs/Reports/methodology.pdf`
- Effort: 30m (debugging build)

### 8.C — `/anu-publish` audit

**[8.C.1]** Run `/anu-publish audit`
- Produces `Outputs/Publish/`
- Effort: 30m

**[8.C.2]** Scrub verification
- `grep -r "D:/Arcanum\|Council\|Druck\|Robin\|Robert" Outputs/Publish/` returns zero
- Fix any leaks
- Effort: 60m

**[8.C.3]** Address D14 findings
- Re-run `/anu-review`; D14 must score ≥90 for publication
- Effort: 60m

### 8.D — `/anu-drive` generate

**[8.D.1]** Run `/anu-drive generate`
- Produces `Outputs/Drive/` consumer bundle
- Effort: 30m

**[8.D.2]** Drive bundle smoke test
- Open master xlsx, verify all 62 series present with units + sources
- Effort: 30m

### 8.E — `/anu-archive` generate

**[8.E.1]** Run `/anu-archive generate`
- Produces `Outputs/Archive/measuring-wealth-of-nations-archive-v1.0.zip`
- Effort: 30m

**[8.E.2]** Verify archive integrity
- Extract; SHA-256 manifest validates
- Effort: 30m

### 8.F — GitHub Release

**[8.F.1]** Create public GitHub repo
- `github.com/andenick/measuring-wealth-of-nations-replication`
- Topics: economics, marxian, replication, data, shaikh-tonak
- Effort: 15m

**[8.F.2]** Push `Outputs/Publish/` to remote
- Effort: 30m

**[8.F.3]** Create v1.0 Release
- Attach `measuring-wealth-of-nations-archive-v1.0.zip`
- Write release notes pulling from each Wave's review report
- Effort: 60m

**[8.F.4]** Fresh-clone smoke test
- Clone to a temp dir, `pip install -r requirements.txt`, `python run.py --validate-only`
- Must complete in <5s, 62/62 PASS
- Effort: 30m

### 8.G — Drive sharing

**[8.G.1]** Upload `Outputs/Drive/` to Google Drive
- Effort: 30m

**[8.G.2]** Set folder permissions to "Anyone with link can view"
- Effort: 5m

**[8.G.3]** Add Drive link to GitHub README
- Effort: 15m

### Phase 8 milestone

**v1.0 Release published.** Project at distribution-ready state.

---

## Phase 9 — Skill updates & QA

### 9.A — Anu skill updates

**[9.A.1]** `anu-ingestion`: formalize `prefix_scheme` in registry schema
- Edit `D:/Arcanum/Council/Druck/.claude/skills/anu-ingestion/SKILL.md`
- Document multi-prefix registries with the S/ES/AS example
- Effort: 60m

**[9.A.2]** `anu-publish`: codify scrub rules as `audit.py` lint
- Effort: 90m

**[9.A.3]** `anu-replicator`: regex update for S/ES/AS prefixes
- Effort: 30m

**[9.A.4]** `anu-extension`: formalize `extension: null` semantics
- Effort: 30m

**[9.A.5]** `anu-docs`: pre-publication tier-check
- Effort: 45m

**[9.A.6]** `anu-archive`: strip Zenodo metadata template
- Per saved feedback (GitHub Releases only)
- Effort: 30m

**[9.A.7]** `anu-review`: ensure 14-dim audit handles mixed prefixes
- Effort: 30m

**[9.A.8]** Re-run `/anu-doctor` after each update
- Effort: 5m × 7 = 35m

### 9.B — KB enrichment

**[9.B.1]** Re-run `/sphdarp` on Ch5 narrative pages
- Targets pages 100-160 to lift L1 from 12.5% to ~95%
- Effort: 60–90m depending on chunk count

**[9.B.2]** Re-run on Ch6, Ch7, Ch9 (if needed)
- Effort: 60m each

**[9.B.3]** Update research JSONs with new quotes
- `/anu-research mine-chapter 5` re-run after KB enrichment
- Effort: 60m

### 9.C — CI

**[9.C.1]** Write `.github/workflows/validate.yml`
- On every push: clone, install, run `python run.py --validate-only`, fail on any series PASS→FAIL regression
- Effort: 45m

**[9.C.2]** Write `.github/workflows/build-pdf.yml`
- Build methodology PDF on tag pushes
- Effort: 45m

### Phase 9 milestone

Commit: `"Phase 9: skill updates + CI + KB enrichment"`. `/anu-doctor` clean.

---

## Phase 10 — Post-publication

### 10.A — Tonak outreach

**[10.A.1]** Adapt `Salvaged/FromTonak/Email_to_Tonak_Draft.md` for v1.0 release
- Update with GitHub URL, Drive URL, headline findings
- Effort: 30m

**[10.A.2]** Send (at user's discretion)
- N/A — user-gated

### 10.B — Maintenance

**[10.B.1]** Quarterly data refresh
- Schedule: re-fetch BEA NIPA + BLS CES + FRED at end of each quarter
- BEA NIPA Q4 release in January; trigger v1.1 refresh
- Effort: 60m per refresh

**[10.B.2]** Issue triage
- Respond to GitHub Issues filed by users
- Effort: ongoing

---

## Effort summary

| Phase | Tasks | Effort | Series gain |
|---|---|---|---|
| 1 — Pipeline + APIs | 16 | ~8 hours | infrastructure |
| 2 — K\* + concordance | 8 | ~5 hours | +1 (S517) |
| 3 — I-O matrices | 9 | ~7 hours | +2 (S401, S402) |
| 4 — Ch5 extensions | 36 | ~25 hours | (no count; existing series extended) |
| 5 — Remaining series | 24 | ~14 hours | +19 |
| 6 — AS001 + AS004 | 2 | ~3.5 hours | +2 |
| 7 — Visualization | 11 | ~12 hours | viz tier |
| 8 — Publication | 18 | ~10 hours | external |
| 9 — Skill + CI | 12 | ~7 hours | quality |
| 10 — Post-pub | 2+ | ongoing | maintenance |
| **TOTAL** | **142** | **~92 hours** | **35 → 62 series + extensions + viz + release** |

At 90-minute focused sessions (one task = roughly one session for the bigger ones, three tasks for the smaller), **142 tasks ≈ 50–70 sessions** to v1.0.

At a more compressed cadence (3–5 tasks per session, which has been the norm in the build so far), **~30–40 sessions** to v1.0.

---

## Task dependencies — critical path

Tasks that gate the largest downstream blocks:

1. **1.A.3** (run.py) — blocks all subsequent phases that rely on `--validate-only` smoke tests
2. **1.C.1** (BEA client) — blocks Phases 2, 4, 5.D, 5.E, 5.G, 6.A
3. **2.A.2** (concordance CSV) — blocks Phase 2's K\* loader and Phase 3's productive-restricted I-O matrices
4. **2.B.1** (K\* loader) — blocks S510, S513, S514, S702, AS001 (5 series)
5. **3.A.2** (IO matrix utils) — blocks S401, S402, S701, S702, S703 (5 series)
6. **4.G** (S513 extension via K\*) — blocks AS001 full and S702 extension
7. **8.C.1** (anu-publish audit) — blocks the GitHub Release

A reasonable parallel-track plan: while one stream works through Phase 1 → 2 → 3 → 4 in order, a second stream can independently work Phase 5.A (S607), 5.B (Mohun 2013), 5.C (ST 1987), 5.G (S201 needs 1.C.2 only), Phase 7 scaffold, Phase 8.B (methodology PDF can be written in parallel as series complete).

---

## Quality gates per phase

Before merging the closing commit of each phase, verify:

- **Phase 1**: `python run.py --health` GREEN; all 4 API caches populated
- **Phase 2**: K\* validated; concordance documented; ≥95% SIC 2-digit codes classified
- **Phase 3**: I-O Hawkins-Simon condition holds at every benchmark year; S401/S402 PASS
- **Phase 4**: All 10 extended Ch5 series have V06 connection_ratio in [0.95, 1.05]
- **Phase 5**: 62/62 PASS in `--validate-only`
- **Phase 6**: AS001 within ±5% of book Table 7.1; AS004 q*/y growth ratio in [2.0, 3.5]
- **Phase 7**: `/anu-review` D10 ≥80
- **Phase 8**: D14 ≥90; zero scrub leakage; fresh-clone smoke <5s
- **Phase 9**: `/anu-doctor` clean; CI GREEN on at least one PR

---

## Anti-shortcut commitments

Per the user's "no shortcuts, methodically step by step" mandate, this plan deliberately:

1. **Never batches series under a single task** when each could be its own L01/P02/V03 trio. Phase 5 lists each series separately.
2. **Never assumes ST2's intermediate outputs as ground truth** — every benchmark check is against either the book directly or the source CSV row values. ST2 outputs are reference-only.
3. **Always documents every data-source choice** in a DPR; pending series get DPR stubs with activation checklists.
4. **Never skips validation**. Every series gets V03; every infrastructure piece gets unit tests.
5. **Never fabricates data**. Pending series have explicit NaN with `provenance: pending_X`; status fields make the absence visible.
6. **Always pairs documentation with code**. Every L01 has a DPR; every extension has an EPR; every chapter has an adequacy report and a review report.
7. **Always commits in coherent units**. One phase = one (sometimes multiple) commits; commit messages list every series gained.
8. **Always re-runs the ledger and validation report** after work, so coverage numbers reflect actual state.

---

*Implementation plan paired with `ROADMAP.md` (high-level sprint view). This file is the granular execution guide; ROADMAP is the strategic map. Keep both in sync — update task statuses here, refresh sprint summaries there.*

*Last updated: 2026-05-14, immediately after Wave 5 partial close (35/62 PASS, commit `35c8f62`).*
