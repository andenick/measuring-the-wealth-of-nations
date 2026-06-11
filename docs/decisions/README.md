# Framework Decisions

This folder records the project-specific framework decisions that
govern series construction and the registry schema. Each decision is a
single definitive document; the rationale lives in the document itself.

| Decision | Topic |
|----------|-------|
| [`0007_verbatim_quote_schema.md`](0007_verbatim_quote_schema.md) | Canonical schema for verbatim source quotes attached to each series. |
| [`0008_reference_values_year_keyed_scalars.md`](0008_reference_values_year_keyed_scalars.md) | Year-keyed scalar `reference_values` for stock-form series (S513 / S514). |

Earlier foundational decisions (extenbook 4-sheet layout, required
`reference_values`, the extension binary invariant, compact script
naming, the `chopped_format` enum, and "code is the source of truth")
are baked into the schema and enforced by the validators and test
suite; they are no longer maintained as loose decision files.
