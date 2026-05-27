# Decision 0007: Canonical verbatim-quote schema for research JSONs

**Status:** Accepted
**Date:** 2026-05-23
**Owner:** Druck (Anu Framework standards)
**Affected projects:** RMWND (and any future Anu-framework project storing per-series research JSONs)
**Phase:** RMWND v1.1 Phase 1

---

## 1. Context

Research JSONs in `Technical/research/*.json` accumulated three coexisting schemas
for verbatim quotations during v1.0 ingestion and cohort-based backfills:

1. **Canonical (target)** — single record inside the top-level `entries[]` list:
   ```json
   {
     "entry_type": "verbatim_quote",
     "content":    "<analyst note about why this quote matters>",
     "source_ref": "<short citation, e.g. 'ST_1994, Ch7 p.213'>",
     "page_reference": "<page or chunk locator>",
     "context":    "<optional surrounding context>",
     "migrated_from": "<optional provenance tag>"
   }
   ```
   The actual verbatim text lives in `content` OR in a sibling field; see §3.

2. **Top-level legacy** — a free-standing `verbatim_quotes[]` array at the JSON root,
   with heterogeneous element shapes (`{text, page, chapter, context, verbatim_check}`,
   `{quote, source_ref, kb_path}`, `{anchor, backfill_date, backfill_task, page, section,
   source, text}`, etc.). Pre-dates the `entries[]` standard.

3. **Inline legacy (cohort 2)** — `entries[]` records that have `entry_type` set to
   something other than `verbatim_quote` (e.g. `definition`, `methodology`) but carry
   sibling fields `verbatim_quote` and `verbatim_source` containing the actual quoted
   text. Cohort 2 (2026-05-24) already added *duplicate* canonical-form entries beside
   each inline-legacy record so anu-doctor P31 counters could find them, but the
   original inline-legacy records were preserved unchanged.

Survey of the 64 RMWND research JSONs (2026-05-23):

| Combination (top, canonical, inline) | Count |
|---|---|
| top + canonical                       | 28 |
| top only                              | 18 |
| canonical + inline-legacy             | 12 |
| canonical only                        |  4 |
| top + inline-legacy                   |  2 |

Forty-eight of 64 series still carried a top-level `verbatim_quotes[]` array,
making schema-aware tooling (anu-doctor P31, anu-docs enrichment, anu-review D2/D5)
brittle and inflating per-series quote counts unreliably.

## 2. Decision

The **canonical schema for verbatim quotations is a record inside `entries[]` with
`entry_type == "verbatim_quote"`.** No other location is authoritative.

### Required fields

| Field          | Type   | Notes                                               |
|----------------|--------|-----------------------------------------------------|
| `entry_type`   | string | Must equal `"verbatim_quote"`                       |
| `content`      | string | Analyst note OR the verbatim text itself; non-empty |
| `source_ref`   | string | Short citation; non-empty                           |

### Optional fields

| Field             | Type   | Notes                                                                 |
|-------------------|--------|----------------------------------------------------------------------|
| `page_reference`  | string | Page or chunk locator (e.g. `"p.213"` or `"chunk_35"`)               |
| `context`         | string | Surrounding paragraph, section title, or analyst gloss                |
| `verbatim_quote`  | string | The verbatim text, when `content` is reserved for the analyst note   |
| `verbatim_source` | string | Source object containing the quote (e.g. KB extract path)            |
| `confidence`      | string | `"high"` \| `"medium"` \| `"low"`                                    |
| `kb_path`         | string | Path into Knowledge Base where the original chunk lives               |
| `migrated_from`   | string | Provenance tag for records produced by an automated migration         |

At least one of `content` or `verbatim_quote` MUST contain the actual quoted text.

## 3. Migration rules

### Rule M-1: Top-level `verbatim_quotes[]` → canonical `entries[]`

For each element of a top-level `verbatim_quotes[]` array, append one new record to
`entries[]`:

```json
{
  "entry_type":      "verbatim_quote",
  "content":         "<text|quote|content from source element>",
  "source_ref":      "<source_ref|source|chapter from source element>",
  "page_reference":  "<page if present>",
  "context":         "<context|section|anchor|notes joined where present>",
  "kb_path":         "<kb_path if present>",
  "migrated_from":   "top_level_verbatim_quotes_array_v1.1_phase1"
}
```

Field-extraction precedence (first hit wins):
- `content` ← `text` → `quote` → `content`
- `source_ref` ← `source_ref` → `source` → `chapter`
- `page_reference` ← `page`
- `context` ← `context` → `section` → `anchor` → `notes` (joined with `" | "` if multiple)
- `kb_path` ← `kb_path`

The original top-level `verbatim_quotes[]` array is **preserved** for backward
compatibility and marked with a sibling top-level boolean field
`verbatim_quotes_deprecated: true`. Downstream tooling MUST ignore the deprecated
array and read only `entries[]`.

### Rule M-2: Inline-legacy sibling-field entries (cohort 2)

Already executed by cohort-2 migration on 2026-05-24:
inline-legacy `entries[]` records with `entry_type != "verbatim_quote"` but carrying
`verbatim_quote`/`verbatim_source` siblings were left in place, and a duplicate
canonical `entries[]` record (`entry_type == "verbatim_quote"`) was appended for
each. Decision 0007 ratifies this approach and adds the `migrated_from` provenance
tag standard for any future re-runs.

### Rule M-3: New authoring

All new verbatim quotes authored after 2026-05-23 MUST be written directly in the
canonical schema. Pre-1.1 schemas MUST NOT be reintroduced.

## 4. Enforcement

`anu-doctor` check **P31** (`per_series_verbatim_quote_minimum`) validates that
every active series in `series_registry.json` has at least three `entries[]`
records with `entry_type == "verbatim_quote"`. Top-level `verbatim_quotes[]` and
inline-legacy records are **not** counted; only canonical records satisfy P31.

`anu-doctor` check **P31a** (`canonical_verbatim_only`) warns when a research JSON
still contains a top-level `verbatim_quotes[]` array that has not been marked
`verbatim_quotes_deprecated: true`.

## 5. Out of scope

- Migration of inline-legacy records into canonical form (already handled by cohort 2).
- Deletion of deprecated top-level arrays (deferred to a future cleanup decision once
  no downstream tool reads them).
- Schema for non-verbatim entry types (definitions, methodology notes, etc.) — those
  retain their existing shapes.

## 6. References

- v1.1 Phase 1, agent 3 task brief (2026-05-23)
- Migration script: `<project>/MIGRATION/_migrate_verbatim_schemas.py`
- Cohort 2 backup registry: `series_registry.pre_stage3_cohort2.20260524T002948Z.json`
- anu-doctor project-mode check definitions: `.claude/skills/anu-doctor/`
