# S607 — Decomposition

**Series**: Net Social Wage (NSW = B_w + G_w - T_w)

## Construction Flow

```mermaid
flowchart TD
    S607_A["S607-A<br/>S&T 1994"]
    S607_EXT["S607-EXT<br/>BEA NIPA"]
    S607_COMBINED["S607-COMBINED<br/>"]
    S607_EXT["S607-EXT<br/>derive: NSW = B_w + G_w - T_w"]
    S607_COMBINED["S607-COMBINED<br/>splice"]
    S605 --> S607_EXT
    S606 --> S607_EXT
    S604 --> S607_EXT
    S607_A --> S607_COMBINED
    S607_EXT --> S607_COMBINED
```

## Step-by-step construction

**Step 1** — load; inputs=['S607-A']; output=``; formula=``
**Step 2** — derive; inputs=['S605', 'S606', 'S604']; output=`S607-EXT`; formula=`NSW = B_w + G_w - T_w`
**Step 3** — splice; inputs=['S607-A', 'S607-EXT']; output=`S607-COMBINED`; formula=``

## Extension

Splice year: 1989; method: `derive`; depends on: S604, S605, S606

## Provenance

See [`S607_DPR.md`](S607_DPR.md).
