# T607: Net Social Wage — Decomposition

## Quick Reference

| Property | Value |
|----------|-------|
| Series ID | T607 |
| Name | Net Social Wage (NSW) |
| Chapter | 6 |
| Book Table | 6.3 |
| Period | 1952-2025 |
| Units | Billions of current dollars |
| Tier | 1 |
| Wave | 1 |

## Sub-Components

| Subseries | Name | Source | Period | Units |
|-----------|------|--------|--------|-------|
| T607-A | Net Social Wage (book data) | Book 6.3 | 1952-1989 | Billions of current dollars |
| T607-EXT | Net Social Wage (extension) | BEA NIPA | 1990-2025 | Billions of current dollars |
| T607-COMBINED | Net Social Wage (spliced) | A + EXT | 1952-2025 | Billions of current dollars |

## Construction Steps

| Step | Operation | Input | Output | Notes |
|------|-----------|-------|--------|-------|
| 1 | Load | T607-A raw data | T607-A series | Book period NSW |
| 2 | Derive | T605 (B_w) + T606 (G_w) - T604 (T_w) | NSW calculation | NSW = B_w + G_w - T_w |
| 3 | Splice | T607-A, T607-EXT | T607-COMBINED | Splice at 1989; BEA NIPA extends 1990-2025 |

## Flow Diagram

```mermaid
graph TD
    subgraph "Tax Components (T604)"
        T601["T601<br/>Personal Tax Workers"]
        T602["T602<br/>Social Insurance Tax Workers"]
        T603["T603<br/>Property Tax Workers"]
        IND["Indirect Taxes<br/>(worker share)"]
        T601 --> T604["T604<br/>Total Tax Workers (T_w)"]
        T602 --> T604
        T603 --> T604
        IND --> T604
    end

    subgraph "Benefit Components"
        SS["Social Security"] --> T605["T605<br/>Benefits B_w"]
        MC["Medicare"] --> T605
        UI["Unemployment Insurance"] --> T605
        OB["Other Benefits"] --> T605
    end

    subgraph "Service Components"
        EDU["Education"] --> T606["T606<br/>Services G_w"]
        HLT["Health"] --> T606
        OS["Other Services"] --> T606
    end

    T605 --> NSW["NSW = B_w + G_w - T_w"]
    T606 --> NSW
    T604 --> NSW

    NSW --> T607A["T607-A<br/>Book (1952-1989)"]

    BEA["BEA NIPA<br/>Extension Data"] --> T607EXT["T607-EXT<br/>(1990-2025)"]

    T607A --> SPLICE["Splice at 1989"]
    T607EXT --> SPLICE
    SPLICE --> T607["T607-COMBINED<br/>Net Social Wage<br/>(1952-2025)"]

    style T607 fill:#f9f,stroke:#333,stroke-width:2px
    style NSW fill:#bbf,stroke:#333,stroke-width:2px
```

## Source Methodology

See `Technical/research/T607_research.json` for full research documentation.

The Net Social Wage (NSW) measures the net fiscal impact of government on workers: benefits received (B_w) plus services consumed (G_w) minus taxes paid (T_w). The book data covers 1952-1989 and is extended through 2025 using BEA NIPA data, with a splice at 1989.

Key figures: 6.1, 6.3, 6.4.

## Related Series

- **T604** — Total Tax Workers (input: T_w)
- **T605** — Government Benefits Workers (input: B_w)
- **T606** — Government Services Workers (input: G_w)
- **T608** — NSW/V* (uses T607 as numerator)
- **T609** — NSW/NI (uses T607 as numerator)
- **T901** — Summary Table (includes T607-derived ratios)
