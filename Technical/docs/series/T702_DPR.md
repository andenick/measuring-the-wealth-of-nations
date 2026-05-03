# T702 — Prices of Production

## Quick Reference

| Field | Value |
|-------|-------|
| Series ID | T702 |
| Chapter | 7 |
| Book Table | 7.2 |
| Period | 1947-1977 (6 SIC benchmark years) |
| Units | dollars (total sector values) |
| Status | calculated |

## Source Context

Prices of production pp_j = (1 + r̄)(C_j + V_j) represent the theoretical equilibrium prices under uniform profit rates across sectors. The book shows these are highly correlated with labor values across sectors (R² > 0.95 in total-value regression).

## Subsources

- **T702-A**: Computed from Z-matrices, sector classification, and V*/VA* ratio from T507.

## Transformation Chain

1. C_j = column sum of Z-matrix (intermediate inputs to sector j)
2. VA_j = x_j - C_j (value added)
3. V_j = VA_j × (V*/VA*) from book ratio (T507)
4. S_j = VA_j - V_j
5. r̄ = ΣS_j / Σ(C_j + V_j) for productive sectors
6. PP_j = (1 + r̄)(C_j + V_j)

## HDARP Linkage

- IO methodology: `Technical/docs/chapters/IO_METHODOLOGY_EXTRACTION.md`
- Book Section 4.2 (pp.86-88): price transformation formulas
