# VPR: S513 Marxian Profit Rate — Stock vs Flow Form

**Series**: S513 (Marxian profit rate r*)
**Variant ID**: VPR_S513_stock_vs_flow
**Date**: 2026-05-24
**Author**: anu-rebuild v1.1 Phase 3
**Status**: exploratory (no methodology change committed)

## Problem

S513 currently splices a stock-form rate (book Table 5.11) into a flow-form
rate (registry-prescribed extension) at 1989:

- **S513-A** (1948-1989): `r* = S* / (K* + V*)` — uses K* (productive capital
  stock), the standard Shaikh formulation in *Measuring the Wealth of Nations*
  Table 5.11.
- **S513-EXT** (1998-2024): `r* = S* / (C* + V*)` — uses C* (constant capital
  *flow*, equal to Mp = M*p — total intermediate inputs of the productive
  sector), per the registry's extension block.

Until v1.1 Phase 2, S517 (K*) had no extension series, so only the flow-form
denominator was available post-1989 and the registry chose flow-form for
S513-EXT. With S517-EXT now populated from BEA Fixed Assets Table 4.1
(Current-Cost Net Stock of private nonresidential fixed assets), both forms
are computable across 1948-2024 and the splice form-change can be made
explicit as a methodology variant rather than left as an implicit
extension-time substitution.

## Forms

| Form  | Formula              | Denominator interpretation                         |
|-------|----------------------|----------------------------------------------------|
| Stock | `r* = S* / (K* + V*)` | Productive capital advanced (durable stock + wage fund) |
| Flow  | `r* = S* / (C* + V*)` | Annual productive costs (intermediate flow + wages)     |

These are different concepts. Under steady reproduction the two ratios are
related by the turnover time of constant capital (`K* / C*`); they coincide
only if `K* = C*`, which they never do in U.S. data (`K*` is roughly 2.5x to
3x `C*` over 1948-2024).

## Results

Computed by `code/E08_exploration/E_S513_stock_vs_flow.py` over all 69 years
where all four inputs (S505, S502, S504, S517) have `-COMBINED` values
(1948-1989 book, 1998-2024 extension; the 1990-1997 splice gap is preserved
as in the underlying inputs). Full table: `data/scratch/S513_stock_vs_flow.csv`.

### Period-level comparison

| Period      | n  | mean r_flow | mean r_stock | mean (r_flow - r_stock) |
|-------------|----|------------:|-------------:|------------------------:|
| Book (1948-1989)      | 42 | 0.5944 | 0.3777 | +0.2167 |
| Extension (1998-2024) | 27 | 0.4162 | 0.1610 | +0.2552 |
| Full (combined)       | 69 | 0.5246 | 0.2929 | +0.2317 |

### Splice-junction levels

| Year | r_flow | r_stock | published S513 value | Form published     |
|------|-------:|--------:|---------------------:|--------------------|
| 1989 | 0.6563 | 0.3723  | 0.3723 (S513-A)      | **stock**          |
| 1998 | 0.3583 | 0.1693  | 0.3583 (S513-EXT)    | **flow**           |

The published S513 series jumps from `r_stock(1989) = 0.3723` to
`r_flow(1998) = 0.3583` at the splice — visually a smooth landing, but only
because the form changes at the same time the data source changes. Within
either form taken consistently:

- Stock-form: 0.3723 (1989) -> 0.1693 (1998), a 54% level drop over 9 years.
- Flow-form: 0.6563 (1989) -> 0.3583 (1998), a 45% level drop over 9 years.

The published series understates the post-1989 decline because the flow-form
denominator (C* + V*) is structurally smaller than the stock-form denominator
(K* + V*).

### Sign analysis

`r_flow > r_stock` in **69 of 69 years** (100%). The two series do not
cross; the flow form is uniformly higher because `C* < K*` in every year.

### Max divergence

Year **2024**: r_flow = 0.4903, r_stock = 0.1604, abs_diff = +0.3299
(r_flow is 3.06x r_stock). Divergence grows over time as `K*/C*` rises
(consistent with rising organic composition / longer turnover).

## Methodological Analysis

**These two rates measure different things.** This is not a "which is closer
to the book" comparison in the simple sense — the book *itself* uses two
different denominators in different places:

- Table 5.11 (the S513 book reference) uses `r* = S* / (K* + V*)` — stock
  form. This is the figure that appears in Chapter 5's profit-rate plots
  (Fig 5.5, Fig 5.8) which the registry lists under S513's `figures`.
- Other passages discussing reproduction and value flows use ratios of S*
  to flow magnitudes (C* + V* or Mp + V*), which correspond to the flow form.

The Marxian tradition itself uses *both* concepts: the *rate of profit* in
the strict sense (relevant to long-run accumulation and TRPF analysis) is
the stock-form rate; ratios of surplus value to flow magnitudes are useful
auxiliaries but are not "the" profit rate.

The current S513 splice combines them by accident of data availability
(K* extension didn't exist when the extension methodology was authored)
rather than by methodological design. That is a form of silent methodology
change at the splice and violates the spirit of Decision 0008's
splice-disclosure expectation.

### Cross-check against S514

S514 ("Adjusted profit rate", r_adj) is the book's matching adjusted-form
rate that pairs with S513. If S513's primary form is changed, S514's
matching form should be changed in lockstep — they are conceptually paired
and used together in Fig 5.5 / Fig 9.x dual plots. This means the choice of
primary form is a coordinated S513+S514 decision, not a unilateral S513
decision.

## Recommendation

**Primary form: stock-form (`r* = S* / (K* + V*)`) across the full 1948-2024
span.** The book's Table 5.11 — the explicit S513 reference — uses stock
form, and the figures S513 feeds (Fig 5.5, Fig 5.8) are stock-form plots.
Maintaining stock-form across the splice preserves conceptual continuity
with the book and matches the cross-series TRPF narrative in Chapter 9.

**Secondary form: flow-form, kept as a documented variant.** The current
S513-EXT (flow-form) is computationally valid and is documented in
DIVERGENCE_REGISTER DIV-005 (registry-noted form change). It should be
retained as a published variant subseries (e.g. S513-EXT-FLOW) for users
who want the flow-form rate.

**Splice 1989 form-change**: previously implicit and noted only as an
extension-time divergence. With this VPR, document it as DIV-009 — an
explicit methodology variant resolved by adopting stock-form as primary.

### What this VPR does NOT do

- It does **not** change `series_registry.json`, `PIPELINE_STATE.json`,
  `ANU_LEDGER.json`, `MANIFEST.json`, or `SUBSERIES_PLAN.json`.
- It does **not** regenerate `chopped/S513.csv` or visualizations.
- It does **not** unilaterally change S514's form.

Adopting the recommendation requires a coordinated change set:

1. Author a paired VPR_S514_stock_vs_flow (S514 is conceptually locked to
   S513).
2. Add a Stage 5 patch that recomputes S513-EXT (and S514-EXT) under
   stock-form using S517-COMBINED, retains the flow-form as
   `S513-EXT-FLOW` / `S514-EXT-FLOW` published variants.
3. Regenerate `chopped/S513.csv`, `chopped/S514.csv`, and any visualization
   that consumes them (Fig 5.5, Fig 5.8, Fig 9.2, Fig 9.4).
4. Update V03_S513 / V03_S514 reference values to honor the new primary
   form at 1998 (currently 0.3583; stock-form would be 0.1693).
5. Add a methodology note in `docs/methodology/` cross-referencing this VPR
   and explaining the splice-discontinuity that adopting stock-form makes
   visible (0.3723 -> 0.1693 at 1989->1998, a real economic decline
   currently masked by the form change).

## Impact

- **viz**: If primary form changes, Fig 5.5 / 5.8 / 9.x dual plots
  (r* and r_adj) will show a more pronounced post-1989 decline. This is
  *more* faithful to the underlying economic reality, not less.
- **chopped/S513.csv** (and S514.csv): would need regeneration with new
  primary; format unchanged.
- **Validation**: V03_S513 reference values at extension endpoints need
  updating.
- **Narrative**: The post-1989 profit-rate decline becomes substantially
  larger when measured consistently in stock-form. This *strengthens* the
  Shaikhian TRPF narrative the project replicates; it is not a problem to
  be smoothed away.
- **No upstream rebuild needed**: S505, S502, S504, S517 are unaffected;
  only S513 / S514 derived stages change.

## References

- `code/E08_exploration/E_S513_stock_vs_flow.py` — computation script
- `data/scratch/S513_stock_vs_flow.csv` — 1948-2024 full table
- `docs/variants/VPR_S517_gross_vs_net.md` — paired VPR on the K* extension
  measure (cross-reference: any change here depends on S517 measure choice)
- `DIVERGENCE_REGISTER.json` — DIV-005 (S513 form-change at extension,
  existing); DIV-009 (this VPR, added in `_v1.1_patches/`)
- `series_registry.json` — `series.S513` (extension methodology),
  `series.S514` (paired adjusted rate), `series.S517` (K* now extended)
- *Measuring the Wealth of Nations*, Shaikh & Tonak 1994 — Table 5.11,
  Chapter 5 figures, Appendix H (text-only K* construction)
