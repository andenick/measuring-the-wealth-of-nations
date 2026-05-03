# T402 — B-Matrix (Leontief Inverse)

## Quick Reference

| Field | Value |
|-------|-------|
| Series ID | T402 |
| Chapter | 4 |
| Book Table | 4.2 |
| Period | Same benchmarks as T401 |
| Units | matrix (85x85 SIC, 71-sector NAICS) |
| Status | benchmark_only |

## Source Context

B = (I - A)^{-1}, the Leontief inverse. Each element b_ij gives the total (direct + indirect) output from sector i required to produce one unit of final demand in sector j. Used to compute labor values λ* = hp* · B.

## Subsources

- **T402-A**: Derived from T401 via matrix inversion.

## Transformation Chain

1. Load T401 A-matrix
2. Compute B = (I - A)^{-1} via numpy.linalg.inv
3. Verify against book values (deviation logged by P13)

## Validation

- B-matrix deviation from book: exact match (1958), <11 (other years)
- Consistency: B × (I - A) ≈ I verified
