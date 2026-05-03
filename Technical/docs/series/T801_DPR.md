# T801 — Cross-Study Comparison (ST vs Mohun)

## Quick Reference

| Field | Value |
|-------|-------|
| Series ID | T801 |
| Chapter | 8 |
| Book Table | 8.1 |
| Period | 1948-1989 |
| Units | mixed (rates, shares) |
| Status | wave3_planned |

## Source Context

Chapter 8 compares Shaikh-Tonak's estimates with alternative studies (Moseley, Wolff, Mohun). T801 contains the comparison table with exploitation rates from different classification methods.

## Subsources

- **T801-A**: Compiled from Mohun exploitation rates (L13) and AS2 T506 series.

## Transformation Chain

1. L13 loads Mohun exploitation rates and comparison data
2. P15 outputs ST vs Mohun exploitation rate comparison (42 years)

## Validation

- V09 Mohun cross-validation: systematic divergence confirmed (42-80%, expected)
- Mean ST/Mohun ratio: 1.61 (via N1404)
