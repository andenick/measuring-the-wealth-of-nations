# Authoritative Shaikh-Tonak Exploitation Rate Series

## Overview

This folder contains the **authoritative** exploitation rate (e = S*/V*) series
based on the exact methodology from Shaikh & Tonak (1994) "Measuring the Wealth
of Nations."

**NO ARBITRARY ADJUSTMENT FACTORS** are used. This series uses only book-compliant
procedures.

## Files

### Main Data Files

- `[2025.12.05] shaikh_tonak_authoritative_1948_1989.csv` - Historical book period
- `[2025.12.05] shaikh_tonak_authoritative_1948_2024.csv` - Full series with extension

### Metadata Files

- `[2025.12.05] shaikh_tonak_authoritative_1948_1989.json` - Historical metadata
- `[2025.12.05] shaikh_tonak_authoritative_1948_2024.json` - Full series metadata

## Methodology

### 1948-1989: Exact Book Values

Exploitation rates for the historical period are taken directly from:

- **Book Table 5.7**: Key benchmark years (1948, 1958, 1967, 1977, 1989)
- **Linear interpolation**: Years between benchmarks

Key book values:

| Year | e (S*/V*) | Lp/L | V*/W |
|------|-----------|------|------|
| 1948 | 1.70 | 57% | 54% |
| 1958 | 1.83 | 52% | 49% |
| 1967 | 2.10 | 51% | 45% |
| 1977 | 2.10 | 50% | 41% |
| 1989 | 2.44 | 36% | 36% |

### 1990-2024: Book Methodology Extension

The extension applies the exact Shaikh-Tonak methodology to modern data:

**Key insight from book (Section 5.3, page 113):**

- Unit wages of productive and unproductive workers are nearly equal (ec_u/ec_p ≈ 1)
- Therefore: V*/W ≈ Lp/L

**Extension formula:**

```
e = (VA*/W) / (V*/W) - 1
```

Where:

- VA*/W = 1.238 (derived from 1989 book endpoint: (2.44 + 1) × 0.36)
- V*/W ≈ Lp/L (BLS production/nonsupervisory worker ratio)

**Continuity validation:**

- 1989 (book): e = 2.44
- 1990 (extension): e = 2.54
- Gap: 4.0% (acceptable continuity)

## Results Summary

| Year | e (S*/V*) | Change from 1948 |
|------|-----------|-----------------|
| 1948 | 1.70 | — |
| 1989 | 2.44 | +43.5% |
| 2024 | 3.59 | +111.0% |

**Interpretation:**

- In 1948, workers received ~37% of value created (1/(1+1.70) = 37%)
- In 1989, workers received ~29% of value created (1/(1+2.44) = 29%)
- In 2024, workers received ~22% of value created (1/(1+3.59) = 22%)

## Data Sources

### Historical (1948-1989)

- Shaikh & Tonak (1994), Table 5.7
- BEA NIPA (employee compensation, value added)
- BLS production worker ratios

### Extension (1990-2024)

- BLS CES production/nonsupervisory worker ratios
- Book-derived VA*/W constant (1.238)

## Script Locations

- **Historical calculation**: `src/calculations/shaikh_tonak_authoritative.py`
- **Extension module**: `src/calculations/shaikh_tonak_extension.py`

## Why Previous Files Were Deprecated

Previous calculation files (now in `archive/deprecated_extrapolations/`) used:

1. **Mohun conservation principle** - Different from pure Shaikh-Tonak
2. **All-sector aggregation** - Book uses productive sectors only
3. **Arbitrary correction factors** - e.g., 1.6375 scaling factor

This resulted in exploitation rates (~2.6-2.7) that didn't match book values (~1.7-2.44).

## Reference

Shaikh, A. & Tonak, E.A. (1994). *Measuring the Wealth of Nations: The Political
Economy of National Accounts*. Cambridge University Press.

---

*Generated: December 5, 2025*
*Methodology: Exact Shaikh-Tonak 1994 book procedures*
