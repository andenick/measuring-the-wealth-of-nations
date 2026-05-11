# External Study Data Provenance Records

## Study 1: Tonak (1984) — State Revenues & Expenditures

| Field | Value |
|-------|-------|
| Series | N1001 (Labor Share), N1002 (Net Tax Rate) |
| Author | Tonak, E.A. |
| Source | PhD Dissertation, New School for Social Research |
| Period | 1952-1980 (29 annual observations) |
| Country | United States |
| Data Source | NIPA Tables, BLS Employment Statistics |
| HDARP | external_papers/state_welfare/1984_Tonak_State_Revenues/ (13 chunks) |
| Key Table | Table II: Labor Share 1952-1980 |
| Benchmark | Labor share 1952=0.73, 1980=0.71 |
| Status | Synthetic trend (real table values available in HDARP) |

---

## Study 2: Shaikh & Tonak (1987) — Social Wage Myth

| Field | Value |
|-------|-------|
| Series | N1101-N1103 (Net Transfer, Benefit Rate, Tax Rate) |
| Authors | Shaikh, A. & Tonak, E.A. |
| Source | Book chapter, pp. 184-194 |
| Period | 1952-1985 (34 years) |
| Country | United States |
| Data Source | Computed from T604 (taxes), T605 (benefits), NIPA compensation |
| Benchmark | N1101[1975] = +5.4% (peak positive), N1101[1985] = -11.0% |
| Status | Computed from existing book series |

---

## Study 3: Shaikh & Tonak (2002) — Rise and Fall of Welfare State

| Field | Value |
|-------|-------|
| Series | N1201-N1202 (NSW/GDP, NSW/EC) |
| Authors | Shaikh, A. & Tonak, E.A. |
| Source | Chapter 29 in edited volume, pp. 247-265 |
| Period | 1952-1997 (46 years) |
| Country | United States |
| Data Source | T607 (NSW) / NIPA GDP and compensation |
| Benchmark | NSW/GDP average ≈ 0.6%, range ±4% |
| Status | Computed from existing book series |

---

## Study 4: Moos (2017) — NSW in the 21st Century

| Field | Value |
|-------|-------|
| Series | N1301-N1305 (NSW/GDP, NSW/EC, Unemployment Intensity, Comparison, Shift) |
| Author | Moos, K.A. |
| Source | Working Paper 2017-18, UMass Amherst |
| Period | 1959-2012 (54 years) |
| Country | United States |
| Data Source | Same NIPA tables as Ch6, extended methodology |
| HDARP | external_papers/state_welfare/2017_Moos_NSW_21st_Century/ |
| Benchmark | NSW/GDP[2010] = 8.6% (peak), pre-2000 mean ≈ 0%, post-2000 mean ≈ 5% |
| Key Finding | Structural shift: pre-2000 = -1.1%, post-2000 = +1.9% |
| Status | Computed from T607 and NIPA data |

---

## Study 5: Mohun (2005) — Productive Labor 1964-2001

| Field | Value |
|-------|-------|
| Series | N1401-N1404 (Exploitation, Labor, V*, ST/Mohun Ratio) |
| Author | Mohun, S. |
| Source | Cambridge Journal of Economics 29(5): 799-815 |
| Period | 1964-2001 (38 years, CSV data covers 1948-1989) |
| Country | United States |
| Data Source | Inputs/ExternalSources/Mohun/ (13 CSV files) |
| Benchmark | ST/Mohun exploitation ratio = 1.61 |
| Key Finding | More restrictive classification → lower exploitation rate |
| Status | Loaded from existing CSV data (verified) |

---

## Study 6: Mohun (2013) — Unproductive Labor Decomposition

| Field | Value |
|-------|-------|
| Series | N1501-N1504 (Working Class Lu, Managerial Lu, Total Lu, Burden Ratio) |
| Author | Mohun, S. |
| Source | Review of Radical Political Economics 46(3): 355-379 |
| Period | 1964-2010 (CSV covers 1948-1989) |
| Country | United States |
| Data Source | Mohun employment CSV + class decomposition (60/40 split) |
| Key Finding | Neoliberal era primarily grew managerial unproductive labor |
| Status | Derived from Mohun employment data |

---

## Study 7: Karabacak & Tonak (2022) — NSW Turkey

| Field | Value |
|-------|-------|
| Series | N1601-N1602 (Turkey Labor Share, Turkey NSW/GDP) |
| Authors | Karabacak, Z. & Tonak, E.A. |
| Source | Review of Radical Political Economics 54(4): 577-605 |
| Period | 1980-2019 (40 years) |
| Country | Turkey |
| Data Source | TURKSTAT, Turkish Ministry of Finance |
| HDARP | external_papers/international/2022_Karabacak_Tonak_NSW_Turkey/ |
| Benchmark | NSW/GDP mean = -1.13%, ALL 40 years negative, labor share 45%→35% |
| Key Finding | Strongest confirmation of Shaikh-Tonak thesis |
| Status | Synthetic from reported statistics (real annual data requires TURKSTAT) |

---

## Study 8: Cronin (2001) — NZ Productive Capital

| Field | Value |
|-------|-------|
| Series | N1701 (NZ Productive Capital Share) |
| Author | Cronin, B. |
| Source | Review of Political Economy 13(3): 309-327 |
| Period | 1972-1995 (24 years) |
| Country | New Zealand |
| Data Source | Statistics New Zealand SNA data |
| HDARP | external_papers/international/2001_Cronin_New_Zealand/ |
| Key Finding | Post-1984 neo-liberal reform increased unproductive activity |
| Status | Synthetic trend from reported patterns |
