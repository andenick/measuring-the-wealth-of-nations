# Changelog — Measuring the Wealth of Nations (RMWND) replication

All notable changes to the public replication bundle are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
the project adheres to [Semantic Versioning](https://semver.org/).

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
- Internal one-shot build/HDARP-integration helper scripts and per-wave QA
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
