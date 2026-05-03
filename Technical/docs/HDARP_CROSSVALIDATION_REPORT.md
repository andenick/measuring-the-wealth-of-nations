# HDARP Cross-Validation Report
## AS2 Chopped CSVs vs. Book Table Extractions

**Date**: 2026-04-09
**Source**: `HDARP_Extractions/1994_Measuring_Wealth/` (40 chunks, 35 table files)

---

## Summary

Cross-validated key AS2 series against HDARP-extracted book tables. All benchmark values match exactly.

## Results

### Table 5.7 Cross-Validation (Exploitation Rate & Composition)

| Series | Measure | Year | Book Value | AS2 Value | Diff | Status |
|--------|---------|------|-----------|-----------|------|--------|
| T506 | S*/V* | 1948 | 1.70 | 1.7000 | 0.0% | PASS |
| T506 | S*/V* | 1989 | 2.44 | 2.4400 | 0.0% | PASS |
| T511 | Lp/L | 1948 | 0.57 | 0.5700 | 0.0% | PASS |
| T511 | Lp/L | 1989 | 0.36 | 0.3600 | 0.0% | PASS |
| T512 | V*/W | 1948 | 0.54 | 0.5400 | 0.0% | PASS |
| T512 | V*/W | 1989 | 0.36 | 0.3600 | 0.0% | PASS |

### Additional Book Values Not Yet in V01 Benchmarks

From Table 5.7 HDARP extraction:
- C*/V* 1948=2.35, 1989=2.89 (value composition — corresponds to T510 but may differ in scope)
- S*_real 1948=$635.36B, 1989=$2,330.44B (real 1982$ — not directly comparable to nominal T505)
- V*_real 1948=$344.01B, 1989=$928.71B (real 1982$ — not directly comparable to nominal T504)

### Tables Available for Future Cross-Validation

| Chunk | Table | Content | Wave 1 Series |
|-------|-------|---------|---------------|
| 11 | 4.1 | Labor/money value measures | Framework reference |
| 11 | 4.2 | Numerical example | Verification of formulas |
| 11 | 4.3 | Inconsistent mapping | Wolff error documentation |
| 11 | 4.4 | Rates of exploitation | T506 methodology |
| 13 | 5.4 | Continuation summary | T501-T503 trends |
| 13 | 5.5 | Employment summary | T515-T516 |
| 14 | 5.6 | Wages summary | T504, V* |
| 14 | 5.7 | Surplus value summary | T505, T506, T510-T512 |
| 15 | 5.8-5.9 | Summary tables | Multiple series |
| 16 | 5.10-5.11 | Additional tables | T513-T514 (profit rates) |
| 17 | 5.12-5.14 | Price-value, comparison | T201, cross-validation |

## Conclusion

All validated benchmark values match exactly (0.0% deviation). The AS2 data construction is faithful to the book's published values for the key exploitation, labor share, and wage share series.

**Remaining opportunity**: Extract numerical values from Tables 5.5-5.11 (currently in markdown summary format in the HDARP extraction) to add to validation_config.json benchmark_validation.
