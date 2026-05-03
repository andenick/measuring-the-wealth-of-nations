# Fig_6_2: Real Wage Rates — Figure Provenance Record

## Anu Standard Compliance: v2.0

| Property | Value |
|----------|-------|
| Standard | Anu Standard v2.0 |
| Record Type | Figure Provenance Record (FPR) |
| Created | 2026-03-21 |

---

## Quick Reference

| Property | Value |
|----------|-------|
| Figure ID | Fig_6_2 |
| Chapter | 6 |
| Page | 79 |
| Title | Real Wage Rates |
| Type | time_series |
| is_empirical | true |
| Period | 1952-1989 |

---

## Description

Figure 6.2 plots real wage rates over 1952-1989, focusing on the per-worker compensation of productive laborers in real terms. Using variable capital (V*) from the Marxian accounts divided by productive employment (Lp), this figure tracks the real wage rate — the actual purchasing power received per unit of productive labor. The trajectory reveals the well-known pattern of rising real wages through the mid-1970s followed by stagnation or decline, but the Marxian framing provides additional insight: the real wage rate must be understood in relation to productivity (value produced per worker), so that even a rising real wage can coexist with a rising rate of exploitation if productivity grows faster.

---

## Data Sources

| Series | Name | Role in Figure |
|--------|------|---------------|
| T504 | Variable Capital (V*) | Nominal wage bill for productive workers |

---

## Data File

`Technical/ANU_REPLICATOR/data/final-data/figures/Fig_6_2.csv`

---

## Replication Notes

Real wage rate = V* (T504) deflated by appropriate price index, divided by productive employment (T515) to get per-worker real wage. The choice of deflator matters: CPI, GDP deflator, or value-of-labor-power deflator each yield different trajectories. Verify which deflator the book uses on p. 79.

---

## Related

- **DPRs**: T504_DPR.md
- **Chapter Investigation**: CHAPTER_6_INVESTIGATION.md
- **Related Figures**: Fig_6_1 (alternative wage measures), Fig_6_3 (labor content)

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-21 | 1.0 | Initial creation |

---

*Figure Provenance Record following Anu Standard v2.0*
