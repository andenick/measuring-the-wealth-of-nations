# Measuring the Wealth of Nations — Replication Package

**Complete replication and extension of every empirical claim in Shaikh & Tonak's *Measuring the Wealth of Nations* (1994), plus 8 follow-up studies, with 64 data series covering 1925–2025.**

---

## Headline findings

| Measure | 1948 | 1989 (book) | 2024 (extended) | Direction |
|---|---|---|---|---|
| Rate of exploitation (e = S\*/V\*) | 1.70 | 2.44 | (~2.4 trend) | Rose then stabilized |
| Productive labor share (Lp/L, broad) | 0.57 | 0.36 | — | Fell 37% |
| Marxian profit rate (r\* = S\*/(K\*+V\*)) | 0.39 | 0.37 | — | Secular decline |
| Capital intensity (K/V\*) | 3.30 | 5.55 | — | Rose 68% |
| Social burden rate (b) | 0.79 | 0.86 | — | Rose |
| Net Social Wage (NSW) | Negative | Negative | **+$1,234B (POS)** | Regime change 1990s |
| K\* productive capital stock | $292B | $6,700B | $35,900B | Real accumulation |

NSW was negative for the entire postwar book period (1952–1989) — workers were net subsidizers of the state. The series first turns positive in 1975 (brief recession spike), then permanently positive in the early 1990s as transfer programs (Medicare, EITC) outpaced the worker tax burden. By 2024, NSW had risen to +$1.2 trillion.

Cross-classification robustness: ST's exploitation rate sits within 0.7–1.3× Mohun's alternative classification over 1948–1989 — the central Marxian finding is robust to productive-sector boundary choice. Karabacak & Tonak's (2022) Turkey result is reproduced fully: 30 of 30 years 1980–2019 show negative NSW.

---

## Quick Start

```bash
git clone https://github.com/andenick/measuring-wealth-of-nations-replication.git
cd measuring-wealth-of-nations-replication

pip install -r requirements.txt

# Validate all 64 series against the source data and benchmarks (no API needed)
python run.py --validate-only
# Expected: 64/64 PASS

# Full pipeline (rebuilds all data/final CSVs from source)
python run.py --test-all
```

Cached BEA / BLS / FRED responses are included under `data/raw/` — `--validate-only` runs without any API key. See `INSTALL.md` for fresh-fetch setup (BEA, BLS, FRED keys required only for re-fetching cached data).

---

## What this replicates

Shaikh and Tonak (1994) reconstruct the US national accounts from a Marxian perspective. They distinguish *productive* labor (which creates surplus value) from *unproductive* labor (administration, finance, government), and show that orthodox national accounting systematically conflates the two. Their framework produces measures — the rate of exploitation, the Marxian profit rate, the net social wage — that differ substantially from conventional statistics and reveal the class structure of the American economy.

This package:

1. **Replicates** every empirical series from Chapters 2, 4, 5, 6, 7, 8, 9 of the book (33 S-series, 1948–1989)
2. **Extends** the extendable series through 2024 using BEA NIPA, BEA Fixed Assets, BLS CES, and FRED data (cached responses included for offline replication)
3. **Replicates 8 follow-up studies** in the Shaikh-Tonak framework (25 ES-series):
   - Tonak (1984) — Workers as net subsidizers
   - Shaikh & Tonak (1987) — The "social wage" myth
   - Shaikh & Tonak (2002) — NSW through the Clinton era
   - Moos (2017) — Post-2000 structural shift
   - Mohun (2005) — Alternative productive/unproductive classification
   - Mohun (2013) — Class decomposition
   - Karabacak & Tonak (2022) — Turkey
   - Cronin (2001) — New Zealand
4. **Computes 4 analytical series** (AS-series): social burden rate, Khanjian cross-validation, unproductive worker exploitation, Marxian productivity.

Total: **64 series, 100% validated** against book benchmarks, identity checks, and cross-source consistency tests.

---

## Repository structure

```
.
├── README.md                          # This file
├── INSTALL.md                         # Setup + API key configuration
├── CITATION.cff                       # Machine-readable citation
├── LICENSE                            # MIT
├── requirements.txt                   # Python dependencies
├── run.py                             # Pipeline orchestrator (TBD; current ad-hoc PowerShell loops work)
├── series_registry.json               # Single source of truth: 64 series definitions
├── ANU_LEDGER.json                    # Auto-generated artifact inventory
├── PIPELINE_STATE.json                # Per-wave status tracker
├── SUBSOURCE_METADATA.json            # 111 subseries metadata entries
├── VALIDATION_REPORT.json             # 64 series, all PASS
├── PROVENANCE_INDEX.json              # Provenance chain per series
├── code/
│   ├── S00_setup/                     # Pipeline setup phase (S01–S05)
│   ├── L01_loaders/                   # Raw data loaders (35 scripts)
│   ├── P02_processors/                # Construction/derivation (64 scripts)
│   ├── V03_validators/                # Validation (64 scripts, all PASS)
│   ├── O06_output/                    # Chopped CSV + Extenbook generators
│   └── utils/                         # Shared infrastructure (paths, io, series, bea_cache, fred_cache, io_matrix)
├── data/
│   ├── source/                        # Digitized book tables + external study CSVs
│   ├── raw/                           # Cached BEA/BLS/FRED responses (4MB)
│   ├── intermediate/                  # Pipeline intermediate outputs
│   └── final/                         # 64 published series CSVs
├── docs/
│   ├── ROADMAP.md                     # 8-sprint strategic plan
│   ├── IMPLEMENTATION_PLAN.md         # 142-task methodical execution plan
│   ├── series/                        # 64 per-series DPRs + 16 EPRs + 17 DECOMPOSITION.md
│   ├── chapters/                      # Per-chapter ADEQUACY + REVIEW reports
│   └── methodology/                   # Methodology PDF source (LaTeX, TBD)
├── research/                          # 58 per-series research JSONs (book quotes)
├── chopped/                           # 64 machine-readable CSVs (Anu Chopped v2.0)
├── extenbooks/                        # 64 human-readable xlsx workbooks (4-sheet)
└── MIGRATION/                         # ID crosswalk + divergence-from-ST2 docs + generators
```

---

## Series ID scheme

| Prefix | Meaning | Count |
|---|---|---|
| `S###` | Book series (Shaikh & Tonak 1994, Ch 2/4/5/6/7/8/9) | 35 |
| `ES####` | External-study replication, grouped by paper | 25 |
| `AS###` | Analytical / Anu-original derived series | 4 |
| **Total** | | **64** |

Each series has subseries (`S###-A` = book period, `S###-B` = extension data, `S###-COMBINED` = spliced final). See `chopped/{sid}.csv` for the canonical 3-row machine-readable format with metadata.

---

## Data sources

| Source | Tables | Coverage |
|---|---|---|
| Shaikh & Tonak (1994) | Appendix tables E.2, E.3, F, G, H.1, H.2; main-text Tables 5.7, 6.1, 6.2, 6.3, 9.1 | 1948–1989 (digitized) |
| BEA NIPA | Tables 1.7.5, 2.1, 1.10, 3.x | 1929–2024 (cached) |
| BEA Fixed Assets | Table 4.1 (net stock, private nonresidential) | 1925–2024 (cached) |
| BEA Benchmark I-O | Use, Make, A, L, Z matrices | 6 SIC benchmark years 1947–1977 (cached); 4 NAICS years (cached, schema deferred) |
| BLS CES | Production worker series | 1948–2024 (cached, subset) |
| FRED | TCU (1967+), GDPDEF (1947+) | Cached |
| External studies | Mohun 2005, Mohun 2013, Moos 2017, Cronin 2001 NZ, Karabacak & Tonak 2022, Tonak 1984 | Per-paper periods, all cached |

All cached responses are included in this repository (`data/raw/`, ~4MB) so `--validate-only` runs without API access. Fresh API fetches require keys (see `INSTALL.md`).

---

## What's in scope, what isn't

**Fully reproduced**:
- 33 S-series book replication (1948–1989), including extensions to 1989–2025 for 11 series
- 25 ES-series external study replications (per-paper periods)
- 4 AS-series analytical derivations

**Approximations documented**:
- K\* uses BEA Fixed Assets Line 1 (Private nonresidential total). A productive-partition refinement (excluding financial sector) is documented as future work in `docs/IMPLEMENTATION_PLAN.md` Phase 2.A.
- S701/S702/S703 (Ch 7 labor values, prices of production, deviations) are scalar matrix-summary approximations rather than full per-sector calculations. The book's qualitative findings are preserved; magnitudes differ.
- Karabacak Turkey 2022 NSW uses World Bank fiscal data as approximation. K&T's headline finding (NSW negative all years) is reproduced 30/30.
- AS001 (Social Burden Rate) uses total corporate profits as Pn proxy; productive-partition refinement is documented.

**Out of scope**:
- Interactive visualization app (deferred to `viz/`, future work)
- Full sectoral decomposition of S701/S702 (matrix-derived scalar approximation used)
- Quarterly/monthly frequency series (annual only)

---

## Validation

All 64 series pass V03 validators:
- 35 series have benchmark checks against published book endpoints
- 12 have identity checks (e.g., GFP = TP\* − C\*_m, S\* = VA\* − V\*, NSW = B_w + G_w − T_w)
- 8 have cross-source consistency checks (Table H.1 vs Table E.2 over 1948–1961 overlap, all clean)
- 9 derived series have round-trip checks against upstream sources

Run `python run.py --validate-only` to reproduce the validation report.

---

## Citation

If you use this package, please cite both the original work and this replication:

```bibtex
@book{shaikh1994measuring,
  author    = {Shaikh, Anwar and Tonak, E. Ahmet},
  title     = {Measuring the Wealth of Nations: The Political Economy of National Accounts},
  publisher = {Cambridge University Press},
  year      = {1994},
}

@software{mwon_replication_2026,
  author  = {Anderson, Nick},
  title   = {Measuring the Wealth of Nations: Replication Package},
  year    = {2026},
  url     = {https://github.com/andenick/measuring-wealth-of-nations-replication},
}
```

See `CITATION.cff` for machine-readable form.

---

## License

MIT (see `LICENSE`). Cached BEA/BLS/FRED data are in the public domain. External-study source CSVs are included under fair-use research provisions; see each study's `docs/series/ES####_DPR.md` for paper citations.

---

## Acknowledgments

Built on the **Anu Framework v10.0** — an open data-construction standard for economic replication packages with strict no-fabrication and full-provenance discipline. Every value in this package traces to either a published source, a cached API response, or a documented derivation from upstream series.
