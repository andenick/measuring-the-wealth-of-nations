# Changelog — Measuring the Wealth of Nations (RMWND) replication

All notable changes to the public replication bundle are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
the project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.1.1] — 2026-07-10 — Metadata erratum: XS1202 1964 validation anchor source-verified

Metadata-only patch. **No data-column value changed** — every published series value is
byte-identical to v2.1.0. This corrects one validation *reference value* (an anchor used only to
check a series, never a served number) and adds source-provenance notes.

### Fixed
- **`XS1202` (Net Social Wage / EC) 1964 validation reference value: −0.0167 → −0.009.** The prior
  −0.0167 erroneously divided the 1964 net social wage (−3.49 bn) by **1954's** employee compensation
  (209.37 bn). The published source — Shaikh & Tonak, "The Rise and Fall of the U.S. Welfare State"
  (*Political Economy and Contemporary Capitalism*, M.E. Sharpe 2000), ch.29 appendix p.259 — prints the
  1964 column as EC = 370.99 bn, net social wage = −3.49 bn, and the "Net Social Wage Ratio" row as
  **−0.009** (= −3.49 / 370.99). The `XS1202` `reference_source` string is rewritten to cite this
  source-verified derivation. This is a provenance/accuracy correction, not a pass/fail change: the 1964
  check stays PASS and `XS1202` continues to FAIL on 1997 only (the documented DIV-036 NSW-basket
  over-count). It supersedes v2.1.0's XS1202 1964 anchor.

### Changed
- **`DIVERGENCE_REGISTER.json`** — DIV-037 records the source-verified retraction of the interim
  −0.0167 revert; DIV-036 notes the 1997 anchor (+0.005) is now table-grade source-verified (appendix
  p.265); DIV-028 / DIV-071 gain external-anchor notes corroborating the reconstructed kIO exploitation
  arm against Rotta (2018, *CJE*) and Savran & Tonak (1999). Register entry count unchanged (73).

---

## [2.1.0] — 2026-07-09 — Book-faithful gross-K\* profit rate, reconstructed kIO exploitation, Tier-A truth fixes

Four post-v2.0 campaigns (2026-07-07 → 09), all additive: every pre-existing published cell is
byte-identical to v2.0 — new content appends as new columns, new series arms, and new sidecars.
No headline value silently changed.

### Added
- **Book-faithful gross-capital profit-rate variants** — `S517-GROSS-A` (book Table 5.8 gross K\*),
  `S513-GROSS-A` (book r\* = S\*/K\*_gross), `S514-GROSS-A` (book r\*' = r\*_gross/u), book period
  1948–1989 only (`nan` beyond — a current-cost gross stock is genuinely non-constructible after the
  mid-1990s BEA discontinuation, DIV-058 extension arm). These give the profit-rate family its first
  **non-tautological book anchor**: `S513-GROSS` reproduces the printed r\* at **MAE 0.0025 (42/42
  years exact at 2 dp)**. The v2.0 net-capital headline series is retained unchanged; the review showed
  its near-match to the book was a *lucky cancellation* of net-K\*+V\* ≈ gross-K\*, so the gross arm was
  added rather than pretended.
- **Reconstructed time-varying I-O uplift (kIO) rate-of-exploitation arm** — `S506-EXT-MARX-KIO`, and the
  `S506-COMBINED` extension tail (1990–2024) now continues on it. DIV-028's frozen kIO = 1.5714 is
  replaced by an officially-sourced, backward-validated, uncertainty-banded annual series:
  the native 1992 SIC benchmark (the last one) gives **kIO₁₉₉₂ ≈ 1.5696** (corroborating the frozen
  constant); the wedge is then computed annually from the NAICS-era 71-order supply-use margin detail,
  with a real-data 1990–96 bridge. kIO(t) passes through 1.571 in the mid-1990s and **rises to 1.731 by
  2024**. The rate of exploitation runs **e ≈ 2.43 (1990) → 4.46 (2024)** vs the frozen arm's 3.95;
  the frozen arm stays published as the conservative lower bound. Bias decomposition: royalties are 72%
  of the naive level gap, the SIC→NAICS classification jump only +3.7%.
- **Uncertainty-band sidecars** — `S506_KIO_BAND.csv` (two-route kIO band, honestly wider after the
  1996/97 SIC→NAICS seam) and `S701_LAMBDA_BAND.csv` / `S702_LAMBDA_BAND.csv` (labor-value precision
  bands, DIV-042 worst-case common-mode, −10.3%/+13.0%). Shipped under `data/bands/`.
- **Restored per-series author quotes** — 34 published series whose verbatim Shaikh–Tonak quotes were
  loader-invisible under the prior quote schema are now surfaced (36 research JSONs normalized
  additively; loader-visible quotes 110 → 348; zero invented or dropped, proven against archived
  originals). A new hard test (`test_published_quotes.py`) guards the schema.

### Changed
- **λ / p\* labor-value series (`S701`, `S702`) publish at 3 significant figures** (inside the tightest
  F3 sensitivity bound) instead of the former 15–17 digits of false precision; rounding at final-emit
  only (intermediate precision retained). `S703` proven unaffected.
- **`S506-COMBINED` post-1989 tail** now rides the reconstructed-kIO arm (primary continuation); the
  frozen-kIO arm remains published alongside as the lower bound.
- **`XS1202` 1964 reference value corrected to −0.0167** (was −0.009, uncorroborated); DIV-037's rationale
  corrected. Provenance-honesty gain; the honest FAIL set is unchanged.
- **Structural rename**: the misnamed `appendix_F/` filter directory → `ch7_productive_filter/`
  (`io85_pu_classification.csv`), with all 7 consumers updated — byte-identical S70x outputs.

### Fixed
- **Zero unexplained book cells** — the two previously-unexplained 1964 tax cells (S601/S603 vs Appendix
  N.1) were adjudicated as *chosen* divergences (S601: BEA vintage + labor-share; S603: basket breadth
  without the homeowner property filter) and registered as **DIV-072 / DIV-073**. The book-fidelity
  ledger is now 153 divergent rows, **0 uncovered**.
- **Validator honesty** — the 5 residual tautological (echo-the-output) validators plus one A1-missed
  case (S510/S517/XS1301/XS1305/XS1602/S609) were re-anchored to independent sources (tautological
  5 → 0); 3 UNCLEAR validators resolved to book-anchored (XS1102/XS1103 to Table N.2, XS1601 qualified).
- **`XS002`** de-hardcoded — its inlined book Table 5.12 moved to `book_tables/` (byte-identical output).
- Golden fixtures truth-aligned to the registry (metadata-only regen, data cells byte-identical);
  latent `NameError` in `L01_S701` fixed as part of the filter rename.

### Registers & QA
- **`DIVERGENCE_REGISTER.json` grown from 69 to 73 entries** (DIV-070 gross-K\* variant, DIV-071 kIO
  reconstruction, DIV-072/073 the S601/S603 1964 adjudications; DIV-028 upgraded frozen → reconstructed,
  DIV-058 narrowed to the extension arm).
- Gates: **anu-doctor 0 FAIL / 0 WARN**; **pytest 95 passed / 2 skipped / 2 justified xfail**
  (baseline moved 93 → 95 with the new quote test); **per-series validators 60 PASS / 4 honest
  registered FAIL** (XS1101, XS1201, XS1202, XS1602).
- Independently verified end-to-end from the raw government files (kIO₁₉₈₉ reproduced to 1.57141;
  the 2017 margin numerator matches BEA's detail files to the dollar).

### New public artifacts
- `ANSWERS.md` — a leak-scrubbed, answers-first brief (the seven best answers, each with basis and
  pointer) at the repository root.

---

## [2.0.0] — 2026-07-03 — Comprehensive review + D-batch book-fidelity decisions

A full series-by-series review (~50 series re-examined) plus the D-batch of
book-fidelity construction decisions. Numeric corrections propagate through the
chopped CSVs (`data/`), the Extenbooks (`extenbooks/`), the golden fixtures
(`tests/golden_chopped/`), `series_registry.json`, and the divergence register.

### Comprehensive review — data corrections
- Roughly **50 series** re-examined and corrected for provenance, units,
  content labels, and reference values. Corrections are recorded in-line in
  `series_registry.json` (per-series `reason`/`validation_source`) and in
  `DIVERGENCE_REGISTER.json`.
- De-tautologised reference values where the stored anchors merely echoed the
  source/output (e.g. XS1401–XS1404, XS1501–XS1503, S201), replacing them with
  independent external or identity-based anchors.

### D-batch decisions
- **S514** rebuilt on the book's own division into the `r*` (profit-rate) and
  `u` (capacity-utilization) components rather than a single derived form.
- **Chapter-7 `K*` series** now ship a **replication-first primary column**
  alongside labelled **variant columns**, so the canonical replication and the
  sensitivity variants are both first-class and clearly separated.
- **S515 / S516** adopt the **seam candidate (d)** for the book-period /
  extension-period join.
- **Net social wage (S607 cluster)** uses the book-faithful **Candidate A**
  construction for 1952–1989.
- **XS1501–XS1504** rebuilt on **Mohun (2014)** published employment shares
  (1964–2010); the prior mislabelled 1948–1989 predecessor decomposition is
  retired from the primary series and preserved only as a labelled variant.

### Provenance deliverables (new, public)
- `data/PROVENANCE_DICTIONARY.csv` (+ `PROVENANCE_DICTIONARY_README.md`) and
  `data/PROVENANCE_COVERAGE.csv` — per-observation source provenance + coverage.
- `data/COMPONENT_CHAINS.csv` / `data/COMPONENT_CHAINS.json` — derived-series
  component-dependency chains.
- `data/S506_STEP_TABLE.csv` — the S506 step-by-step construction table.
- `data/concordances/MASTER_IO_CONCORDANCE.csv` (+ README) — the master
  input-output sector concordance.

### Registers & QA
- **`DIVERGENCE_REGISTER.json` grown from 12 to 69 entries**, capturing every
  intentional deviation surfaced by the review and D-batch.
- Test suite: **93 passed / 2 skipped / 2 justified xfail**.
- **`anu-doctor`: 0 errors / 0 warnings.**

---

## [1.3] — 2026-06-11 — Series-ID migration + provenance reconciliation

Brings the public bundle into line with the internal canonical tree after the
AS/ES → XS series-ID migration (Series ID Spec v2.2, Anu Framework v12.2) and a
Knowledge-Base reconciliation pass.

### Series-ID migration (AS/ES → XS)
- The 4 analytical/supplementary series (legacy `AS001`–`AS004`) and the 25
  follow-up-study replication series (legacy `ES1001`–`ES1704`) are migrated to
  the canonical **`XS`** ("Extra Series") prefix. `AS`/`ES` are now legacy
  prefixes rejected by the framework.
- Each `XS` entry carries `xs_class` (`appendix` for the former AS analytical
  series, `external_study` for the former ES study replications) and
  `xs_attribution` (e.g. Tonak 1984, Shaikh & Tonak 1987/2002, Moos 2017,
  Mohun 2005/2013, Karabacak & Tonak 2022, Cronin 2001).
- The full old→new correspondence table is published at
  **`MIGRATION/crosswalk.csv`** (with `MIGRATION/PREFIX_SCHEME.md`) — the
  authoritative public crosswalk for anyone who referenced the old IDs.
- Migration applied uniformly to: `series_registry.json`, all chopped CSVs
  (`Data/`), per-series Extenbooks (filenames **and** internals), DPRs/EPRs
  (`Docs/series/`), the replicator scripts (`code/`), golden-output fixtures
  (`tests/golden_chopped/`), and the data files behind the Extenbooks.

### Series scheme (v2.2)
- **33 primary `S` series** (book chapters 2–9) + **29 `XS` extra series**
  (the former 4 AS + 25 ES) = **64 total** (the registry currently holds 35 `S`
  + 29 `XS`; see `series_registry.json` for the authoritative set).
- Every series carries a `publish` flag and a `triage` record
  (`{verdict, reason, date}`).

### Triage verdicts (transparency)
- **Culled series are retained in the bundle but marked `publish: false`** for
  full transparency: **`S401`, `S402`** (primary) and **`XS1601`, `XS1602`**
  (Turkey labor-share / NSW-GDP, Karabacak & Tonak 2022). Downstream consumers
  should honor `publish: false`.

### Provenance reconciliation (KB)
- DPRs and per-series provenance corrected against the Knowledge Base, removing
  hallucinated provenance statements carried by earlier bundles.
- Per-subseries units declared where a series mixed dimensionless ratios with
  level/dollar components.

### Bundle hygiene
- Internal one-shot build/KB-integration helper scripts and per-wave QA
  review reports are no longer shipped (`.publish_ignore`); the reproducible
  pipeline is the numbered L00/L01/P02/V03/O06 scripts.
- Hardcoded workstation paths and internal-tooling references scrubbed from the
  shipped scripts and docs.

### Notes
- Public GitHub repository references (`github.com/andenick/measuring-the-wealth-of-nations`)
  are the project's own publication target and are intentional.

## [1.2] — 2026-05-24

See the project-level `CHANGELOG.md` for the full v1.2 (and earlier) history:
academic-grade public-ready release with the v1.2 reproducibility infrastructure
(build orchestrator, container, pinned dependencies, pre-commit hook).
