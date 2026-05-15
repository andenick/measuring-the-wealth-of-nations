# RMWND Roadmap — All Next Steps

**Status as of 2026-05-14**: 35 of 62 series PASS validation. 10 commits on `main`. Build is audit-clean: zero synthetic data, every value traces to a source CSV, all implemented series validated against book benchmarks. The remaining 27 series are blocked on five concrete infrastructure pieces, each unlocks a documented set of series.

This roadmap organizes the remaining work into **8 sprints** ordered by dependency and leverage. Each sprint has a defined goal, a list of series it unblocks, the concrete steps to execute, and acceptance criteria. Effort estimates assume the same series-by-series cadence proven across Waves 1, 2, 4, and 5 (15–30 min per implemented series; 1–3 hours for infrastructure pieces).

---

## Snapshot

```
Implemented & validated   35/62   56.5%   PASS
Pending (data-blocked)    23/62   37.1%   DPR stub w/ activation criteria
Pending (Wave 4 follow)    8/62    12.9%   (~half overlap w/ data-blocked)
DPR coverage              59/62   95.2%
```

**Implemented**: S501-S507, S508, S509, S511, S512, S515, S516, S601-S609, S901, ES1001, ES1002, ES1401-ES1404, ES1701-ES1704, AS002, AS003.

**Pending — Wave 1**: S510, S513, S514 (need K*); 10 EPRs documented but not executed (need API keys + L01 extension for extension subseries).

**Pending — Wave 2**: S607 extension splice (data already on disk; EPR has the activation checklist).

**Pending — Wave 3**: S201 (NIPA), S401, S402 (IO), S701, S702, S703 (IO + employment + K*), S801 (Mohun, Wave 4).

**Pending — Wave 4**: ES1101-1103 (ST '87), ES1201-1202 (ST '02), ES1301-1305 (Moos '17), ES1501-1504 (Mohun '13), ES1601-1602 (Karabacak Turkey '22).

**Pending — Wave 5**: AS001 (Social Burden), AS004 (Marxian Productivity).

---

## Dependency Graph

```
                ┌─────────────────────────────────────────────────────────┐
                │                  Infrastructure pieces                  │
                │                                                         │
                │  [A] BEA NIPA loader   ──unlocks──>  S201, ES1201,      │
                │                                       ES1202, ES1301-5, │
                │                                       AS001 (Pn), AS004 │
                │                                       (GDPDEF)          │
                │                                                         │
                │  [B] K* concordance    ──unlocks──>  S510, S513, S514,  │
                │      (BEA Fixed Assets)               S702, AS001       │
                │                                                         │
                │  [C] BLS CES hours     ──unlocks──>  AS004              │
                │                                                         │
                │  [D] FRED TCU + GDPDEF ──unlocks──>  S514, AS004        │
                │                                                         │
                │  [E] IO matrix loader  ──unlocks──>  S401, S402, S701,  │
                │      (BEA Use/Make/Z)                 S702, S703        │
                │                                                         │
                └─────────────────────────────────────────────────────────┘

                ┌─────────────────────────────────────────────────────────┐
                │                Quick-win compositions                   │
                │                                                         │
                │  S605, S606, S604 + EC  ─>  ES1101, ES1102, ES1103      │
                │  Mohun decomposition CSVs (in tree)  ─>  ES1501-1504    │
                │  S607 extension data (in tree)       ─>  S607-COMBINED  │
                │  Wave 4 Mohun complete    ─>  S801                      │
                │                                                         │
                └─────────────────────────────────────────────────────────┘

                ┌─────────────────────────────────────────────────────────┐
                │                  Distribution (Wave 6)                  │
                │                                                         │
                │  All implementation done  ─>  /anu-publish  ─>  GitHub  │
                │                            ─>  /anu-drive   ─>  Drive   │
                │                            ─>  /anu-archive ─>  Release │
                │  Methodology PDF                                        │
                │  Top-level README                                       │
                │  /anu-visualize (Dash or Shiny)                         │
                │                                                         │
                └─────────────────────────────────────────────────────────┘
```

---

## Sprint 1 — Quick Wins (data already on disk)

**Goal**: Activate the series that need no new data, only composition or simple loading. These should be the next session because they have the highest leverage-per-hour.

**Series unlocked**: ES1101, ES1102, ES1103 (ST 1987 derivations), ES1501-1504 (Mohun 2013), S607 extension splice. **Total: 8 series** (33→43 implemented; 69% coverage).

**Effort**: 1 focused session (~2-3 hours).

### Step-by-step

1. **S607 extension splice** (data on disk):
   - Copy `Inputs/ST2/Inputs/ST_Chopped/ch06/Table6_3_Extended.csv` → already done as `data/source/book_tables/Table6_3_Extended.csv`
   - Update `L01_S607_net_social_wage.py`: add a second loader for `Table6_3_Extended.csv` column `nsw`, period 1990–2024, emit as `S607-B`
   - Update `P02_S607_net_social_wage.py`: compute `S607-COMBINED` = `S607-A` (1952–1989) concatenated with `S607-B` (1990–2024). No rebasing needed — the extension was constructed by the same NIPA methodology so 1989 values match.
   - Update `V03_S607_net_social_wage.py`: add an overlap check at 1989; abs error < 0.01.
   - Run pipeline; expect new `S607-COMBINED` to span 1952-2024 with NSW turning POSITIVE in early 1990s.
   - Update DPR + EPR to record the activation date and the headline regime-change finding (NSW negative → positive).

2. **Mohun 2013 decomposition (ES1501-1504)** — data already in `Inputs/ST2/Inputs/ExternalSources/Mohun/`:
   - Copy the Mohun decomposition CSVs:
     - `mohun_unproductive_decomposition_1948_1989.csv` → `data/source/external_studies/`
     - `mohun_unproductive_decomposition_by_industry.csv` (auxiliary)
   - Inspect column names (probably `working_class_unproductive`, `managerial_unproductive`, `total_unproductive`).
   - Write 4 L01/P02/V03 trios via the same template as Wave 4 (BookColumnLoader pattern).
   - For ES1504 (`Lu/Lp` burden ratio), derive from ES1503 / `Lp_total` column.
   - Validate against book Mohun (2013) endpoints (look up in his paper or trust the source CSV's documented values).

3. **ST 1987 derivations (ES1101-1103)**:
   - These are ratios over employee compensation (EC). EC is in `data/source/book_tables/book_tableH1_1948_1989.csv` (column `EC`). The numerators are S604, S605, S606 from Ch6.
   - **First**, write `code/P02_processors/P02_EC_employee_compensation.py` as a small helper (no L01 needed — just project the `EC` column from H.1 and write to `data/final/EC.csv`). Actually, register EC as a proper series in the registry — let's call it `S516B-EC` or add it as a dedicated subseries. **Decision**: add EC as a derived series `S617-EC` with a DPR.
   - Then compute ES1101 = (S605 + S606 - S604) / S617-EC; ES1102 = (S605 + S606) / S617-EC; ES1103 = S604 / S617-EC.
   - Validate against ST 1987 paper's published values (or against the legacy Phase 1 NSW canonical CSV's intermediate columns if those are available).

### Acceptance criteria for Sprint 1

- [ ] `python run.py --validate-only` (we don't have a `run.py` yet — see Sprint 2's first task) reports 43/62 PASS
- [ ] `data/final/S607.csv` has 73 rows (1952–2024), 1989 overlap value identical between `S607-A` and `S607-B`
- [ ] `data/final/ES15{01,02,03,04}.csv` exist and PASS
- [ ] `data/final/ES11{01,02,03}.csv` exist and PASS
- [ ] DPRs updated for the 8 newly-activated series
- [ ] Single commit: `"Sprint 1: quick wins — S607 extension, Mohun 2013, ST 1987 derivations (43/62 PASS)"`

---

## Sprint 2 — Build BEA NIPA loader and unlock ~12 series

**Goal**: Implement a reusable BEA NIPA loader (the single highest-leverage infrastructure piece) and use it to activate S201, ES1201, ES1202, ES1301-1305, AS001 (partial), AS004 (partial).

**Effort**: 1–2 sessions. The loader itself is ~half a day; series activation is fast once it works.

### Step-by-step

1. **First task**: write `code/run.py` — the top-level pipeline orchestrator. It should:
   - Run S01–S05 setup
   - Discover all L01_*.py / P02_*.py / V03_*.py files and run them in series-ID order
   - Support `--validate-only`, `--from <stage>`, `--series <SID>`, `--list`
   - Adapted from ST2's `Technical/NickyData/run.py` but cleaner and aware of the S/ES/AS prefix scheme.
   - Acceptance: `python run.py --validate-only` runs the full validator pipeline and reports the aggregate PASS/FAIL counts.

2. **Provision API keys**:
   - Create `data/user-inputs/api_keys.env.template` with empty fields for `BEA_API_KEY`, `BLS_API_KEY`, `FRED_API_KEY`.
   - Document in `INSTALL.md` (we'll write `INSTALL.md` here too if not present): user copies the template to `api_keys.env` and fills in keys obtained from `apps.bea.gov/API/signup/` etc.
   - Add `data/user-inputs/api_keys.env` to `.gitignore`.

3. **Write `code/utils/nipa.py`**:
   - Function `fetch_nipa_table(table_id: str, year_range: tuple) -> pd.DataFrame`
   - Uses the BEA API: `https://apps.bea.gov/api/data/?UserID={key}&method=GetData&datasetname=NIPA&TableName={table_id}&Frequency=A&Year={years}`
   - Cache responses to `data/raw/bea/{table_id}_{year_min}_{year_max}.json` (gitignored)
   - Handles rate limits (BEA caps at 100 req/min) with exponential backoff
   - Unit tests against the cached responses

4. **L01_S201_alternative_gfp.py**:
   - Fetch NIPA Table 1.1.5 (Gross Domestic Product); extract `GDP`, `CFC` (depreciation), `NDP`
   - Combine with S503 (GFP*) from existing pipeline output
   - Compute the comparison: `GFP_GDP_ratio = S503 / GDP`, `FP_NDP_ratio = (S503 - CFC) / NDP`
   - Write to `data/final/S201.csv` in long format
   - V03: validate against the book's Ch2 Figure 2.1 values (which I haven't found yet — look in book_text_1994 for the corresponding page; otherwise use the legacy `Inputs/Salvaged/methodology_decisions/` for known values).

5. **L01_ES1201_nsw_gdp_st2002.py + L01_ES1202_nsw_ec_st2002.py**:
   - ES1201 = S607 / GDP (NIPA Table 1.1.5)
   - ES1202 = S607 / EC (NIPA Table 2.1 or H.1 EC column already loaded)
   - V03: ratios should be in [-0.05, +0.05] for ES1201 across full period (NSW is small relative to GDP); validates against ST 2002 paper if benchmarks available.

6. **Moos 2017 series (ES1301, ES1302, ES1304, ES1305)**:
   - ES1301 = nsw_reconciled / GDP, using `Inputs/Salvaged/Moos/...` (already copied? — check)
   - ES1302 = nsw_reconciled / compensation
   - ES1304 = comparison delta vs ES1201 at overlap years
   - ES1305 = structural-shift indicator (pre/post-2000 slope diff)

7. **Partial AS001 + AS004**:
   - AS001 needs Pn from NIPA Table 1.10 (corporate profits) and S505 from existing pipeline. Compute b = (T + Eu)/S* with T from S604 and Eu approximated as 0 (then mark explicitly that without K* we can only do a partial). Better: WAIT for Sprint 3's K* before activating; just produce a partial-DPR-update noting NIPA is now available.
   - AS004 needs GDPDEF from FRED (Sprint 4) and BLS CES hours (Sprint 4). Same wait.

### Acceptance criteria for Sprint 2

- [ ] `code/run.py` works and replaces ad-hoc PowerShell loops
- [ ] `code/utils/nipa.py` fetches and caches at least 3 NIPA tables (1.1.5, 2.1, 1.10)
- [ ] S201, ES1201, ES1202, ES1301-1305 implemented and PASS (8 series)
- [ ] `python run.py --validate-only` reports 51/62 PASS
- [ ] No api_keys committed to git
- [ ] DPRs updated for the 8 series + one ADR (architecture decision record) documenting the NIPA loader design
- [ ] Commit: `"Sprint 2: BEA NIPA loader + 8 NIPA-dependent series PASS (51/62)"`

### Risks

- BEA API rate limits — mitigated by aggressive caching
- BEA table schemas change over time (NIPA underwent the 2013 comprehensive revision) — V03 must check known endpoints to detect schema drift

---

## Sprint 3 — K\* (Capital Stock) sourcing and 5 dependent series

**Goal**: Source the productive constant capital stock `K*` and activate S510, S513, S514, AS001 (full). Also enables S702 once IO matrices are in (Sprint 4).

**Effort**: 1–2 sessions. K* is conceptually involved (productive/unproductive concordance over NAICS) but the data is publicly available.

### Step-by-step

1. **Source K\* raw data**:
   - BEA Fixed Assets Table 4.1 (net stock by detailed industry, NAICS-classified)
   - Available via BEA API: `datasetname=FixedAssets&TableName=Table_4_1_*`
   - Cache to `data/raw/bea/fixed_assets_4_1_*.json`

2. **Implement productive/unproductive concordance**:
   - Reference: book Appendix C lists which 2-digit SIC sectors are productive vs unproductive. The NAICS equivalent is documented in ST2's `Inputs/Concordances/` (verify, copy if present).
   - Write `code/utils/concordance.py` with `apply_productive_partition(df: pd.DataFrame) -> pd.DataFrame`
   - This is where DPR decisions matter most — productive-sector membership determines whether each NAICS industry contributes to K* or to K_u.

3. **L01_K_star.py + P02_K_star.py + V03_K_star.py**:
   - Register K* in the registry as a new derived series (call it `S513-K`, or break it out as `S517-K_star` if we want it as a first-class series).
   - Load Fixed Assets Table 4.1, apply concordance, sum across productive NAICS, write annual time series.
   - V03: validate against book Appendix Table H.2 (capital stock) endpoints (1948, 1989) — need to find these values; if not in the salvaged KB, calculate from the ST2 `K_star_by_industry.csv` output (treating that as a benchmark reference, not as a source).

4. **Activate S510 (K/V\*)**:
   - Compute S510 = K* / S504 year by year.
   - V03: range check (typical Marxian VCC is 5–20).

5. **Activate S513 (Marxian profit rate r\* = S\*/(C\* + V\*))**:
   - r* = S505 / (K* + S504). Note: book sometimes uses C* = K* + Mp (stock + flow); we follow ST 1994's exact formula per the research JSON.
   - V03: benchmarks from validation_config or book Table 5.10 (likely 1948=~0.18-0.20, 1989=~0.13). Need to verify exact values.

6. **Activate S514 (capacity-adjusted r\*_adj)**:
   - Fetch FRED series `TCU` (Total Industrial Capacity Utilization), aggregate to annual.
   - Cache to `data/raw/fred/TCU_annual.csv`
   - Compute S514 = S513 × (TCU/100)
   - V03: comparable to S513 endpoints minus the ~15-20% TCU adjustment.

7. **Activate AS001 (Social Burden Rate)**:
   - With K* and NIPA Pn now both present, compute Eu = S505 - Pn - S604 (residual).
   - b = (T + Eu) / S505 = (S604 + Eu) / S505 = 1 - Pn/S505 (simpler form).
   - V03: book Table 7.1 reports b rises 0.56 (1948) → 0.66 (1989). Validate.

### Acceptance criteria for Sprint 3

- [ ] K* time series loaded and validated against book Table H.2 (or against ST2 K_star_by_industry.csv as fallback benchmark)
- [ ] S510, S513, S514, AS001 all PASS
- [ ] `python run.py --validate-only` reports 55/62 PASS
- [ ] Concordance documented in `docs/methodology/productive_classification_NAICS.md`
- [ ] Commit: `"Sprint 3: K* sourcing + S510/S513/S514/AS001 (55/62 PASS)"`

### Risks

- Productive/unproductive concordance is a judgment call at SIC-NAICS boundary cases — the DPR must document every borderline decision
- BEA Fixed Assets schema may have category changes between revisions

---

## Sprint 4 — IO matrix loader + Chapter 7 series

**Goal**: Build the I-O matrix loader (the heaviest single infrastructure piece), then activate S401, S402, S701, S702, S703.

**Effort**: 2 sessions. The I-O matrix loader is the largest single piece of new code.

### Step-by-step

1. **Source BEA Benchmark I-O tables**:
   - Available at https://www.bea.gov/industry/input-output-accounts-data
   - Benchmark years: 1947, 1958, 1963, 1967, 1972, 1977, 1982, 1987, 1992, 1997, 2002, 2007, 2012, 2017
   - Pre-1997 are SIC-classified; post-1997 are NAICS — the loader handles both
   - Cache to `data/raw/bea/io_matrices/{year}/` with Use, Make, and Z matrices each as separate CSVs

2. **Write `code/utils/io_matrix.py`**:
   - `load_benchmark(year: int) -> dict[str, pd.DataFrame]` returning `{"Use": ..., "Make": ..., "Z": ...}` matrices
   - `compute_A_matrix(Use, Make) -> pd.DataFrame` — technical coefficients
   - `compute_B_matrix(A) -> pd.DataFrame` — Leontief inverse via `np.linalg.inv(I - A)`
   - `apply_productive_partition(matrix, concordance) -> pd.DataFrame` — slice to productive sectors only

3. **Implement S401 (A-matrix summary)**:
   - For each benchmark year: compute A, then extract summary stats:
     - `n_sectors`, `sparsity`, `max_eigenvalue`, `condition_number`, `leontief_max_dev`, `n_productive`, `n_unproductive`
   - Validate that `max_eigenvalue` < 1.0 (Hawkins-Simon condition) at every benchmark year
   - Compare against ST2's T401.csv values as cross-check

4. **Implement S402 (B-matrix summary)**:
   - Same shape as S401 but for the Leontief inverse
   - Validate against ST2's T402.csv

5. **Implement S701 (Labor Values)**:
   - Labor value vector: `λ = l (I - A)^-1` where `l` is the labor input coefficient vector
   - Need BLS CES sectoral employment for benchmark years (Sprint 4 sub-task: BLS loader)
   - Aggregate to scalar series (single number per benchmark year) per registry convention
   - Validate against ST2's T701.csv as reference

6. **Implement S702 (Prices of Production)**:
   - `p = (a₀(1+r) + Ap)` solved for `p` — requires S513 (r*) from Sprint 3
   - Cross-Sprint dependency: needs Sprint 3 complete
   - Validate against ST2's T702.csv

7. **Implement S703 (Value-Price Deviations)**:
   - `deviation = (p - λ) / λ × 100`
   - Book finding: deviations small (~2-15%), confirming labor value as a good first approximation

### Acceptance criteria for Sprint 4

- [ ] BEA Benchmark I-O matrices cached for all 9-13 benchmark years
- [ ] `code/utils/io_matrix.py` covered by basic unit tests
- [ ] S401, S402, S701, S702, S703 PASS
- [ ] `python run.py --validate-only` reports 60/62 PASS
- [ ] Commit: `"Sprint 4: IO matrix loader + Ch7 (5 series, 60/62 PASS)"`

### Risks

- BEA Benchmark I-O publishes Detailed (~400 sectors) and Summary (~71 sectors) versions — pick one consistently (book uses Detailed for pre-1997, Summary for post). Document choice.
- Detailed matrices are large (~400×400); memory footprint matters

---

## Sprint 5 — Remaining Wave 4 follow-ups and S801

**Goal**: Activate the last 2 ES series (Karabacak Turkey 2022) and S801 (cross-study comparison).

**Effort**: 1 session.

### Step-by-step

1. **ES1601, ES1602 (Karabacak & Tonak 2022 Turkey)**:
   - Source data in `Inputs/ST2/Inputs/ExternalSources/Turkey2022/` (multiple FRED, World Bank, OECD inputs)
   - Read the paper (PDF in salvaged folder) to confirm the exact formula
   - Likely: ES1601 (Turkey Labor Share) = (worldbank_turkey_structural compensation / GDP); ES1602 (Turkey NSW/GDP) = computed from OECD tax + WB government consumption
   - Validate against Karabacak & Tonak (2022) paper's published Figure 4 endpoints (1980, 2019)

2. **S801 (Cross-Study Comparison)**:
   - Now that ES1401-1404 are present, merge S506, S511, ES1401, ES1402 into one wide CSV
   - Columns: year, ST_e, Mohun_e, e_diff, ST_LpL, Mohun_LpL, ST_VW (per ST2's T801.csv schema)
   - V03: round-trip values match upstream sources

### Acceptance criteria for Sprint 5

- [ ] ES1601, ES1602, S801 PASS
- [ ] `python run.py --validate-only` reports 62/62 PASS (or 62 minus any genuinely unrecoverable series)
- [ ] Commit: `"Sprint 5: Karabacak Turkey + S801 cross-study (62/62 PASS)"`

---

## Sprint 6 — Visualization (`/anu-visualize`)

**Goal**: Build the interactive Dash app (or R Shiny — choose at start of sprint) exposing all 62 series.

**Effort**: 1–2 sessions.

### Step-by-step

1. **Invoke `/anu-visualize init` skill** to scaffold the app structure under `viz/`.
2. **Choose framework**: Plotly Dash (Python-native, simpler deployment) vs R Shiny (richer ecosystem for economics). **Recommend Dash** for this project (Python-only stack matches the pipeline).
3. **Wire data sources**:
   - Each `chopped/{sid}.csv` is the canonical data source for one tab.
   - `SUBSOURCE_METADATA.json` drives trace labels, colors, units.
   - Per-series Extenbooks accessible via "Download workbook" link.
4. **Build per-chapter tabs**:
   - Ch5 Exploitation Accounting (16 series)
   - Ch6 NSW (9 series)
   - Ch2/4/7/8/9 Special Topics
   - External Studies (25 series, sub-tabs by study)
   - Analytical Derivations (4 series)
5. **Methodology panel**: each series gets a click-through panel showing the DPR markdown rendered + the research JSON entries + the construction Mermaid diagram.
6. **Validation widget**: a "Validation Health" tab showing the latest `VALIDATION_REPORT.json` aggregated by chapter.

### Acceptance criteria for Sprint 6

- [ ] `python viz/app.py` launches a Dash server on `:8050`
- [ ] All implemented series are visible and interactive
- [ ] Cross-study comparisons (ST vs Mohun, ST vs Khanjian) are first-class views
- [ ] D10 (Viz Integration) dimension of `/anu-review` scores ≥80
- [ ] Commit: `"Sprint 6: anu-visualize Dash app — all 62 series"`

---

## Sprint 7 — Publication (Wave 6)

**Goal**: Produce the three public distribution artifacts (GitHub repo, Drive bundle, audit-grade `.zip`) and push the GitHub remote.

**Effort**: 1 session (mostly mechanical once `/anu-publish` is invoked).

### Step-by-step

1. **Write the public-facing top-level docs**:
   - `README.md` for `Technical/` (becomes the GitHub repo root). Audience: developers who `git clone`. Include quick-start (`pip install`, `python run.py --validate-only`), data sources, citation, license.
   - `INSTALL.md`: API key setup, dependency install, troubleshooting.
   - `CITATION.cff`: machine-readable citation. Include the original Shaikh & Tonak (1994) book + this replication package as a distinct artifact.
   - `LICENSE`: MIT or BSD-3-Clause (choose at start; recommend MIT for replication packages).
   - `codemeta.json`: software metadata.

2. **Write the methodology PDF**:
   - LaTeX source in `docs/methodology/methodology.tex`
   - Composes per-chapter sections from the chapter DPRs + decompositions
   - Sections: introduction, data sources, Marxian categories (Ch 2 + 4 + 5 + 6 + 7 + 8 + 9), external studies, analytical derivations, divergences from ST2, validation summary
   - Build with `latexmk -pdf docs/methodology/methodology.tex` → `Outputs/Reports/methodology.pdf`

3. **Run `/anu-publish audit`**:
   - Should produce `Outputs/Publish/` as a clean git tree
   - Scrub rules per the Anu Framework + the scrub list documented in our plan file:
     - Strip `D:/Arcanum`, `Council/`, `Druck`, `Robin`, `Robert`
     - Strip `[YYYY.MM.DD]` filename prefixes
     - Strip "Arcanum research workspace" branding
     - Strip `DEC-XXX` internal IDs (or expand them)
   - Verify: `grep -r "D:/Arcanum\|Council\|Druck\|Robin\|Robert" Outputs/Publish/` returns zero hits.

4. **Run `/anu-drive generate`**:
   - Produces `Outputs/Drive/` with master xlsx + per-series extenbooks + plain-text README + methodology PDF
   - Designed for scholars who don't `git clone`

5. **Run `/anu-archive generate`**:
   - Produces `Outputs/Archive/measuring-wealth-of-nations-archive-v1.0.zip`
   - Includes everything in Publish + Drive + Salvaged provenance + MANIFEST.json + CHECKSUMS.txt
   - This becomes the GitHub Release asset (NOT Zenodo per saved feedback)

6. **Final `/anu-review` whole-project audit**:
   - Must score ≥85% across all dimensions
   - D14 (Outward-Facing Intelligibility) is now in scope — must hit ≥90 for distribution
   - Address any D14 findings before pushing

7. **GitHub remote push**:
   - Create `github.com/andenick/measuring-wealth-of-nations-replication` (public)
   - From `Outputs/Publish/`: `git init`, push to origin
   - Create v1.0 GitHub Release; attach `measuring-wealth-of-nations-archive-v1.0.zip`
   - Add Topics: `economics`, `marxian`, `replication`, `data`, `shaikh-tonak`

8. **Drive folder share**:
   - Upload `Outputs/Drive/` to Google Drive
   - Set folder to "Anyone with link can view"
   - Add the Drive link to the GitHub README

### Acceptance criteria for Sprint 7

- [ ] `Outputs/Publish/` is clean (zero internal references)
- [ ] `Outputs/Drive/` opens without code
- [ ] `Outputs/Archive/...zip` extracts and SHA-256 verifies
- [ ] Methodology PDF builds clean with no LaTeX errors
- [ ] Fresh-clone smoke test: clone the public repo, `pip install -r requirements.txt`, `python run.py --validate-only` completes in < 5s
- [ ] GitHub Release v1.0 published
- [ ] `/anu-review` whole-project audit ≥85%, D13 and D14 GREEN
- [ ] Commit: `"Sprint 7: Wave 6 distribution — GitHub Release v1.0"`

---

## Sprint 8 — Quality and knowledge improvements

**Goal**: Post-publication polish, KB enrichment, and skill updates surfaced during the build.

**Effort**: Open-ended; can be staged across multiple later sessions.

### Step-by-step

1. **Re-run `/sphdarp` on Ch5 narrative**:
   - Current L1 KB coverage is 12.5% (only pages 100, 140 of the ~50 Ch5 pages extracted)
   - A focused `/sphdarp` run on pages 100-160 of the book PDF would lift L1 from 65 → ~95
   - Updates research JSONs with richer quotes; re-runs `/anu-review` for a final score lift

2. **Update Anu skills surfaced during build** (per plan task #14):
   - **anu-ingestion**: formalize `prefix_scheme` block in the registry schema spec
   - **anu-publish**: codify the scrub rule set (D:/Arcanum, Council/, Druck, Robin, Robert, `[DATE]` prefixes, DEC-XXX) as an actual lint rule in `anu-publish/audit.py`
   - **anu-drive**: verify generator handles multi-prefix (S/ES/AS) series IDs
   - **anu-archive**: strip Zenodo metadata template fields from SKILL.md (GitHub Releases only per feedback)
   - **anu-replicator**: regex update for S/ES/AS prefix discovery
   - **anu-extension**: formalize `extension: null` as valid for ES/AS series
   - **anu-docs**: pre-publication tier-check for scrubbed paths
   - **anu-doctor**: rerun after each skill update; verify zero failures

3. **Activate the 10 documented Ch5 EPRs**:
   - Each of S501, S504, S505, S506, S511, S512, S513, S514, S515, S516 has an EPR with an activation checklist
   - With NIPA + K* + TCU now sourced (Sprints 2–4), extend each loader to fetch the post-1989 component and splice
   - This produces the FULL 1948–2024 time series for the headline 10 series — the publication's flagship deliverable

4. **Per-series narrative READMEs in `docs/series/`**:
   - For top 10 most-cited series, write a 1-page narrative DPR companion explaining the economic significance in plain language
   - Audience: economists who aren't Marxists but want to understand the framework

5. **Replication tests in CI**:
   - GitHub Actions workflow: clone, install, run `--validate-only`, fail if any series goes from PASS to FAIL
   - Catches regressions from any future commits

6. **Optional: peer outreach**:
   - Send the GitHub link to Prof. Tonak (using `Salvaged/FromTonak/Email_to_Tonak_Draft.md` as starting template)
   - Tag relevant authors in the issues page

### Acceptance criteria for Sprint 8

- [ ] `/anu-doctor` clean after all skill updates
- [ ] Full 1948–2024 time series for the 10 Ch5 EPR series
- [ ] CI passes on every push
- [ ] L1 KB coverage > 80% via `/sphdarp` re-run

---

## Sprint sequencing — recommended order

```
Sprint 1   ──>   Sprint 2   ──>   Sprint 3   ──>   Sprint 4   ──>   Sprint 5
(quick      (NIPA           (K* +              (IO matrices       (Karabacak
 wins)       loader)         capital-stock      + Ch7)             + S801)
                             series)
                                                                       │
                                                                       v
                                                                  Sprint 6   ──>   Sprint 7   ──>   Sprint 8
                                                                 (visualize)       (publish)        (polish)
```

**Sprints 1, 2 are non-blocking** — can run in parallel if multiple agents are deployed.
**Sprint 3 depends on Sprint 2** (NIPA needed for AS001).
**Sprint 4 depends on Sprint 3** (S702 needs r* from S513).
**Sprint 5 depends on Sprint 4** (S801 needs Wave 4 + Mohun comparisons).
**Sprint 6 depends on Sprint 5** (visualize all 62 once they're all built).
**Sprint 7 depends on Sprint 6** (D10 viz dimension is gated for publication).
**Sprint 8 is post-publication polish.**

**Optimistic total**: 8–12 focused sessions to reach Sprint 7 close. **Realistic**: 12–18 sessions accounting for debugging, schema drift in BEA APIs, and concordance edge cases.

---

## Cumulative milestones

| Milestone | Sprint | Series PASS | Notes |
|---|---|---|---|
| Quick wins close | 1 | 43/62 (69%) | All zero-data-dependency series active |
| NIPA series close | 2 | 51/62 (82%) | First major infrastructure piece done |
| Capital series close | 3 | 55/62 (89%) | Headline Marxian profit rate live |
| Ch7 close | 4 | 60/62 (97%) | I-O matrix infrastructure done |
| All series close | 5 | 62/62 (100%) | Every registry entry validated |
| Viz close | 6 | 62/62 | Dash app live, D10 ≥80 |
| Publication | 7 | — | GitHub Release v1.0 live |
| Polish | 8 | — | KB enrichment, skill updates, CI |

---

## Risk register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| BEA API schema drift between fetches | Medium | Medium | Aggressive caching + V03 endpoint checks |
| Productive/unproductive NAICS concordance edge cases | High | Low-medium | Document every borderline decision in `productive_classification_NAICS.md`; sensitivity check vs Mohun's classification |
| K* benchmark unrecoverable from book Table H.2 | Low | High | Fall back to ST2's `K_star_by_industry.csv` as a reference benchmark, document the decision |
| `/anu-publish` scrub leaves residual internal references | Medium | High | D14 audit catches; CI-add a final `grep` check |
| LaTeX methodology PDF builds break in CI | Medium | Low | Use `latexmk -interaction=nonstopmode` and pin LaTeX dependencies |
| Drive folder share permissions change | Low | Low | README links to specific Drive folder ID; can re-share if needed |
| Prof. Tonak feedback requires major revisions | Low | Medium | Delivery via Drive bundle (consumer tier) makes iteration cheap |

---

## Open questions to resolve in-flight

These are flagged for resolution at the start of the relevant sprint:

1. **Sprint 2**: Should we cache BEA responses for the full 1929–2024 range up front, or fetch per-table-per-sprint? Bigger cache = faster downstream; bigger initial commit (~50MB).
2. **Sprint 3**: When sourcing K\*, do we use BEA's NAICS-only post-1997 series and accept the SIC→NAICS break as a documented divergence, or attempt to bridge via the BLS bridge tables? The simpler path is the documented break; the cleaner path is bridge tables.
3. **Sprint 4**: For the I-O matrices, use BEA's Detailed (~400 sectors) or Summary (~71 sectors)? Book uses Detailed; modern computers handle it fine, but it bloats the cache.
4. **Sprint 6**: Dash vs R Shiny? Recommend Dash (Python-only stack). Pin choice at sprint start.
5. **Sprint 7**: GitHub Release vs simply tagging the GitHub repo. Recommend Release with attached `.zip` archive — gives the audit bundle a stable URL.
6. **Sprint 8**: Should the 10 Ch5 EPR activations be a separate sprint (call it Sprint 8a) before publication, or after as a v1.1? Recommend BEFORE publication — the full 1948–2024 series is the marketing hook.

---

## Definition of done (project-level)

The project is "done" when:

- [ ] 62/62 series PASS validation (or fewer with documented `data_unavailable` status — no fabrication)
- [ ] Full 1948–2024 time series for the 10 headline Ch5 extendable series
- [ ] `/anu-review` whole-project audit ≥85%; D13 + D14 GREEN
- [ ] GitHub repo public at `andenick/measuring-wealth-of-nations-replication` with v1.0 Release
- [ ] Drive folder shareable; methodology PDF embedded
- [ ] Audit-grade `.zip` attached to GitHub Release with SHA-256 verifiable manifest
- [ ] Fresh-clone smoke test passes in < 5 seconds
- [ ] CI green on every push
- [ ] All Anu skill updates surfaced during build are applied; `/anu-doctor` clean
- [ ] Email draft to Prof. Tonak prepared (sent at user's discretion)

---

*Roadmap maintained as part of the working-tree `docs/` and updated at the end of each sprint. The full per-series provenance lives in `docs/series/`; per-chapter quality audits in `docs/chapters/`; this file is the cross-cutting planning view.*

*Last updated: 2026-05-14, after Wave 5 partial close (35/62 PASS, commit `35c8f62`).*
