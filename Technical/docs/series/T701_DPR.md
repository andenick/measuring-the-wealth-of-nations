# T701 — Labor Values (λ*)

## Quick Reference

| Field | Value |
|-------|-------|
| Series ID | T701 |
| Chapter | 7 |
| Book Table | 7.1 |
| Period | 1947-1977 (6 SIC benchmark years) |
| Units | labor_hours_per_dollar |
| Status | benchmark_only |

## Source Context

Labor values λ*_j = hp*_j · B_j represent the total (direct + indirect) labor time embodied in one dollar of sector j's output. Computed from the Leontief inverse B = (I-A)^{-1} and direct labor coefficients hp* = hours / gross_output.

## Subsources

- **T701-A**: Computed from L12 (hp* vectors) and L11 (B-matrices) for 6 SIC benchmark years.

## Transformation Chain

1. L12 computes hp*_j = employment_j × avg_hours / gross_output_j for each sector
2. P14 computes λ* = hp* · B for each benchmark year
3. Summary statistics (mean productive sector labor value) interpolated between benchmarks

## Validation

- Cross-validated against KLEMS labor data (T504 correlation = 0.967)
