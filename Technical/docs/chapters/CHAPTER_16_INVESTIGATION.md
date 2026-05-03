# Chapter 16 Investigation: Karabacak & Tonak (2022) — NSW Turkey 1980-2019

## Paper Metadata

| Field | Value |
|-------|-------|
| Authors | Zafer Karabacak, E. Ahmet Tonak |
| Title | The Net Social Wage in Turkey, 1980-2019 |
| Year | 2022 |
| Journal | Review of Radical Political Economics 54(4): 577-605 |
| Period | 1980-2019 (40 years) |
| DOI | 10.1177/04866134221089659 |
| HDARP Location | `external_papers/international/2022_Karabacak_Tonak_NSW_Turkey/` |

## Significance

**Strongest confirmation of Shaikh-Tonak thesis**: NSW is negative for ALL 40 years (100% of observations). No other study achieves this level of consistency. Average NSW = -1.13% GDP.

## HDARP Extraction Quality

Excellent — includes:
- Full transcription
- Equations directory with complete NSW methodology
- Table descriptions with classification taxonomy
- Figures directory

### Key Table: Government Expenditure/Tax Classification

| Category | Components |
|----------|------------|
| E_1 (Direct Benefits to Labor) | Social security, education, social assistance, health |
| E_2 (Mixed Expenditures) | Allocated by labor share |
| E_3 (Direct Benefits to Capital) | Business support, debt service |
| T_1 (Direct Taxes on Labor) | Personal income tax, SSC |
| T_2 (Indirect/Mixed Taxes) | VAT, consumption, property |
| T_3 (Direct Taxes on Capital) | Corporate tax |

## Series to Replicate

| ID | Name | Formula | Period |
|----|------|---------|--------|
| N1601 | Turkey Labor Share | W_p / GDP | 1980-2019 |
| N1602 | Turkey NSW/GDP | (E_1 + α×E_2 - T_1 - β×T_2) / GDP | 1980-2019 |
| N1603 | Turkey Tax Ratio | (T_1 + β×T_2) / GDP | 1980-2019 |
| N1604 | Turkey Benefit Ratio | (E_1 + α×E_2) / GDP | 1980-2019 |
| N1605 | US-Turkey Comparison | N1602 vs T607/GDP | 1980-2019 |

## Benchmark Values

| Statistic | Value |
|-----------|-------|
| Labor Share Mean | 39.7% |
| Labor Share Range | 35-45% (declining) |
| NSW/GDP Mean | -1.13% |
| NSW/GDP Range | -2.5% to -0.2% |
| Tax Ratio Mean | 8.63% GDP |
| Benefit Ratio Mean | 7.50% GDP |
| Negative Years | 40/40 (100%) |

## Data Sources

Turkey-specific data from TURKSTAT and Ministry of Finance (not from BEA/NIPA).
This chapter uses the HDARP-extracted data VALUES directly rather than computing from raw APIs.

## Implementation

1. Extract annual time series from HDARP transcription
2. Create chopped CSVs from extracted data
3. Compute N1605 comparison with US T607 series
4. Validate against benchmark statistics
