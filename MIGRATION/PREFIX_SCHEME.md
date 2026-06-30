# RMWND Prefix Scheme

**Project**: Measuring the Wealth of Nations Replication
**Scheme**: S / ES / AS (project-specific extension of canonical D / AD)

## Rationale

RMWND uses a project-specific prefix scheme rather than the canonical `D`/`AD` scheme because:

1. The project predates the canonical scheme (began as predecessor-build with T### / N### IDs)
2. The three-prefix system (`S` for primary book series, `ES` for external studies, `AS` for analytical/supplementary) provides clearer semantic grouping for a project with 64 series spanning 8 follow-up studies
3. The scheme was established during Wave 0 and is now frozen across 64 series, 100+ code files, and 64 chopped CSVs

## ID Grammar

```
^(S|ES|AS)\d{3,4}(-[A-Z]|-EXT|-COMBINED)?$
```

## Prefix Definitions

| Prefix | Full Name | Count | Description |
|--------|-----------|-------|-------------|
| `S` | Primary Series | 33 | Direct replications from the book (Chapters 2, 4, 5, 6, 7, 8, 9) |
| `ES` | External Studies | 27 | Follow-up papers by Shaikh, Tonak, and others (Studies 1-8) |
| `AS` | Analytical Series | 4 | Supplementary series (profit rate components, GDP deflator, etc.) |

## Subseries Suffixes

| Suffix | Meaning |
|--------|---------|
| `-A` | Book period (primary data) |
| `-B` | Extension period or secondary component |
| `-EXT` | API extension data only |
| `-COMBINED` | Final spliced series (book + extension) |
| `-F` | Female-specific data (employment series) |

## Compatibility

This scheme is registered in `series_registry.json` under `prefix_scheme`:
```json
{
  "prefix_scheme": {
    "primary": "S",
    "external": "ES",
    "analytical": "AS"
  }
}
```

`anu-doctor` P12 accepts project-declared prefix schemes rather than hard-coding the canonical `D`/`AD`.
