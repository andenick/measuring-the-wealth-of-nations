"""Sprint 1 generator: S617 (EC), ES1501-1504 (Mohun 2013), ES1101-1103 (ST 1987 derived)."""
from __future__ import annotations
from pathlib import Path

L_DIR = Path("D:/Arcanum/Projects/RMWND/Technical/code/L01_loaders")
P_DIR = Path("D:/Arcanum/Projects/RMWND/Technical/code/P02_processors")
V_DIR = Path("D:/Arcanum/Projects/RMWND/Technical/code/V03_validators")


# === S617 EC (Employee Compensation) - new series from H.1 ===
S617_L = '''"""L01_S617 — Load Employee Compensation (EC) from Appendix H.1.

EC is the total wage bill (productive + unproductive labor) — the denominator
for ST 1987 and ST 2002 NSW ratios (ES1101-1103, ES1201-1202).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader

LOADER = BookColumnLoader(
    series_id="S617", subseries_id="S617-A",
    source_file=BOOK_TABLES / "book_tableH1_1948_1989.csv",
    source_column="EC",
    units="billions_usd", unit_scale=1.0,
)

def run():
    df = LOADER.load()
    print(f"    [L01_S617] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.2f}, last={df.iloc[-1]['value']:.2f}")
    return df

if __name__ == "__main__":
    run()
'''

S617_P = '''"""P02_S617 — Employee Compensation pass-through."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S617_employee_compensation import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402

def run():
    final_path = run_pipeline_for_series(LOADER, "book_tableH1_1948_1989.csv:EC")
    print(f"    [P02_S617] wrote {final_path.name}")

if __name__ == "__main__":
    run()
'''

S617_V = '''"""V03_S617 — Validate EC against H.1 row values."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL
from utils.series import BenchmarkValidator

VALIDATOR = BenchmarkValidator(
    series_id="S617", tolerance_class="dollar_series",
    benchmarks={1948: 142.09, 1989: 3145.41},
    subseries_filter="S617-A",
)

def run():
    result = VALIDATOR.run(DATA_FINAL / "S617.csv")
    print(f"    [V03_S617] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
'''

(L_DIR / "L01_S617_employee_compensation.py").write_text(S617_L, encoding="utf-8")
(P_DIR / "P02_S617_employee_compensation.py").write_text(S617_P, encoding="utf-8")
(V_DIR / "V03_S617_employee_compensation.py").write_text(S617_V, encoding="utf-8")
print("Wrote S617 (EC) trio")


# === ES1501-1503: direct column from Mohun decomposition ===
MOHUN_SPECS = [
    ("ES1501", "working_class_unproductive_mohun2013", "Working Class Unproductive Labor (Mohun 2013)", "Luw_mohun",
     {1948: 6426.4746, 1989: None}),
    ("ES1502", "managerial_unproductive_mohun2013", "Managerial Unproductive Labor (Mohun 2013)", "Lum_mohun",
     {1948: 7669.3547, 1989: None}),
    ("ES1503", "total_unproductive_mohun2013", "Total Unproductive Labor (Mohun 2013)", "Lu_mohun",
     {1948: 14095.8293, 1989: None}),
]

ES_DIRECT_L = '''"""L01_{sid} — Load {name}.

Source: Mohun_unproductive_decomposition_1948_1989.csv, column `{col}`.
Units: thousands of workers under Mohun's narrow productive classification.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES
from utils.series import BookColumnLoader

LOADER = BookColumnLoader(
    series_id="{sid}", subseries_id="{sid}-A",
    source_file=EXTERNAL_STUDIES / "Mohun_unproductive_decomposition_1948_1989.csv",
    source_column="{col}",
    units="thousands", unit_scale=1.0,
)

def run():
    df = LOADER.load()
    print(f"    [L01_{sid}] loaded {{len(df)}} rows; "
          f"period {{df['year'].min()}}-{{df['year'].max()}}; "
          f"first={{df.iloc[0]['value']:.0f}}, last={{df.iloc[-1]['value']:.0f}}")
    return df

if __name__ == "__main__":
    run()
'''

ES_DIRECT_P = '''"""P02_{sid} — {name} pass-through."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_{sid}_{slug} import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402

def run():
    final_path = run_pipeline_for_series(LOADER, "Mohun_unproductive_decomposition_1948_1989.csv:{col}")
    print(f"    [P02_{sid}] wrote {{final_path.name}}")

if __name__ == "__main__":
    run()
'''

ES_DIRECT_V = '''"""V03_{sid} — Validate {name}."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL
from utils.series import BenchmarkValidator

VALIDATOR = BenchmarkValidator(
    series_id="{sid}", tolerance_class="level_series",
    benchmarks={benchmarks},
    subseries_filter="{sid}-A",
)

def run():
    result = VALIDATOR.run(DATA_FINAL / "{sid}.csv")
    print(f"    [V03_{sid}] status={{result['status']}} bench_pass={{result['n_pass']}}/{{result['n_pass']+result['n_fail']+result['n_missing']}}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
'''

for sid, slug, name, col, bm in MOHUN_SPECS:
    bm_clean = {k: v for k, v in bm.items() if v is not None}
    (L_DIR / f"L01_{sid}_{slug}.py").write_text(
        ES_DIRECT_L.format(sid=sid, name=name, col=col), encoding="utf-8")
    (P_DIR / f"P02_{sid}_{slug}.py").write_text(
        ES_DIRECT_P.format(sid=sid, slug=slug, name=name, col=col), encoding="utf-8")
    (V_DIR / f"V03_{sid}_{slug}.py").write_text(
        ES_DIRECT_V.format(sid=sid, name=name, benchmarks=repr(bm_clean)), encoding="utf-8")
    print(f"Wrote {sid} trio ({col})")


# === ES1504 derived = Lu / Lp ratio ===
ES1504_P = '''"""P02_ES1504 — Compute Lu/Lp burden ratio (Mohun 2013).

ES1504 = Mohun's Lu (S1503) / Mohun's Lp (from mohun_employment_annual_1948_1989.csv).
The "unproductive burden" — how many unproductive workers per productive worker.

Book finding: burden ratio rises from ~0.77 (1948) to higher in later years.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import read_book_table, write_series_csv
from utils.paths import DATA_FINAL, EXTERNAL_STUDIES

SERIES_ID = "ES1504"
SUBSERIES = "ES1504-A"

def compute() -> pd.DataFrame:
    es1503 = pd.read_csv(DATA_FINAL / "ES1503.csv")
    es1503 = es1503[es1503["series_id"] == "ES1503-A"][["year", "value"]].rename(columns={"value": "Lu"})
    # Get Lp from Mohun employment annual
    mohun_emp = read_book_table(EXTERNAL_STUDIES / "Mohun_mohun_employment_annual_1948_1989.csv")
    lp = mohun_emp[["year", "Lp_mohun"]].rename(columns={"Lp_mohun": "Lp"})
    merged = es1503.merge(lp, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["Lu"] / merged["Lp"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "share"
    merged["stage"] = "analytical_derivation"
    merged["provenance"] = "ES1503 / Mohun Lp_mohun"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]

def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_ES1504] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df

if __name__ == "__main__":
    run()
'''

ES1504_V = '''"""V03_ES1504 — Validate Lu/Lp ratio range."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    df = pd.read_csv(DATA_FINAL / "ES1504.csv")
    df = df[df["series_id"] == "ES1504-A"]
    # Burden ratio: expect 0.5 to 2.0 over the period
    in_range = bool(df["value"].between(0.5, 2.0).all())
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": "ES1504",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series",
        "status": status, "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "range_check": {"expected": [0.5, 2.0], "actual_min": float(df["value"].min()), "actual_max": float(df["value"].max())},
    }
    write_validation_result("ES1504", result)
    print(f"    [V03_ES1504] status={status} range=[{df['value'].min():.4f}, {df['value'].max():.4f}]")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
'''

(P_DIR / "P02_ES1504_burden_ratio.py").write_text(ES1504_P, encoding="utf-8")
(V_DIR / "V03_ES1504_burden_ratio.py").write_text(ES1504_V, encoding="utf-8")
print("Wrote ES1504 derived processor + validator")


# === ES1101-1103: ST 1987 derived ratios ===
ES_ST87_SPECS = [
    ("ES1101", "net_transfer_rate", "Net Transfer Rate (S&T 1987)",
     "(S605 + S606 - S604) / S617", "S605+S606-S604", "/", "S617",
     # numerator = S605 + S606 - S604; denom = S617
    ),
    ("ES1102", "social_benefit_rate", "Social Benefit Rate (S&T 1987)",
     "(S605 + S606) / S617", "S605+S606", "/", "S617",
    ),
    ("ES1103", "social_tax_rate", "Social Tax Rate (S&T 1987)",
     "S604 / S617", "S604", "/", "S617",
    ),
]

ES_ST87_P = '''"""P02_{sid} — {name} (derived ratio).

Computed as {formula}.

Uses Ch6 NSW component series (S604/S605/S606) and S617 (Employee Compensation
from H.1). This is the Shaikh & Tonak (1987) framework — what fraction of
total compensation flows back to workers via the state in each direction.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv
from utils.paths import DATA_FINAL

SERIES_ID = "{sid}"
SUBSERIES = "{sid}-A"

def _load(sid: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_FINAL / f"{{sid}}.csv")
    return df[df["series_id"] == f"{{sid}}-A"][["year", "value"]].rename(columns={{"value": sid}})

def compute() -> pd.DataFrame:
    {load_lines}
    merged = {merge_chain}
    merged["value"] = {compute_expr}
    merged["series_id"] = SUBSERIES
    merged["units"] = "share"
    merged["stage"] = "analytical_derivation"
    merged["provenance"] = "{formula}"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]

def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{sid}] {{len(df)}} rows; first={{df.iloc[0]['value']:.4f}}, last={{df.iloc[-1]['value']:.4f}}; wrote {{final_path.name}}")
    return df

if __name__ == "__main__":
    run()
'''

ES_ST87_V = '''"""V03_{sid} — Range check for {name}."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    df = pd.read_csv(DATA_FINAL / "{sid}.csv")
    df = df[df["series_id"] == "{sid}-A"]
    # Range: ratios should be small (single-digit percent of EC, so 0.0x-0.5x)
    in_range = bool(df["value"].between(-1.0, 1.0).all())
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {{
        "series_id": "{sid}",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series",
        "status": status, "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "range_check": {{"expected": [-1.0, 1.0], "actual_min": float(df["value"].min()), "actual_max": float(df["value"].max())}},
    }}
    write_validation_result("{sid}", result)
    print(f"    [V03_{sid}] status={{status}} range=[{{df['value'].min():.4f}}, {{df['value'].max():.4f}}]")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
'''

# Per-series load/merge/compute strings
ES_LOGIC = {
    "ES1101": (
        '\n    '.join(["S605 = _load('S605')", "S606 = _load('S606')", "S604 = _load('S604')", "S617 = _load('S617')"]),
        "S605.merge(S606, on='year').merge(S604, on='year').merge(S617, on='year').sort_values('year').reset_index(drop=True)",
        "(merged['S605'] + merged['S606'] - merged['S604']) / merged['S617']",
    ),
    "ES1102": (
        '\n    '.join(["S605 = _load('S605')", "S606 = _load('S606')", "S617 = _load('S617')"]),
        "S605.merge(S606, on='year').merge(S617, on='year').sort_values('year').reset_index(drop=True)",
        "(merged['S605'] + merged['S606']) / merged['S617']",
    ),
    "ES1103": (
        '\n    '.join(["S604 = _load('S604')", "S617 = _load('S617')"]),
        "S604.merge(S617, on='year').sort_values('year').reset_index(drop=True)",
        "merged['S604'] / merged['S617']",
    ),
}

for sid, slug, name, formula, num, _op, denom in ES_ST87_SPECS:
    load_lines, merge_chain, compute_expr = ES_LOGIC[sid]
    (P_DIR / f"P02_{sid}_{slug}.py").write_text(
        ES_ST87_P.format(sid=sid, name=name, formula=formula,
                         load_lines=load_lines, merge_chain=merge_chain,
                         compute_expr=compute_expr),
        encoding="utf-8")
    (V_DIR / f"V03_{sid}_{slug}.py").write_text(
        ES_ST87_V.format(sid=sid, name=name), encoding="utf-8")
    print(f"Wrote {sid} derived processor + validator ({formula})")

print("\nDone.")
