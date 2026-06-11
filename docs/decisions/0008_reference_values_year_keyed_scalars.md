<!--
status: approved
approved_at: 2026-05-23T11:00:00
-->

# Decision 0008 — `validation.reference_values` schema: year-keyed scalars only

**Date**: 2026-05-23
**Status**: ACCEPTED
**Phase**: v1.1 Phase 1 (Anu Framework v12.0 schema v2.3.0)
**Author**: Agent 4 (composite-key reference_values refactor)
**Supersedes / amends**: Decision 0002 (registry as canonical source of `validation.reference_values`)
**Affects**: anu-doctor P32, V03 validators, series_registry.json schema v2.3.0+

---

## Context

Decision 0002 made `series_registry.json[series][<SID>].validation.reference_values` the canonical, registry-resident dictionary of benchmark values. Each V03 validator was wired to read this dict via `utils.registry_validator.get_reference_values(sid)` so that the validator and the registry could never silently diverge.

The implicit contract was: **keys are years, values are scalars** (`{<year_int>: <float>}`). That contract held for 60+ series. It broke for 7 series whose authors needed to record statistics that are not annual scalars:

| SID    | Non-year keys in `reference_values` (v1.0)                           | Nature                          |
| ------ | -------------------------------------------------------------------- | ------------------------------- |
| ES1301 | `1959_1997_mean`                                                     | period-mean (single statistic)  |
| ES1305 | `structural_shift`                                                   | post/pre-2000 delta (statistic) |
| ES1404 | `mean`                                                               | series mean (statistic)         |
| ES1601 | `mean`, `std`                                                        | summary statistics              |
| ES1602 | `mean`, `n_negative`                                                 | summary + count statistic       |
| S901   | `1948_e`, `1948_VW`, `1948_LpL`, `1989_e`, `1989_VW`, `1989_LpL`, `1989_NSW_V` | year+variable composite (multi-column summary table) |
| AS002  | (year-keyed already; see note below)                                 | n/a — included only because V03 was skipped during the cohort-1 refactor for a different reason |

The Stage 5 V03 refactor (per Decision 0002) skipped these series because the year-keyed contract didn't fit. Six V03 validators (ES1301, ES1305, ES1404, ES1601, ES1602, S901) still carry hardcoded benchmark literals; AS002 reads a derived diagnostic column (`our_gap_to_khanjian_pct`) that isn't in chopped output. That is the gap this decision closes.

## Decision

Split the two concerns into two registry fields with disjoint schemas.

### `validation.reference_values` — year-keyed scalars (canonical anchors)

```jsonc
"reference_values": {
  "<year_int>": <float>,     // e.g. "1959": -0.01455
  "<year_int>": <float>      // at least two endpoints recommended
}
```

* Keys MUST parse as `int` years.
* Values MUST be `float` (the canonical magnitude at that year).
* MUST be a faithful endpoint reading from the chopped CSV (or KB-confirmed published value).
* Empty `{}` is allowed for series whose canonical column has no scalar benchmarks (e.g., S901-A composite NaN).

### `validation.derived_statistics` — non-year statistics (companion field, new in v2.3.0)

```jsonc
"derived_statistics": {
  "mean": <float>,
  "std": <float>,
  "structural_shift": <float>,
  "n_negative": <int>,
  "1959_1997_mean": <float>,   // period-windowed stats allowed
  "1948_e": <float>,            // composite year+variable keys allowed
  ...
}
```

* Keys are free-form strings (statistic name, period-window, year+variable composite).
* Values are `float` (or `int` for counts).
* No structural constraint beyond JSON-serialisable scalars.
* Field is OPTIONAL — series without derived statistics may omit it.

### Migration rule

For every series whose v1.0 `reference_values` carries non-year keys:

1. Move all non-year keys (and their values) into a new `derived_statistics` block, preserving names verbatim.
2. Re-populate `reference_values` with year-keyed endpoint values read from the chopped CSV (at least two anchor years — typically the first and last year present).
3. Record the migration in `registry_patch_notes` with `ts`, cohort tag `v1.1_p1`, and a one-line note referencing Decision 0008.
4. The chopped CSV is unchanged; only the registry validation block is rewritten.

### Enforcement

* `anu-doctor` check **P32** (registry `reference_values` integrity): updated to accept *both* fields per the new contract. P32 SHOULD:
  * Fail if any key in `reference_values` does not parse as `int`.
  * Fail if any value in `reference_values` is not a finite `float`.
  * Allow (no constraint) any key in `derived_statistics`.
  * Pass when `reference_values` is empty *and* `derived_statistics` is non-empty (multi-column summary case).
* V03 validators that need year anchors call `utils.registry_validator.get_reference_values(sid)` (existing, returns only year-int keys after this decision).
* V03 validators that need statistics call `utils.registry_validator.get_derived_statistics(sid)` (new helper added in this decision).
* The legacy `get_reference_values(sid, year_keys_only=False)` path remains for backward compatibility with S901's pre-migration composite handling, but new code SHOULD prefer the split helpers.

## Consequences

* **Positive**: P32 becomes mechanically enforceable; V03 validators stop carrying hardcoded benchmark literals; the registry's two roles (canonical anchors vs. derived stats) become explicit; future series adding statistics know exactly which field to populate.
* **Negative**: 7 registry patches and 6 V03 refactors land in this phase. anu-doctor must ship a new P32 implementation before this decision is enforced strictly.
* **Forward-compatible**: anu-chopped, anu-extenbook, anu-publish are unaffected (they don't read either field). anu-review D6 (validation quality) gains a new sub-check: prefer year anchors over single statistics.

## AS002 sub-note

AS002 already had year-keyed `reference_values` (the five IO benchmark years: 1958, 1963, 1967, 1972, 1977). It was skipped during the cohort-1 refactor because the V03 read a diagnostic column (`our_gap_to_khanjian_pct`) that is *not* present in chopped output. Under Decision 0008 the V03 is refactored to compare chopped column `AS002-A` (rate of surplus value via Khanjian decomposition) against the registry's year anchors. No migration patch is required for AS002's `validation.reference_values` itself; only the V03 source is updated.

## References

* Decision 0002 (registry-as-source-of-truth for benchmarks) — now archived in the framework decision log; concepts live in `SERIES_REGISTRY_SCHEMA.md`
* `Technical/code/utils/registry_validator.py` (helper module)
* `Technical/_v1.1_patches/<SID>_decision_0008_patch.json` (per-series migration patches)
* anu-doctor P32 (rule to be updated in the framework skill files)

## Provenance note (v1.2 iter2 — 2026-05-24)

This decision was originally authored in the project decision log during v1.1 Phase 1. It was moved to its canonical framework decision-log location during v1.2 iteration 2 (P28 cleanup) so that all framework-level decisions live in one place alongside Decision 0007. The original project-local file has been removed; references in code/docs have been updated.
