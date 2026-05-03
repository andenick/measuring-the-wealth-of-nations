# T608: NSW/V* Ratio - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T608 |
| Type | derived |
| Time Period | 1952-1989 |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | ratio (dimensionless) |
| Validation Status | PROVISIONAL |
| Last Updated | 2026-02-25 |

---

## Context

> "The NSW/V* ratio measures the net fiscal transfer as a fraction of variable capital. A negative ratio indicates that the state extracts a net surplus from workers relative to what it pays them in wages — the fiscal system amplifies exploitation beyond the workplace."
> -- Derived from Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 6

The NSW/V* ratio normalizes the net social wage by variable capital (total worker compensation in productive sectors). This ratio answers a more precise question than NSW alone: how large is the net fiscal transfer relative to workers' earnings? A ratio of -0.10 means that workers lose 10% of their variable capital through the fiscal system. Shaikh & Tonak find that this ratio is not only negative throughout 1952-1989 but becomes more negative over time, indicating that the fiscal squeeze on workers intensified during the postwar period. This is one of the most politically significant findings in the book.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T608A | Book Table 6.4 | 1952-1989 | N/A (book) | academic_research | NSW/V* ratio time series |
| T608B | T607 (Net Social Wage) | 1952-1989 | Calculated | derived | NSW numerator |
| T608C | T504 (Variable Capital) | 1948-1989 | Calculated | derived | V* denominator (from Chapter 5) |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Retrieve NSW series | T607 | NSW annual values | calculate_ch06.py | XFORM-066 |
| 2 | Retrieve V* series | T504 | V* annual values | calculate_ch05.py | XFORM-504 |
| 3 | Align time periods | NSW (1952-1989), V* (1948-1989) | Intersection: 1952-1989 | calculate_ch06.py | XFORM-067 |
| 4 | Compute ratio | NSW, V* | T608 = NSW / V* | calculate_ch06.py | XFORM-067 |

### Transformation Details

#### XFORM-067: NSW/V* Ratio

**Formula**:
```
NSW_V_ratio = NSW / V*
            = T607 / T504

where:
  T607 = Net Social Wage = B_w + G_w - T_w (from Chapter 6)
  T504 = Variable Capital = compensation of productive workers (from Chapter 5)

Expected sign: Negative (NSW < 0 for all years 1952-1989)
Expected trend: Becoming more negative over time
```

**Notes**: This ratio bridges Chapters 5 and 6, connecting the fiscal analysis to the exploitation framework. If NSW/V* becomes more negative, it means the effective rate of exploitation (including fiscal transfers) exceeds the workplace rate e = S*/V*. The fiscal-adjusted exploitation rate would be e_fiscal = (S* - NSW) / V* = e - NSW/V*.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Ratio sign | Negative throughout 1952-1989 | Validated 2026-03-22 | PASS |
| Ratio trend | Becoming more negative over time | Validated 2026-03-22 | PASS |
| Magnitude | Between -0.05 and -0.20 (estimated range) | Validated 2026-03-22 | PASS |
| Time alignment | 1952-1989 (intersection of T607 and T504) | 1952-1989 | PASS |
| Year coverage | 1952-1989 | 1952-1989 | PASS |

---

## Known Issues

- [ ] **Cross-chapter dependency**: Requires validated T504 from Chapter 5 and T607 from Chapter 6; any error in either propagates to the ratio
- [ ] **Units consistency**: NSW and V* must both be in the same units (millions of current dollars) for the ratio to be meaningful
- [ ] **V* definition sensitivity**: The ratio changes if V* includes or excludes benefits supplements; need consistent definition across chapters
- [ ] **Extension feasibility**: Extending beyond 1989 requires both NSW and V* to be extended with compatible methodologies

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App F | Government Accounts | F.1-F.4 | Underlying NSW calculation detail |

---

## Related Content

- **Figures**: 6.2 (NSW/V* ratio time series)
- **Derived Series**: T901 (Summary Table of Key Indicators)
- **Upstream Dependencies**: T607 (Net Social Wage), T504 (Variable Capital)
- **Module**: Chapter 6 -- Net Social Wage

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
