# NickyData v7.2 — Marxian National Accounts from Public Data

Computes the complete Marxian national accounting framework for the US economy (1948-2024) using only public BEA, BLS, and FRED data.

**Methodology**: Shaikh & Tonak (1994) *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press.

## Accuracy

At all benchmark years (1948, 1958, 1967, 1972, 1977, 1980, 1985, 1989):
- V* (variable capital): **exact match** to book Table H.1
- e (exploitation rate): within **0.3%** of book at all benchmarks
- e trajectory: correctly **RISING** from 1.70 (1948) to 2.44 (1989)

Extension (1997-2024) uses 412-industry detail BEA data. Post-book finding:
e peaks at 2.44 (1989), then declines to 1.26 (2024) as the productive sector shrinks.

## Quick Start

```bash
pip install -r requirements.txt

# Add your API keys
export FRED_API_KEY=your_key_here    # https://fred.stlouisfed.org/docs/api/
export BEA_API_KEY=your_key_here     # https://apps.bea.gov/API/signup/

# Run the pipeline (~5 seconds with cached data, ~30s first run)
python -m nickydata.run
```

## What It Computes

| Series | Content | Years |
|--------|---------|-------|
| T501-T503 | Total product (TP*), constant capital (C*m), gross final product (GFP*) | 1948-2024 |
| T504-T505 | Variable capital (V*), surplus value (S*) | 1948-2024 |
| T506-T507 | Exploitation rate (e = S*/V*), surplus ratio | 1948-2024 |
| T511-T516 | Productive labor share, wage share, employment | 1939-2024 |
| T513-T514 | Marxian profit rate (r* = S*/K*), capacity-adjusted | 1948-2024 |
| T601-T609 | Net social wage (taxes, benefits, NSW) | 1952-2024 |
| A07-A10 | Social burden rate, unproductive exploitation, Marxian productivity | 1948-2024 |

## Data Sources (all public, all fetched automatically)

- **BEA UnderlyingGDPbyIndustry**: 412-industry detail gross output + value added (1997-2024)
- **BEA NIPA**: GDP, compensation by industry, government, social benefits (13 tables)
- **BEA IO**: Input-output Use tables, 71 sectors, annual 1997-2024
- **BEA Fixed Assets**: Capital stock (Table 4.1)
- **FRED**: Employment (PAYEMS), GDP deflator, depreciation (COFC), capacity utilization (TCU)
- **BLS CES**: Production worker ratios and wages by sector (via FRED mirrors)
- **Book Table H.1**: Digitized benchmark values for 1948-1989 (included)

## Architecture

```
nickydata/
  config/
    methodology.json    # All formulas, parameters, sector classifications
    api_sources.json    # API endpoints (optional, for reference)
  fetch/                # Data fetchers with caching
  compute/              # Marxian accounting computations
  validate/             # Output validation checks
  output/               # Database and figure generation
  run.py                # Pipeline orchestrator
  data/                 # Cached API responses + computed output (gitignored)
```

## Methodology

The pipeline implements the Shaikh & Tonak (1994) framework:

1. **Classify sectors** as productive (create use values), trading (circulate use values), or unproductive (transfer surplus)
2. **Compute total product** TP* from gross output of productive + trading sectors
3. **Compute variable capital** V* from wages of production workers in productive sectors
4. **Derive surplus value** S* = TP* - C*m - V* (total product minus materials minus wages)
5. **Compute exploitation rate** e = S*/V*
6. **Compute net social wage** NSW = benefits - taxes on workers
7. **Compute profit rate** r* = S*/K* (surplus value / productive capital stock)

All formulas documented in `config/methodology.json`.
