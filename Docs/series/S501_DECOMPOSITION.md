# S501 — Decomposition

**Series**: Total Product (TP*)

## Construction Flow

```mermaid
flowchart TD
    S501_A["S501-A<br/>S&T 1994"]
    S501_B["S501-B<br/>BEA GDPbyIndustry"]
    S501_COMBINED["S501-COMBINED<br/>"]
    S501_COMBINED["S501-COMBINED<br/>splice"]
    S501_A --> S501_COMBINED
    S501_B --> S501_COMBINED
```

## Step-by-step construction

**Step 1** — load
  - Inputs: S501-A

**Step 2** — load
  - Inputs: S501-B

**Step 3** — splice
  - Inputs: S501-A, S501-B
  - Output: `S501-COMBINED`
  - At year: 1997
  - Method: growth_rate

## Extension

- Splice year: 1997
- Splice method: growth_rate
- Depends on: (none)

## Provenance

See [`S501_DPR.md`](S501_DPR.md) for the canonical Data Provenance Record, including source-file citations, validation benchmarks, and known caveats.
