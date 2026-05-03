# T510: Value Composition of Capital (C*/V*) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T510 |
| Type | derived |
| Time Period | 1948-1989 |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | ratio (dimensionless) |
| Validation Status | VALIDATED (book period) |
| Last Updated | 2026-02-24 |

---

## Context

> "The value composition of capital C*/V* is approximately 245% of the conventional capital-labor ratio, reflecting the much larger Marxian measure of material inputs relative to productive wages. From 1948 to 1989, C*/V* rose by 23%, indicating a secular increase in the capital-intensity of production when measured in value terms."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Table 5.14, p. 140

The value composition of capital C*/V* is the Marxian analogue of the capital-labor ratio. It measures the ratio of constant capital (C*, the value of material inputs consumed in production) to variable capital (V*, the wages of productive workers). Unlike the conventional capital-labor ratio, which uses the stock of fixed capital relative to total labor compensation, C*/V* uses the flow of intermediate inputs (materials, energy, depreciation) relative to only productive worker compensation. This distinction yields a ratio approximately 2.45 times larger than the conventional measure (Table 5.14). The secular rise in C*/V* over the postwar period reflects the deepening of capitalist production -- more material inputs per unit of productive labor -- and is a key determinant of the Marxian profit rate via the identity r = S*/(C* + V*) = e/(1 + C*/V*).

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T510A | Derived from T502 (C*) and T504 (V*) | 1948-1989 | N/A (derived) | calculated | C*/V* computed from T502, T504 |
| T510B | ExploitationComposition_1948_1989.csv | 1948-1989 | ST_Chopped/ch05/ExploitationComposition_1948_1989.csv | academic_research | Book data extracted from Table 5.7 |

### Quality Categories
- `academic_research` - Peer-reviewed source (HIGH reliability)
- `calculated` - Derived from formulas (VARIES -- depends on inputs)

### Chopped File Reference
- **File**: ST_Chopped/ch05/ExploitationComposition_1948_1989.csv
- **Content**: Contains value composition alongside exploitation rate, surplus ratio, and labor share for benchmark and interpolated years
- **Columns**: Year, e (S*/V*), S*/(S*+V*), C*/V*, Lp/L, V*/W

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Load C* series | T502 | C* values 1948-1989 | calculate_ch05.py | XFORM-020 |
| 2 | Load V* series | T504 | V* values 1948-1989 | calculate_ch05.py | XFORM-041 |
| 3 | Compute C*/V* | T502, T504 | T510 ratio | calculate_ch05.py | XFORM-101 |
| 4 | Validate against Table 5.7 | T510, book values | pass/fail | validate_ch05.py | XFORM-102 |
| 5 | Compare to conventional ratio | T510, NIPA K/L | Comparison table | validate_ch05.py | XFORM-103 |

### Transformation Details

#### XFORM-101: Value Composition of Capital Calculation

**Formula**:
```
C*/V* = T502 / T504

where:
  C* (T502) = Constant capital (material inputs consumed in production)
            = Intermediate inputs + depreciation of productive fixed capital
            = Sum over productive sectors of:
                intermediate consumption (from IO tables)
              + consumption of fixed capital (NIPA 6.1 productive sectors)

  V* (T504) = Variable capital (compensation of productive workers)
            = Sum over productive sectors of:
                employee compensation (NIPA 6.2D)

The value composition is related to the profit rate via:
  r = e / (1 + C*/V*)
  where e = S*/V* (exploitation rate, T506)

Numerical range (book period):
  C*/V* rises from approximately 2.8 (1948) to approximately 3.4 (1989)
  representing a 23% increase over the period

Conventional comparison (Table 5.14, p. 140):
  C*/V* ~ 2.45 × (K/L)_conventional
  This ratio reflects:
    (a) C* includes flow of intermediate inputs, not just capital stock
    (b) V* excludes unproductive worker compensation
```

**Parameters**:
- C* (T502): Constant capital flow (billions current dollars)
- V* (T504): Variable capital (billions current dollars)
- K/L conventional: NIPA fixed capital stock / total compensation (for comparison)

**Notes**: The value composition of capital is the flow analogue of the organic composition of capital (OCC). Marx distinguished between the value composition (C/V in value terms), the technical composition (physical capital per worker), and the organic composition (value composition insofar as it reflects the technical composition). In the Shaikh-Tonak framework, C*/V* is the empirically measurable value composition.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| C*/V* ratio to conventional | ~245% of K/L (Table 5.14) | Consistent with 2.45x factor | PASS |
| C*/V* trend | Rising (+23% over 1948-1989) | Confirmed secular increase | PASS |
| C*/V*(1948) | ~2.8 (consistent with Table 5.7) | Verified from chopped data | PASS |
| C*/V*(1989) | ~3.4 (consistent with Table 5.7) | Verified from chopped data | PASS |
| Profit rate identity | r = e/(1 + C*/V*) consistent with T513 | Cross-check passes | PASS |
| C*/V* > 0 | Positive for all years | Confirmed | PASS |
| Year Coverage | 1948-1989 | 1948-1989 | PASS |

### Validation Notes

The value composition of capital provides an independent check on the profit rate series (T513). Given e = S*/V* (T506) and C*/V* (T510), the profit rate must satisfy r = e/(1 + C*/V*). If the profit rate computed directly from S*/(C* + V*) differs from this identity, it signals an inconsistency in the component series. The 245% ratio to the conventional capital-labor measure is a robust diagnostic from Table 5.14 (p. 140) that helps validate both C* and V* independently.

---

## Known Issues

- [ ] **C* requires IO methodology for accurate computation**: Constant capital C* (T502) depends on input-output tables for intermediate consumption allocation across productive sectors; IO tables are available only for benchmark years (1947, 1958, 1963, 1967, 1972, 1977, 1982, 1987), with inter-benchmark years interpolated
- [ ] **Ratio inherits T502 and T504 limitations**: C*/V* compounds errors from both numerator (IO-dependent) and denominator (sector classification-dependent)
- [ ] **No extension beyond 1989**: Extension requires both C* and V* to be independently extended; C* extension is particularly challenging due to IO table methodology changes post-1987
- [ ] **Conventional comparison methodology**: The 245% figure from Table 5.14 uses a specific definition of the conventional capital-labor ratio; alternative conventional measures may yield different comparison ratios

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App C | Input-Output Tables | C.1-C.4 | Source methodology for C* (intermediate inputs by sector) |
| App D | National Accounts Detail | D.2 | Depreciation of productive fixed capital (component of C*) |
| App E | Revenue Accounts | E.2 | V* derivation for denominator |

### Key Appendix Variables
- **C***: Constant capital = intermediate inputs + productive-sector depreciation (Appendix C, D)
- **V***: Variable capital = productive worker compensation (Appendix E, NIPA 6.2D)
- **IO tables**: Input-output tables for benchmark years (Appendix C)
- **CFC**: Consumption of fixed capital for productive sectors (NIPA 6.1, Appendix D)

---

## Related Content

- **Book Table**: 5.7 (Exploitation and Composition), 5.14 (Comparison with conventional measures)
- **Figures**: 5.4 (Value Composition of Capital), 5.7 (Conventional vs Marxian ratios)
- **Derived Series**: T513 (profit rate, via r = e/(1 + C*/V*))
- **Dependencies**: T502 (C*), T504 (V*)
- **Module**: Chapter 5 -- Accounting Framework

## Extension Status

| Property | Value |
|----------|-------|
| Current Period | 1948-1989 (book only) |
| Extension Feasibility | BLOCKED — requires IO benchmark tables (Chapter 4) |
| Wave Assignment | Wave 2 |
| Dependency | Chapter 4 IO classification → sector-level decomposition |
| Estimated Extension Date | After Wave 2 IO chapter completion |
| Notes | Value composition C*/V* requires T502 (C*) extension from IO tables |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Status section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation with benchmark years validated against Table 5.7 and Table 5.14 comparison ratios |

---

*Data Provenance Record following Anu Standard v2.0*
