# AS2 - Shaikh & Tonak (1994) Replication and Extension Package

**Complete replication and extension of every empirical claim in Shaikh & Tonak's *Measuring the Wealth of Nations* (1994)**

---

## Quick Start

```bash
cd Technical/NickyData
pip install -r requirements.txt
# Set API keys in data/user-inputs/api_keys.env (BEA_API_KEY, BLS_API_KEY)
python run.py --test-all    # Full pipeline + verification (~100s)
```

## Key Findings

| Measure | 1948 | 1989 (book) | 2024 (extended) | Change |
|---------|------|-------------|-----------------|--------|
| Rate of exploitation (e = S*/V*) | 1.70 | 2.44 | ~3.59 | +111% |
| Productive labor share (Lp/L) | 0.57 | 0.36 | ~0.25 | -56% |
| Productive wage share (V*/W) | 0.54 | 0.36 | ~0.24 | -56% |
| Net social wage | Negative | Negative | Negative | 92% of years |
| Labor value / price R^2 | 0.98 (1958) | — | — | Shaikh claim confirmed |

## What This Is

AS2 (Anu Shaikh-Tonak 2) is a fully automated NickyData pipeline that reproduces 55 data series from Shaikh & Tonak (1994), extends them through 2024, and replicates 8 related academic studies. Everything runs from a single command with zero manual intervention.

### Pipeline Architecture (NickyData v6.0)

```
S## Setup (2)  -->  Environment validation, ledger generation
L## Loading (15) --> Parse source CSVs, fetch API data
P## Processing (20) --> Compute all 55 series with dependency ordering
V## Validation (15) --> 348 automated checks, 0 failures
M## Manual Adj (3) --> K->K* profit rate, ec_u/ec_p ratio corrections
A## Analysis (6) --> Cross-study comparisons, sensitivity analysis
O## Output (6) --> 11 figures, master database, chopped CSVs, extenbooks
E## Exploration (1) --> Wave 3 investigation
```

**67 scripts | 55 series | 15 validators | ~100 seconds**

### Coverage

| Chapter | Series | Content | Status |
|---------|--------|---------|--------|
| Ch 2 | T201 | Orthodox GDP comparison | Calculated |
| Ch 4 | T401-T402 | IO A-matrix + Leontief inverse (11 benchmarks) | Benchmark-only |
| Ch 5 | T501-T516 | Exploitation accounting (16 series, 1948-2024) | Extended |
| Ch 6 | T601-T609 | Net social wage (9 series, 1952-2025) | Extended |
| Ch 7 | T701-T703 | Labor values + prices of production (R^2=0.70-0.98) | Calculated |
| Ch 8 | T801 | Cross-study comparison (ST vs Mohun) | Calculated |
| Ch 9 | T901 | Summary indicators | Assembled |
| Studies | N1001-N1701 | 8 external papers, 22 series (US/Turkey/NZ) | Calculated |

### External Studies Replicated

1. Tonak (1984) — Workers as net subsidizers of the state
2. Shaikh & Tonak (1987) — "Social wage" is a myth
3. Shaikh & Tonak (2002) — NSW through Clinton era
4. Moos (2017) — Post-2000 structural shift (+3.0pp)
5. Mohun (2005) — Alternative classification (ST/Mohun ratio = 1.61)
6. Mohun (2013) — Class decomposition (81.3% working class)
7. Karabacak & Tonak (2022) — Turkey NSW negative ALL 40 years
8. Cronin (2001) — New Zealand post-reform shift

## Project Structure

```
ST2/
  Inputs/               # Read-only source data (book tables, IO matrices, API data)
  Technical/
    NickyData/           # Self-contained pipeline
      run.py             # Master orchestrator
      code/              # 67 scripts across 8 phases (S/L/P/V/M/A/O/E)
      utils/             # Shared libraries (fetchers, formatters, transforms)
      data/              # Raw, final, and adjusted data
      *.json             # Registries, configs, ledger
    docs/                # 61 DPRs, 28 EPRs, 17 FPRs, decompositions
    Knowledge_Base/      # HDARP book extractions (380 pages, 40 chunks)
    ShinyApp/            # R Shiny interactive visualization
    Handoffs/            # Session handoff documentation
  Outputs/
    Data/                # Master database (97yr x 48 series, CSV + XLSX)
    Figures/             # 11 publication-quality figures (PNG + SVG)
    Reports/             # LaTeX methodology report (PDF)
```

## Anu Suite Compliance

| Artifact | Count | Standard |
|----------|-------|----------|
| Chopped CSVs | 49 | Anu Chopped v1.0 (Row 1 metadata, Row 2 IDs) |
| Extenbooks | 50 | Anu Extenbook v3.0 (4 sheets: Data/Provenance/Research/Construction) |
| DPRs | 61 | Anu Ingestion v3.0 |
| EPRs | 28 | Anu Extension v3.0 |
| FPRs | 17 | Anu Standard v2.2 |
| Validators | 15 (348 checks) | Anu Replicator v2.0 (V## phase) |
| Variants | 6 documented | Anu Variant v1.0 |
| Ledger | 50/55 covered | Anu Ledger v2.0 |

## Source Book

Shaikh, A. & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press.

## Technology Stack

- **Python 3.11+**: Pipeline, data processing, API fetching
- **R 4.x**: Shiny interactive visualization
- **APIs**: BEA, BLS, FRED
- **Standards**: Druck workspace, Anu Suite v5.0, NickyData v1.1

---

*Part of the Arcanum research workspace. Last updated: May 3, 2026.*
