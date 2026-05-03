# T703 — Value-Price Deviations

## Quick Reference

| Field | Value |
|-------|-------|
| Series ID | T703 |
| Chapter | 7 |
| Book Table | 7.3 |
| Period | 1947-1977 (6 SIC benchmark years) |
| Units | R², correlation, WAD |
| Status | calculated |

## Source Context

Measures the closeness of labor values and prices of production across sectors. The key empirical claim of Shaikh & Tonak: labor values predict market prices with high accuracy (R² > 0.95 in total-value cross-sectional regressions).

## Subsources

- **T703-A**: Computed from T701 (labor values) and T702 (prices of production).

## Transformation Chain

1. Compute total labor values: Λ_j = λ_j × x_j
2. Compute total prices of production: PP_j from T702
3. Regress log(PP_j) on log(Λ_j) for productive sectors
4. Report R², slope, correlation, Weighted Average Deviation

## Methodology Notes

The total-value regression captures both technology (IO structure) and scale effects. Per-unit regressions yield lower R² because unit labor values have less cross-sectional variation.
