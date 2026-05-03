# Unit Audit Report
## Dollar-Denominated Series in AS2

**Date**: 2026-04-09

---

## Findings

### Source Data Units

| Series | Source | Chopped CSV Unit | L## Conversion | Final Unit | 1948 Value |
|--------|--------|-----------------|----------------|------------|------------|
| T501 (TP*) | Table E.2 | billions | none | **billions** | 446.21 |
| T502 (C*m) | Table E.2 | billions | none | **billions** | 198.47 |
| T503 (GFP*) | Table E.2 | billions | none | **billions** | 247.74 |
| T504 (V*) | Table 5.7 | thousands | ÷1000 | **millions** | 1,294.16 |
| T505 (S*) | Table 5.7 | thousands | ÷1000 | **millions** | 1,673.14 |
| T508 (CON*) | Table E.2 | billions | none | **billions** | 158.46 |
| T509 (IG*) | Table E.2 | billions | none | **billions** | 44.27 |
| T601-T604 | Table 6.1 | thousands | ÷1000 | **billions** | 22-53 |
| T605-T606 | Table 6.2 | thousands | ÷1000 | **billions** | 11-33 |
| T607 (NSW) | Derived | thousands | ÷1000 | **billions** | -9.52 |

### Unit Groups
- **Billions (from Table E.2)**: T501, T502, T503, T508, T509
- **Millions (from Table 5.7)**: T504, T505
- **Billions (from Ch6 tables)**: T601-T607
- **Ratios**: T506, T507, T510, T511, T512, T513, T514, T608, T609

### Key Finding

T501-T503 (Total Product, Constant Capital, GFP) are in **billions** from Table E.2.
T504-T505 (Variable Capital, Surplus Value) are in **millions** from Table 5.7.

These come from **different accounting pathways** in the book:
- Table E.2 gives macro aggregates (TP*, C*m, GFP*) in billions
- Table 5.7 gives labor-derived measures (V*, S*, e) from NIPA employee compensation data in millions

The identity GFP* = V* + S* holds conceptually but the published values use different unit bases because they're computed from different source tables.

### Implication for Cross-Series Validation

V05's identity checks (T505 = T501 - T504, T506 = T505/T504) cannot hold across these series because:
1. T501 (billions) and T504 (millions) differ by ~1000x
2. T505 and T504 are in the same units (both millions), so T506 = T505/T504 IS valid
3. T505 ≠ T501 - T504 because they use different accounting pathways

The current V05 configuration correctly handles this: T505=T501-T504 is SKIP'd, T506=T505/T504 uses wide tolerance.

### Implication for DIV-001 (K→K*)

The profit rate r* = S*/K requires S* and K to be in the same units:
- T505 (S*) is in millions
- BEA Fixed Assets (K) is in millions (UNIT_MULT=6)
- So the ratio should work IF both are in millions

But the L02 comment says "÷1000 → billions" which is incorrect — the output is millions, not billions. The M02 script needs to use K in millions (not ÷1e3 to billions).

### Recommended Fix for M02

Change `k_total_b = k_total / 1e3` to `k_total_m = k_total` (keep in millions) since T505 is also in millions.

---

*This audit resolves the confusion about "Step 1: Unit Normalization." The series are actually internally consistent within their source-table groups — the issue was incorrect documentation, not incorrect data.*
