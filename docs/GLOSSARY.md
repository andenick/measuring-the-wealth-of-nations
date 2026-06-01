# Glossary

Definitions for terms, symbols, and abbreviations used throughout the RMWND replication. This glossary covers (1) Marxian categories operationalized by Shaikh & Tonak (1994), (2) Anu Framework v12.0 artifact and decision terminology, and (3) data-source abbreviations.

---

## 1. Marxian categories (Shaikh & Tonak operationalization)

Symbols follow the book's convention. An asterisk (`*`) marks aggregates derived after the productive / unproductive partition has been applied (i.e., aggregates that exclude unproductive sectors). Capital letters denote *value-form* (price × quantity, current dollars) magnitudes; lowercase Greek / Latin letters denote *labor-time* coefficients.

| Symbol | Name | Definition |
|---|---|---|
| **TP\*** | Total Product | Gross output of the productive sector. Series **S501** (book Ch.5). |
| **C\*** | Constant Capital | Value of means of production consumed (intermediate inputs) in the productive sector. Series **S502** (Ch.5). |
| **V\*** | Variable Capital | Wages of productive labor. Series **S504** (Ch.5). |
| **S\*** | Surplus Value | Productive-sector surplus: `S* = TP* − C* − V*`. Series **S505** (Ch.5). The `S505 = S503 − S504` identity carries a documented wedge (see book Tables 5.5 / 5.6) — pytest XFAIL is the honest expression of this. |
| **e** | Rate of Exploitation | `e = S* / V*`. Series **S506** (Ch.5). |
| **r\*** | Marxian Profit Rate | Stock-form (canonical, v1.2): `r* = S* / K*` where `K*` is productive capital stock (S517). Flow-form (secondary, retained as `S513-FLOW`): `r* = S* / (C* + V*)`. Series **S513**. See `Technical/docs/variants/VPR_S513_stock_vs_flow.md` and DIV-012. |
| **K\*** | Productive Capital Stock | BEA fixed-asset net stock for productive industries, current cost. Series **S517**. The book's prose calls this "gross stock" but values match BEA NET stock at all five benchmark years exactly; see S517 EPR `conceptual_continuity` field for the disclosure. |
| **Lp** | Productive Labor | Hours of labor employed in productive sectors. |
| **Lu** | Unproductive Labor | Hours of labor employed in unproductive sectors (trade, finance, government services). |
| **GFP** | Gross Final Product | `GFP = TP* − C*_m` (subtracting only material constant capital). Series **S503**. Distinct from S505 by the wedge described above. |
| **NSW** | Net Social Wage | Worker tax contributions minus social benefits received. Used as a transfer adjustment in some derived series. |
| **hp\*** | Direct Labor Coefficient | Hours of direct (productive) labor per dollar of output, per industry. Series **S701**. |
| **λ\*** | Total Labor Coefficient | Leontief-amplified direct coefficient: `λ = hp* × (I − A)^−1` where `A` is the input-output matrix. Series **S702**. The book + Khanjian 1980s benchmark for the value-price deviation envelope (S703) is 6–9 %; v1.2 publishes an honest blocker note documenting why the current per-aggregate computation lands outside that envelope (see `Technical/Handoffs/CH7_REAL_FIX_PLAN.md`). |

### Derived ratios used in the book

| Symbol | Name | Series |
|---|---|---|
| `S* / Y` | Surplus Ratio | **S507** — superseded definition uses `S* / (S* + V*) = e / (1 + e)`; see DIV-001. |
| `VA* − V*` | Value-Added minus Variable Capital | Implicit in the S505 / S503 wedge discussion. |
| `S* / W` | Total Surplus over Total Wages | Used in distribution analysis chapters. |

---

## 2. Anu Framework v12.0 terms

### Workspace-level decisions (canonical at `Council/Druck/docs/decisions/`)

| ID | Title | Effect on RMWND |
|---|---|---|
| **Decision 0001** | Extenbook 4-sheet canonical format | All RMWND extenbooks ship Data / Provenance / Research / Construction sheets. |
| **Decision 0002** | Registry as benchmark source | Every series carries `validation.reference_values`; V03 reads from registry, not hardcoded. |
| **Decision 0003** | Extension binary invariant | Either `extension: null` with no `-EXT` / `-COMBINED` subseries, OR populated extension block with both subseries — never partial. |
| **Decision 0004** | Compact L01 / P02 / V03 naming | `<phase>_<sid>.py` convention. RMWND was already compliant. |
| **Decision 0005** | Wide chopped format | Row 1 metadata, Row 2 column IDs, Row 3+ data. Long-form CSV permitted elsewhere. |
| **Decision 0006** | Code as source of truth | When code and registry disagree, code wins; registry must be patched. |
| **Decision 0007** | Verbatim-quote canonical schema | 48 research JSONs migrated in v1.1; new entries must conform. |
| **Decision 0008** | reference_values year-keyed-scalars policy | 7 series patched in v1.1; year-keyed scalars (not lists) for benchmark anchors. |

### Per-series provenance records

| Acronym | Full name | Purpose |
|---|---|---|
| **DPR** | Data Provenance Record | Documents the source(s), authority, and per-year provenance of a single series (book period). Authored per-series by the agent during Stage 3 ingestion. |
| **EPR** | Extension Provenance Record | Documents the live-API source, methodology, and divergence-from-book for a series' extension beyond the book horizon (canonical 6-field schema). |
| **VPR** | Variant Provenance Record | Documents an alternative construction approach for a series. Each variant gets a unique ID; the chosen primary form is implemented, alternatives are documented for future reconsideration. |

### DIVERGENCE_REGISTER

A **DIV** entry (`DIV-NNN-SXXX`) records every numerical or methodological divergence from a predecessor implementation (ST2 baseline) or from the book. Status values: `active`, `partially_resolved`, `resolved`, `resolved_by_DIV-NNN`. Live register at `Technical/DIVERGENCE_REGISTER.json` (12 entries as of v1.2).

### Subseries suffix convention

| Suffix | Meaning |
|---|---|
| **`-A`** | Book period (the literal Shaikh & Tonak 1994 horizon, typically 1948–1989). |
| **`-EXT`** | Extension subseries — series values derived from live BEA / BLS / FRED data beyond the book horizon (typically 1998–2024 or 1990–2024 depending on data availability). |
| **`-COMBINED`** | Full-range spliced subseries `-A` ∪ `-EXT` (the consumer-facing published series). |
| **`-INTERP`** | Bridge-interpolation subseries covering a gap between `-A` and `-EXT` (e.g., S504 / S512 1990–1997 INTERP bridge). |
| **`-FLOW`** | Secondary flow-form variant (currently only `S513-FLOW` and `S514-FLOW` per DIV-012). |

### Pipeline phases

| Phase | Acronym meaning | Role |
|---|---|---|
| **L01** | Loading | Reads source CSVs / cached API responses into a canonical in-memory shape. |
| **P02** | Processing | Implements the construction formula. Hardcoded book tables in P02 are forbidden per the AS003 cleanup. |
| **V03** | Validation | Compares output against `validation.reference_values` from the registry. |
| **M0x** | Manual Adjustment | Documents bridge factors, vintage adjustments, splice methodology (e.g., M04 BLS CES 2003 bridge). |
| **O01** | Output | Generates the chopped CSV from in-memory series. |

---

## 3. Data-source abbreviations

| Acronym | Full name | RMWND usage |
|---|---|---|
| **SIC** | Standard Industrial Classification | Pre-1997 industry partition. Book Appendix C concordance. |
| **NAICS** | North American Industry Classification System | Post-1997 industry partition. SIC → NAICS bridges live in `data/source/concordances/`. |
| **BEA** | Bureau of Economic Analysis | NIPA tables, fixed-asset accounts (S517 capital stock), GDP-by-industry. |
| **BLS** | Bureau of Labor Statistics | CES employment, productivity / hours, KLEMS multifactor productivity. API key stored at `Council/Robin/.secrets/`. |
| **CES** | Current Employment Statistics (BLS program) | Establishment-survey employment by supersector. Subject to a 2003 SIC → NAICS retrospective revision; bridge factors at `data/adjusted-final-data/bls_ces_2003_bridge_factors.json` (DIV-010). |
| **NIPA** | National Income and Product Accounts (BEA) | Source for most aggregate flow series in chapters 5–6. |
| **TCU** | Capacity utilization (FRED series `TCU`) | Used for capacity-adjusted profit-rate series (S514). |
| **FRED** | Federal Reserve Economic Data | St Louis Fed data portal. |
| **IO matrix** | Input-Output matrix (BEA Use / Make tables) | Source for Leontief inverse used in S702 total labor coefficients. |
| **KLEMS** | Capital, Labor, Energy, Materials, Services productivity accounts | BLS productivity decomposition used in select ES series. |
| **QCEW** | Quarterly Census of Employment and Wages (BLS) | Alternative employment source; used for cross-validation of CES. |

---

## See also

- `Technical/docs/ROADMAP.md` — release roadmap and milestone definitions.
- `Technical/Handoffs/BACKLOG.md` — items deferred from v1.2.
- `Council/Druck/docs/decisions/` — canonical decision log (0007 + 0008).
- `Council/Druck/anu/` — Anu Framework v12.0 canonical scripts and protocol docs.
