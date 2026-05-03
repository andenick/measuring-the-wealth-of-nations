# Chapter 14 Investigation: Mohun (2005) — Measuring Wealth 1964-2001

## Paper Metadata

| Field | Value |
|-------|-------|
| Author | Simon Mohun |
| Title | On measuring the wealth of nations: the US economy, 1964-2001 |
| Year | 2005 |
| Journal | Cambridge Journal of Economics 29(5): 799-815 |
| Period | 1964-2001 |
| HDARP Location | `external_papers/productive_labor/2005_Mohun_US_1964_2001/` |
| CSV Data | `Inputs/ExternalSources/Mohun/` (13 files) |

## Significance

Mohun's key contribution: a MORE RESTRICTIVE productive labor classification that produces LOWER exploitation rates than Shaikh-Tonak. The comparison reveals how classification choices affect Marxian measures.

## Existing Data Files (already in ST2)

| File | Content | Columns |
|------|---------|---------|
| mohun_exploitation_rates_1948_1989.csv | Exploitation rates | year, Lp_mohun, Hp, Y, lambda_m, V_star_mohun, V_star_hours, S_star, e_mohun |
| mohun_employment_annual_1948_1989.csv | Employment | year, L, Lp_mohun, Lp_mohun_L_ratio, Lu_mohun |
| mohun_variable_capital_1948_1989.csv | Variable capital | Multiple V* variants |
| mohun_vs_st_employment_comparison.csv | Direct comparison | ST vs Mohun employment |
| mohun_vs_st_variable_capital_comparison.csv | Direct comparison | ST vs Mohun V* |
| detailed_exploitation_comparison_ST_vs_Mohun.csv | Full comparison | Side-by-side all metrics |

## Series to Replicate

| ID | Name | Source File | Period |
|----|------|-----------|--------|
| N1401 | Mohun Exploitation Rate | mohun_exploitation_rates*.csv, col e_mohun | 1964-2001 |
| N1402 | Mohun Productive Labor | mohun_employment*.csv, col Lp_mohun | 1964-2001 |
| N1403 | Mohun Variable Capital | mohun_variable_capital*.csv | 1964-2001 |
| N1404 | ST vs Mohun Ratio | detailed_exploitation_comparison*.csv | 1964-1989 |

## Implementation

This is the EASIEST chapter — CSV data already exists. Just need:
1. Create L## script to load existing CSVs
2. Create P## script to formalize as pipeline series
3. Generate chopped CSVs and extenbooks
4. V09 already provides cross-validation
