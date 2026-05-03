# Fig_5_2: Productive and Unproductive Labor, 1948-1988 — Figure Provenance Record

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
| Figure ID | Fig_5_2 |
| Chapter | 5 |
| Page | 56 |
| Title | Productive and Unproductive Labor, 1948-1988 |
| Type | time_series |
| is_empirical | true |
| Period | 1948-1988 |

---

## Description

Figure 5.2 charts the historical trends in productive versus unproductive labor over the postwar period 1948-1988. It decomposes total employment into productive labor (workers directly engaged in commodity production) and unproductive labor (workers in circulation, supervision, and other non-value-producing activities). The figure demonstrates the secular rise of unproductive labor as a share of total employment — a central empirical finding in Shaikh and Tonak's Marxian accounting framework. This trend reflects the growing weight of trade, finance, government, and managerial functions in the US economy, with direct implications for the rate of surplus value and the divergence between Marxian and conventional productivity measures.

---

## Data Sources

| Series | Name | Role in Figure |
|--------|------|---------------|
| T511 | Total Employment | Denominator / total labor force reference |
| T515 | Productive Labor (Lp) | Productive employment trend line |
| T516 | Unproductive Labor (Lu) | Unproductive employment trend line |

---

## Data File

`Technical/ANU_REPLICATOR/data/final-data/figures/Fig_5_2.csv`

---

## Replication Notes

Productive labor (T515) is derived from BLS Current Employment Statistics production and nonsupervisory worker counts, filtered to productive sectors as classified via IO benchmark tables. Unproductive labor (T516) is the residual: T511 minus T515. Plot both series against time to reproduce the figure. Index or level presentation depends on book formatting.

---

## Related

- **DPRs**: T511_DPR.md, T515_DPR.md, T516_DPR.md
- **Chapter Investigation**: CHAPTER_5_INVESTIGATION.md
- **Related Figures**: Fig_5_1 (conceptual mapping), Fig_5_7 (labor trends revisited)

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-21 | 1.0 | Initial creation |

---

*Figure Provenance Record following Anu Standard v2.0*
