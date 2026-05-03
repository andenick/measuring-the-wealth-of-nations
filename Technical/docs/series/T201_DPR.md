# T201 — Alternative GFP Measures (Orthodox Comparison)

## Quick Reference

| Field | Value |
|-------|-------|
| Series ID | T201 |
| Chapter | 2 |
| Book Table | 2.1 |
| Period | 1929-2025 |
| Units | billions_dollars |
| Status | wave3_planned |

## Source Context

Chapter 2 compares Marxian GFP (Gross Final Product) with orthodox GDP. T201 contains conventional national accounts measures (GDP, CFC, NDP) for comparison against T501-T503.

## Subsources

- **T201-A**: BEA NIPA GDP, CFC, NDP. Source: L14 loads from BEA API.

## Transformation Chain

1. L14 loads orthodox GDP/CFC/NDP from BEA NIPA (97 rows, 1929-2025)
2. P15 outputs comparison table

## Validation

- GDP values cross-checked against FRED GDPA series
