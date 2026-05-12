# Measuring the Wealth of Nations — Replication Package

**Complete replication and extension of every empirical claim in Shaikh & Tonak's *Measuring the Wealth of Nations* (1994), with 59 data series covering 1948–2024.**

---

## Key Findings

| Measure | 1948 | 1989 (book) | 2024 (extended) | Change |
|---------|------|-------------|-----------------|--------|
| Rate of exploitation (e = S\*/V\*) | 1.70 | 2.44 | ~3.59 | +111% |
| Productive labor share (Lp/L) | 0.57 | 0.36 | ~0.33 | -42% |
| Productive wage share (V\*/W) | 0.54 | 0.36 | ~0.27 | -50% |
| Net social wage | Negative | Negative | Negative | 92% of years |
| Marxian profit rate (r\* = S\*/K\*) | 1.87 | 0.44 | ~0.39 | Falling trend confirmed |
| Labor value / price R-squared | 0.93 (1958) | 0.79 (1977) | 0.85–0.99 (NAICS) | Strong correlation |

The exploitation rate — the ratio of surplus value to the wages of productive workers — more than doubled over the postwar period. The net social wage is negative in 92% of years, meaning workers pay more in taxes than they receive in government benefits. The Marxian profit rate shows a secular decline, consistent with the classical prediction.

---

## Quick Start

```bash
git clone https://github.com/andenick/measuring-the-wealth-of-nations.git
cd measuring-the-wealth-of-nations/Technical/NickyData
pip install -r requirements.txt

python run.py --validate-only   # Verify all 59 series against benchmarks (2 seconds)
python run.py --test-all        # Full pipeline: fetch data, compute, validate (~15 seconds)
```

API keys are needed only for `--test-all` (which re-fetches data from BEA, BLS, and FRED). The `--validate-only` mode works immediately with the cached data included in the repository.

See [INSTALL.md](INSTALL.md) for API key setup and troubleshooting.

---

## What This Replicates

Shaikh and Tonak (1994) reconstruct the US national accounts from a Marxian perspective. They distinguish *productive* labor (which creates surplus value) from *unproductive* labor (administration, finance, government), and show that orthodox national accounting systematically conflates the two. Their framework produces measures — the rate of exploitation, the Marxian profit rate, the net social wage — that differ substantially from conventional statistics and reveal the class structure of the American economy.

This package:

1. **Replicates** every table and figure from Chapters 2, 4–9 of the book (33 T-series, 1948–1989)
2. **Extends** all extendable series through 2024 using BEA, BLS, and FRED public data
3. **Replicates 8 related studies** that build on the Shaikh-Tonak framework (25 N-series):
   - Tonak (1984) — Workers as net subsidizers of the state
   - Shaikh & Tonak (1987) — "Social wage" is a myth
   - Shaikh & Tonak (2002) — NSW through the Clinton era
   - Moos (2017) — Post-2000 structural shift (+3.0 pp)
   - Mohun (2005) — Alternative productive/unproductive classification
   - Mohun (2013) — Class decomposition (81.3% working class)
   - Karabacak & Tonak (2022) — Turkey: NSW negative for ALL 40 years
   - Cronin (2001) — New Zealand post-reform shift

4. **Computes 4 analytical series**: social burden rate, unproductive exploitation rate, Marxian productivity, and Khanjian cross-validation

Everything runs from a single command with zero manual intervention.

---

## Data Sources

All data used in this project is publicly available:

| Source | Tables | Coverage | Access |
|--------|--------|----------|--------|
| BEA NIPA | 1.7.5, 2.1, 3.1–3.3, 6.2D, 6.5D | 1929–2025 | [Free API key](https://apps.bea.gov/API/signup/) |
| BEA Fixed Assets | Table 4.1 (net stock by industry) | 1925–2024 | Same API key |
| BEA GDP-by-Industry | Value added, components by industry | 1997–2024 | Same API key |
| BEA Input-Output | Benchmark Use/Make tables | 1947–2017 | [Public download](https://www.bea.gov/industry/input-output-accounts-data) |
| BLS CES | Production workers by industry | 1948–2024 | [Free API key](https://data.bls.gov/registrationEngine/) |
| FRED | Capacity utilization, Turkey labor share | 1948–2024 | [Free API key](https://fred.stlouisfed.org/docs/api/api_key.html) |
| Book tables | Appendices E, F, G, H (digitized) | 1948–1989 | Included in this repo |
| TurkStat | Compensation of employees (HDARP-extracted) | 1980–2006 | Included in this repo |

Cached API responses are included in `data/raw-data/`, so the pipeline can run without API keys in validation mode.

---

## Repository Structure

```
measuring-the-wealth-of-nations/
  Inputs/                    Source data
    BookTables/              Digitized tables from the book
    ST_Chopped/              Book data in structured CSV format
    Concordances/            SIC-NAICS sector classification mappings
    ExternalSources/         Data for the 8 replicated studies

  Technical/
    NickyData/               Self-contained pipeline (run.py + 85 scripts)
      run.py                 Master orchestrator
      code/                  Scripts organized by phase (S/L/P/V/M/A/O/E)
      utils/                 Shared libraries (API fetchers, data transforms)
      data/                  Raw inputs, cached API data, computed outputs
      series_registry.json   Canonical registry of all 59 series
      validation_config.json Benchmark values and tolerance thresholds

    docs/                    Data provenance documentation
      series/                Per-series provenance records (58 files)
      figures/               Per-figure provenance records (17 files)
      chapters/              Chapter-level review reports

    Knowledge_Base/          Text extracted from the book (380 pages)
    ShinyApp/                Interactive R Shiny visualization (15 tabs)

  Outputs/
    Data/                    Master database (97 years x 48 series, CSV + Excel)
    Figures/                 11 publication-quality figures (PNG + SVG)
    Reports/                 Methodology report (LaTeX/PDF)
```

---

## Pipeline Architecture

The pipeline has 8 phases, each containing numbered scripts that run in order:

| Phase | Scripts | What it does |
|-------|---------|--------------|
| **S** Setup | S01–S05 | Validate environment, generate artifact registry and provenance index |
| **L** Loading | L01–L22 | Parse source CSVs, fetch data from BEA/BLS/FRED APIs |
| **P** Processing | P01–P23 | Compute all 59 series with correct dependency ordering |
| **V** Validation | V01–V15 | 348 automated checks against book benchmarks |
| **M** Manual Adj | M01–M04 | Documented adjustments (K-to-K\* correction, ec_u/ec_p ratios) |
| **A** Analysis | A01–A11 | Cross-study comparisons, sensitivity analysis, period decomposition |
| **O** Output | O01–O08 | Figures, master database, structured CSVs, Excel workbooks |
| **E** Exploration | E01 | Investigative analysis |

**85 scripts | 59 series | 15 validators | 348 checks | 0 failures**

---

## Series Coverage

| Chapter | Series | Content | Period |
|---------|--------|---------|--------|
| Ch 2 | T201 | Orthodox vs Marxian GDP comparison | 1948–1989 |
| Ch 4 | T401–T402 | Input-output A-matrix + Leontief inverse (11 benchmarks) | 1947–2017 |
| Ch 5 | T501–T516 | Exploitation accounting: TP\*, V\*, S\*, e, Lp/L, V\*/W, r\* | 1948–2024 |
| Ch 6 | T601–T609 | Net social wage: taxes, benefits, NSW, NSW/V\* | 1952–2025 |
| Ch 7 | T701–T703 | Labor values, prices of production, value-price deviations | 1947–2017 |
| Ch 8 | T801 | Cross-study comparison (Shaikh-Tonak vs Mohun) | 1948–1989 |
| Ch 9 | T901 | Summary indicators | 1948–2024 |
| Studies | N1001–N1704 | 8 external papers, 25 series (US, Turkey, New Zealand) | Various |

---

## Validation

Every series is verified against the book's published values. The 15 validators cover:

| Validator | What it checks |
|-----------|---------------|
| V01 | 31 reference values from the book (exact match within tolerance) |
| V02 | Range checks on all 59 series (no impossible values) |
| V03 | Year-to-year continuity (no unexplained jumps) |
| V04 | Completeness (no missing years in expected ranges) |
| V05 | Cross-series identities (e.g., GFP\* = TP\* - C\*m) |
| V06 | Splice quality at book/extension transition (1989–1990) |
| V07 | Overlap correlation between book and extension data |
| V08 | Hash integrity (data files unchanged since last validation) |
| V09 | Cross-validation against Mohun (2005) estimates |
| V10 | Input-output matrix consistency |
| V11 | External benchmark comparison |
| V12 | Net social wage cross-study consistency |
| V13–V15 | Unit consistency, data freshness, Robin cross-validation |

---

## Data Format

Series data is stored in the [Anu Data Architecture](https://github.com/andenick/anu-suite) format:

- **CSV files** with structured metadata headers (Row 1: descriptions, Row 2: column IDs, Row 3+: data)
- **Excel workbooks** with 4 sheets per series: Data, Provenance, Research, Construction
- **Provenance records** documenting the source, methodology, and construction steps for every series

The `series_registry.json` file is the canonical definition of all 59 series — every output format reads from this single source of truth.

---

## Citation

```bibtex
@book{shaikh1994measuring,
  author    = {Shaikh, Anwar and Tonak, E. Ahmet},
  title     = {Measuring the Wealth of Nations: The Political Economy of National Accounts},
  publisher = {Cambridge University Press},
  year      = {1994}
}
```

See [CITATION.cff](CITATION.cff) for this replication package's citation metadata.

---

## Requirements

- **Python 3.11+** — pipeline, data processing, API fetching
- **R 4.x** (optional) — Shiny interactive visualization only
- **APIs** — BEA, BLS, FRED (free registration, see [INSTALL.md](INSTALL.md))
- **Disk** — ~50 MB (repo) + ~200 MB (computed outputs)
- **Time** — ~15 seconds for full pipeline run
