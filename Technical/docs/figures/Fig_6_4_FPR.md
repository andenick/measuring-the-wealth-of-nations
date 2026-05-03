# Fig_6_4: NSW Trend: Tax vs Benefit Rates — Figure Provenance Record

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
| Figure ID | Fig_6_4 |
| Chapter | 6 |
| Page | 160 |
| Title | NSW Trend: Tax vs Benefit Rates |
| Type | time_series |
| is_empirical | true |
| Period | 1952-1989 |

---

## Description

Figure 6.4 charts the net social wage (NSW) by decomposing it into its tax and benefit components over 1952-1989. The net social wage is defined as social benefits received by workers (transfers, public services, social insurance) minus taxes paid by workers. This figure reveals whether the welfare state on balance benefits or burdens the working class in fiscal terms. Shaikh and Tonak find that for most of the postwar period, taxes on workers exceeded the social benefits they received — meaning the NSW was negative, and the state effectively transferred value from workers to capital. The figure shows the trend in both the tax rate on workers and the benefit rate, allowing the reader to see which component drives changes in the net social wage over time.

---

## Data Sources

| Series | Name | Role in Figure |
|--------|------|---------------|
| T601 | Tax Rate on Workers | Worker tax burden trend |
| T605 | Benefit Rate for Workers | Social benefit trend |
| T607 | Net Social Wage Components | Combined NSW measures |

---

## Data File

`Technical/ANU_REPLICATOR/data/final-data/figures/Fig_6_4.csv`

---

## Replication Notes

Plot T601 (tax rate) and T605 (benefit rate) on the same axes over 1952-1989. The net social wage is the difference: T605 - T601. If negative, workers pay more in taxes than they receive in benefits. T607 may provide the pre-computed NSW or additional components. Verify exact definitions against Chapter 6 tables.

---

## Related

- **DPRs**: T601_DPR.md, T605_DPR.md, T607_DPR.md
- **Chapter Investigation**: CHAPTER_6_INVESTIGATION.md
- **Related Figures**: Fig_6_1 (alternative wages), Fig_6_2 (real wage rates)

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-21 | 1.0 | Initial creation |

---

*Figure Provenance Record following Anu Standard v2.0*
