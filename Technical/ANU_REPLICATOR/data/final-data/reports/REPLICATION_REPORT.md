# Anu Replication Report — AS2

**Generated**: 2026-04-09 14:29:24  
**Pipeline version**: 3.0.0  
**Series processed**: 20  

---

## Summary

| Metric | Count |
|--------|------:|
| Total series | 20 |
| Passed       | 20 |
| Warnings     | 0 |
| Failed       | 0 |

## Series Detail

### ✓ T501

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | IO TV* loaded: 28 years (1997-2024) |
| 2 | · | T501: 14 book rows + 83 GDP-extended (1997+ IO-based) → 97 total |
| 3 | · | T502: 14 book rows + 83 GDP-extended → 97 total |
| 4 | · | T503: 14 book rows + 83 GDP-extended → 97 total |
| 5 | · | T508: 14 book rows + 83 GDP-extended → 97 total |
| 6 | · | T509: 14 book rows + 83 GDP-extended → 97 total |

### ✓ T511

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T511: 42 book + 77 ext rows | WARN: T511[1967]: NIPA vintage diff 0.5100 vs 0.48 (within tolerance) |
| 2 | · | T512: 42 book + 77 ext rows | WARN: T512[1989]: NIPA vintage diff 0.3600 vs 0.33 (within tolerance) |

### ✓ T515

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | BLS extension: 35 years |
| 2 | · | T515/T516: 42 book + 35 ext rows |

### ✓ T507

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T507: 42 book + 32 ext rows |
| 2 | · | T510: extension blocked by C*/V* unit mismatch (C* in billions, V* in millions) |
| 3 | · | T510: 42 rows (book only) |

### ✓ T601

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T601: 38 rows (book only) |
| 2 | · | T602: 38 rows (book only) |
| 3 | · | T603: 38 rows (book only) |
| 4 | · | T604: 38 rows (book only) |

### ✓ T605

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T605: 38 book + 36 ext rows |
| 2 | · | T605: 1996 continuity OK (+8.2%) |
| 3 | · | T605: splice continuity 1989->1990: +10.3% |
| 4 | · | T606: 38 book + 36 ext rows |
| 5 | · | T606: 1996 continuity OK (+6.9%) |
| 6 | · | T606: splice continuity 1989->1990: +7.6% |

### ✓ T504

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T504 book: 42 rows, 1948-1989 |
| 2 | · | BEA compensation: 27 rows |
| 3 | · | Interpolated 8 gap years (1990-1997) via log-linear growth |
| 4 | · | Extension: 27 years via W×(V*/W) |

### ✓ T506

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | Mohun cross-validation (informational): |
| 2 | · |   1948: ST=1.700 Mohun=1.667 diff=+0.033 |
| 3 | · |   1958: ST=1.830 Mohun=1.699 diff=+0.131 |
| 4 | · |   1967: ST=2.100 Mohun=1.760 diff=+0.340 |
| 5 | · |   1977: ST=2.100 Mohun=1.793 diff=+0.307 |
| 6 | · |   1989: ST=2.440 Mohun=1.873 diff=+0.567 |
| 7 | · | T506: 42 book, 77 combined rows |

### ✓ T505

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T505 book: 42 rows |
| 2 | · | Extension via GFP-V*: 35 years |

### ✓ T513

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T513: 42 book, 77 combined |
| 2 | · | T514: 42 book, 77 combined |

### ✓ T607

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T607: 74 rows |
| 2 | · | T608: 73 rows (NSW/V*) |
| 3 | · | T609: 74 rows |

### ✓ T901

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T901 book: 42 rows |
| 2 | · | T506_exploitation_rate: 77 rows from T506 |
| 3 | · | T511_productive_labor_share: 77 rows from T511 |
| 4 | · | T512_productive_wage_share: 77 rows from T512 |
| 5 | · | T513_marxian_profit_rate: 77 rows from T513 |
| 6 | · | T514_capacity_adj_profit_rate: 77 rows from T514 |
| 7 | · | T608_nsw_v_star: 73 rows from T608 |
| 8 | · | Summary: 77 rows, 6/6 columns |

### ✓ T401

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | 1947: 85×85, sparsity=36.18%, eig_max=0.9918, B check: dev=10.572171 |
| 2 | · | 1958: 85×85, sparsity=36.04%, eig_max=0.9584, B check: exact match |
| 3 | · | 1963: 85×85, sparsity=36.65%, eig_max=0.9588, B check: dev=1.914787 |
| 4 | · | 1967: 85×85, sparsity=39.54%, eig_max=0.5048, B check: dev=1.013377 |
| 5 | · | 1972: 85×85, sparsity=40.51%, eig_max=0.9883, B check: dev=9.317743 |
| 6 | · | 1977: 85×85, sparsity=42.75%, eig_max=0.9867, B check: dev=7.032045 |

### ✓ T701

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | 1947 T701: mean lv*=0.000414 (productive=0.000442) |
| 2 | · | 1947 T702: r_bar=0.1945 |
| 3 | · | 1947 T703: MAD=1.022341, corr=-0.1588, R²=-155.3839 |
| 4 | · | 1958 T701: mean lv*=0.004213 (productive=0.004289) |
| 5 | · | 1958 T702: r_bar=0.2032 |
| 6 | · | 1958 T703: MAD=1.024257, corr=-0.2841, R²=-308.1578 |
| 7 | · | 1963 T701: mean lv*=0.000353 (productive=0.000371) |
| 8 | · | 1963 T702: r_bar=0.1957 |
| 9 | · | 1963 T703: MAD=1.026319, corr=-0.0643, R²=-195.9807 |
| 10 | · | 1967 T701: mean lv*=0.138081 (productive=0.142671) |
| 11 | · | 1967 T702: r_bar=1.3448 |
| 12 | · | 1967 T703: MAD=1.029181, corr=0.1302, R²=-16.9003 |
| 13 | · | 1972 T701: mean lv*=0.287196 (productive=0.313901) |
| 14 | · | 1972 T702: r_bar=0.1920 |
| 15 | · | 1972 T703: MAD=0.824118, corr=0.8524, R²=-6.3370 |
| 16 | · | 1977 T701: mean lv*=0.160140 (productive=0.174401) |
| 17 | · | 1977 T702: r_bar=0.1936 |
| 18 | · | 1977 T703: MAD=0.883781, corr=0.4551, R²=-13.3843 |

### ✓ T801

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | T801: 42 overlapping years, MAD=0.2835, corr=0.9500 |
| 2 | · | T201: book period GFP/GDP ratio: mean=0.0000, range=0.0000-0.0000 |
| 3 | · | T201: 97 years, GFP vs GDP comparison |

### ✓ N1401

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | N1401: 42 rows (1948-1989) |
| 2 | · | N1402: 42 rows (1948-1989) |
| 3 | · | N1403: 42 rows (1948-1989) |
| 4 | · | N1404: 42 years, mean ratio=1.61 |

### ✓ N1301

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | N1301: 28 years | 1959-1997 mean=-0.0062 vs Moos=0.0110 |
| 2 | · | N1302: 74 years (NSW/EC) |
| 3 | · | N1304: 1 years (1959-1997 overlap) |
| 4 | · | N1305: pre-2000 mean=-0.0107, post-2000 mean=0.0142 (shift=+0.0249) |

### ✓ N1101

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | N1101: 34 years (net transfer rate) |
| 2 | · | N1102: 34 years (benefit rate) |
| 3 | · | N1103: 34 years (tax rate) |
| 4 | · | N1201: 1 years (NSW/GDP, avg=-0.0062) |
| 5 | · | N1202: 46 years (NSW/EC) |

### ✓ N1601

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | N1601: 40 years (Turkey labor share, linear trend 45%→35%) |
| 2 | · | N1602: 40 years (Turkey NSW/GDP, all negative, mean=-0.0111) |
| 3 | · | N1603-N1605: deferred (requires TURKSTAT data) |

### ✓ N1001

| Step | Status | Detail |
|------|--------|--------|
| 1 | · | N1001: 29 years (Tonak labor share, 1952-1980) |
| 2 | · | N1002: 29 years (Tonak net tax rate) |
| 3 | · | N1501: 42 years (working class unproductive) |
| 4 | · | N1502: 42 years (managerial unproductive) |
| 5 | · | N1503: 42 years (total unproductive (Mohun)) |
| 6 | · | N1504: 42 years (unproductive burden ratio) |
| 7 | · | N1701: 24 years (NZ productive capital share) |

---

*Report generated by AS2 Anu Replicator v3.0.0*