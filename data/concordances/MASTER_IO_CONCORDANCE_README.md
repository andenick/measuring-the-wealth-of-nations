# MASTER_IO_CONCORDANCE — construction & provenance

**Project:** RMWND — *Measuring the Wealth of Nations* (Shaikh & Tonak 1994), comprehensive review Phase 2, task **T5**.
**Built:** 2026-07-01 by `Technical/Handoffs/REVIEW_2026-07/scratch/build_master_io_concordance.py` (fully reproducible).
**Files:** `MASTER_IO_CONCORDANCE.csv` (data), `MASTER_IO_CONCORDANCE.xlsx` (2 sheets: data + README), this file.

A single **long-format** downloadable concordance — one row per **vintage x industry** — that maps every
Input-Output industry, across every vintage this project uses, to its Shaikh-Tonak (ST) productive /
unproductive / trade / government classification, with a **real, checkable source on every row**. Where the
1994 book is silent and only the literature supports a call, the source says so; nothing is fabricated.

## Schema (11 columns)

`vintage_year, scheme, sector_code, sector_name, sic_range, naics_code, st_classification,
productive_share, classification_source, bridge_quality, notes`

- **scheme**: `SIC-85` (book benchmark vintages), `82x88` (book final-table scheme, Appendix A.1),
  `NAICS-benchmark` (1997/2002/2007/2012/2017), `NAICS-71` (annual series).
- **st_classification** enum: `productive / unproductive / trade / govt / mixed / n.a.`
- **productive_share**: `1.0` productive, `0.0` unproductive/trade/govt(admin), blank for `n.a.`/`mixed`.

## Coverage (994 rows total)

| vintage_year | scheme | rows |
|---|---|---:|
| 1947 | SIC-85 | 85 |
| 1958 | SIC-85 | 85 |
| 1963 | SIC-85 | 85 |
| 1967 | SIC-85 | 85 |
| 1972 | SIC-85 | 85 |
| 1977 | SIC-85 | 85 |
| 1972 | 82x88 | 88 |
| 1997 | NAICS-benchmark | 65 |
| 2002 | NAICS-benchmark | 65 |
| 2007 | NAICS-benchmark | 65 |
| 2012 | NAICS-benchmark | 65 |
| 2017 | NAICS-benchmark | 65 |
| annual-1997+ | NAICS-71 | 71 |

**Classification distribution:**

| st_classification | rows |
|---|---:|
| productive | 814 |
| unproductive | 103 |
| trade | 36 |
| n.a. | 35 |
| govt | 5 |
| mixed | 1 |


## Blocks and build rules

### 1. SIC-85 book vintages (1947, 1958, 1963, 1967, 1972, 1977) — 6 x 85 rows
- `sector_code`/`sector_name`/`sic_range` from `data/raw/concordances/io_85_to_nipa_13_concordance.csv`.
- `naics_code` = the semicolon-joined NAICS codes from `Technical/data/source/concordances/sic_naics_bridge.csv`
  (one-to-many bridge rows joined); `bridge_quality` likewise from the bridge (mostly `coarse_aggregation`;
  `unmapped` for special sectors 81-84 with no SIC<->NAICS link).
- `st_classification` + `classification_source` = the **T2 adjudication**
  (`P2_appendix_F_verdicts.csv` / `P2_APPENDIX_F_ADJUDICATION.md`): 81 book-confirmed, 1 literature-only,
  3 unsupported-with-corrections. `productive_share` per `Technical/data/source/appendix_F/Table_F_1.csv`
  **with the T2 corrections applied**.
- **The 85-order classification is CONSTANT across the six book vintages** — ST apply one categorical sector
  taxonomy (Table 3.1/3.2, §3.6.1) to all benchmark years. Rows are emitted per vintage so each year is
  independently queryable, but the classification does not vary 1947->1977.
  **Caveat:** within-sector productive fractions in ST/Mohun are *time-varying* annual BLS production-worker
  `(Lp/L)` ratios (the REAL Table F.1 at `.../CSV_Tables/table_031_032_04*.csv`), NOT the static
  `productive_share` here; re-apply BLS ratios at compute time for true productive-worker counts.

### 2. The 1972 final "82x88" scheme (Appendix A.1) — 88 rows
- Rows = the final-table sectors from ST 1994 **Appendix A Table A.1** (KB `table_026_026_01.csv`): sectors
  1..88 (industry rows 1-80, value-added/final-demand block 81-88).
- Classification is **aggregated from the mapped 85-order members' ST broad-category classifications**; where
  members agree it is that class, where they disagree it is `mixed` with the member split in `notes`.
  Source = "ST 1994 Appendix A Table A.1 (KB table_026_026_01) + member-sector adjudication (P2 T2)".
- **85-order MISMATCH CAVEAT (known limitation, flagged per row):** A.1's own "1972 85-order" (Livestock and
  products / Iron mining / ...) is a **different aggregation** from the **BEA-1967 85-order** used by the
  SIC-85 block (Dairy farm products / Coal mining / ...). Membership here is based on A.1's OWN numbering and
  names, classified by ST broad-category **name-match**; the two 85-orders are **not reconciled
  one-to-one**. This is confirmed in the T2 adjudication (Blocker #2) and the reconstruction's own
  PROVENANCE limitation #4. Do NOT force a false alignment between the two blocks' sector numbers.
- Notable ST routing: A.1 **routes "Eating & drinking places" (orig 74) into the Trade aggregate (final 65)**
  even though eating&drinking is productive-by-nature under §3.6.1 -> final sector 65 is therefore `mixed`.

### 3. NAICS-benchmark vintages (1997, 2002, 2007, 2012, 2017) — 5 x 65 rows
- `sector_code` = the 65 NAICS column codes from each year's matrix header
  (`Technical/data/intermediate/io_matrices_labeled/{YEAR}_A_matrix_naics_labeled.csv`). Note 2017's set
  differs (adds `525`, drops `GFE`).
- `sector_name` from the **standard BEA GDP-by-Industry / Summary I-O industry code list** (bea.gov/industry).
- `st_classification` from `data/raw/concordances/naics_71_to_classification.csv`; `sic_range` =
  reverse-bridge SIC ranges (semicolon-joined) from `sic_naics_bridge.csv` (blank where no exact bridge row).
- **These are NOT book-confirmed** — the 1994 book predates the first NAICS benchmark (1997). The
  classification is the NAICS **re-derivation** of the ST rule; every row's `notes` says so.
- The 65-code benchmark tier is a **subset of the 71-industry summary tier** (six codes
  111CA / 525 / GFGD / GFGN / GSLG / HS are aggregated or absent in a given benchmark matrix).

### 4. NAICS-71 annual block (`vintage_year = annual-1997+`) — 71 rows
- The full 71-industry summary tier from `naics_71_to_classification.csv` (the annual integrated I-O series;
  the natural NAICS extension vehicle past 1977). Same NAICS classification rules and honesty caveats.

## The `trading -> trade` mapping (ST treatment)
`naics_71_to_classification.csv` uses the label **`trading`** (wholesale/retail/rental: 42, 441, 445, 452,
4A0, 532RL). In the ST framework trade is **circulation** and its labor is **unproductive** (it realizes,
does not create, value). These rows are emitted with `st_classification = trade` and `productive_share = 0.0`,
and each `notes` states "trading = circulation, economically UNPRODUCTIVE". Government mapping: BEA
`govt_enterprise` (GFE/GSLE) -> `productive` (ST government *production* enterprises); BEA `govt_admin`
(GFGD/GFGN/GSLG) -> `govt` with `productive_share 0.0` (general government administration is unproductive
under ST §3.2), preserving the "it is government" information while carrying the unproductive verdict
numerically.

## The three T2 corrections applied (vs. the raw reconstruction)
1. **Sector 85 "Government industry": `mixed (0.167)` -> `unproductive (0.0)`.** The 0.167 count-ratio proxy
   is not book-supported; ST treat general government as a nonproduction/royalties (secondary) sector whose
   labor is unproductive (§3.2, §3.6.1, Table 3.1). Government *enterprises* are separate sectors (79/80),
   already productive.
2. **Sector 82 "Business travel, entertainment, gifts": `unproductive` -> `n.a.`** — special BEA IO
   intermediate-use column, not a labor-bearing sector. Zero numeric impact; a labeling/honesty fix.
3. **Sector 83 "Office supplies": `unproductive` -> `n.a.`** — same rationale as sector 82.

**Documented caveat (retained, not corrected): Sector 74 "Business services" stays `unproductive`, verdict
`literature-only`.** The 1994 book is silent on business services; the unproductive call rests entirely on
Mohun 2013 (RRPE 46(3):355-379). Mohun actually **splits** the sector (engineering/design/R&D productive;
legal/accounting/advertising/consulting/personnel unproductive) — a fractional treatment is an optional
future refinement (needs sub-sector payroll weights not in the 85-order table).

## Known limitations
- The static `productive_share` is a **categorical** filter; ST/Mohun within-sector productive fractions are
  **time-varying BLS ratios** and must be re-applied at compute time (see Block 1 caveat).
- The SIC-85 (BEA-1967) and 82x88 (book 1972) blocks use **two different 85-orders** that are not reconciled
  one-to-one; keep them separate (Blocker #2 above).
- NAICS blocks sit on the **other side of the 1977->1997 SIC->NAICS discontinuity** from the book's tables;
  continuation rests on the `naics_71_to_classification.csv` re-derivation, not on book confirmation. See
  `P2_IO_VINTAGE_LEDGER.md` for the full vintage-by-vintage discontinuity map and the post-1994 Marxian
  literature cross-check (Mohun, Tsoulfidis-Paitaridis, Rotta, Camara).
- `Technical/data/source/appendix_F/Table_F_1.csv` is a **filename misnomer** (it is the predecessor-build
  `io_85_to_nipa_13` categorical filter, NOT the book's real annual Table F.1); this concordance uses it only
  for `productive_share` and applies the T2 corrections on top.

## Sources (all real, checkable)
- `data/raw/concordances/io_85_to_nipa_13_concordance.csv`
- `Technical/Handoffs/REVIEW_2026-07/P2_appendix_F_verdicts.csv` + `P2_APPENDIX_F_ADJUDICATION.md` (T2)
- `Technical/data/source/appendix_F/Table_F_1.csv` + `PROVENANCE.md`
- `Technical/data/source/concordances/sic_naics_bridge.csv`
- `data/raw/concordances/naics_71_to_classification.csv`
- `Technical/HDARP_Extractions/1994_Measuring_Wealth_v2/CSV_Tables/table_026_026_01.csv` (Appendix A.1)
- `Technical/data/intermediate/io_matrices_labeled/{1997..2017}_A_matrix_naics_labeled.csv` (headers)
- `Technical/Handoffs/REVIEW_2026-07/P2_IO_VINTAGE_LEDGER.md` + `P2_vintage_ledger.csv` (vintage citations)
- Mohun, S. (2013/2014) "Unproductive Labor in the U.S. Economy 1964-2010," RRPE 46(3):355-379.
- Shaikh, A. & Tonak, E.A. (1994) *Measuring the Wealth of Nations*, CUP — Ch.3 (Tables 3.1/3.2, §3.6.1), Appendix A.
- BEA GDP-by-Industry / Summary Input-Output industry code list (bea.gov/industry) for NAICS sector names.
