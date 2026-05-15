"""Generate L01/P02/V03 scripts for Wave 4 — external-study replications.

Implements 10 of 25 ES series with clean source data:
- ES1001-1002 (Tonak 1984)
- ES1401-1404 (Mohun 2005)
- ES1701-1704 (Cronin 2001 NZ)

The other 15 (ST 1987, ST 2002, Moos 2017, Mohun 2013, Karabacak 2022)
get pending stub DPRs.
"""
from __future__ import annotations

from pathlib import Path

L_DIR = Path("D:/Arcanum/Projects/RMWND/Technical/code/L01_loaders")
P_DIR = Path("D:/Arcanum/Projects/RMWND/Technical/code/P02_processors")
V_DIR = Path("D:/Arcanum/Projects/RMWND/Technical/code/V03_validators")
EXT   = Path("data/source/external_studies")  # relative to ROOT for utils.paths

# Per-series specs: column-from-file load.
# (sid, slug, name, source_file_basename, source_column, units, scale,
#  tol_class, benchmarks)
SPECS_DIRECT = [
    # ----- Tonak 1984 -----
    ("ES1001", "labor_share_tonak1984",
     "Labor Share of National Taxes (Tonak 1984)",
     "Tonak1984_table_V_taxes_labor_nonlabor_1952_1980.csv",
     "labor_taxes",
     "billions_usd", 1.0, "dollar_series",
     {1952: 34.58, 1980: 538.65}),  # endpoints from CSV head/tail
    ("ES1002", "net_tax_tonak1984",
     "Net Tax on Labor (Tonak 1984)",
     "Tonak1984_table_X_net_tax_1952_1980.csv",
     "net_tax",
     "billions_usd", 1.0, "dollar_series",
     {1952: 16.02}),  # 1980 endpoint to be discovered

    # ----- Mohun 2005 -----
    ("ES1401", "exploitation_rate_mohun2005",
     "Exploitation Rate — Mohun Classification (Mohun 2005)",
     "Mohun_mohun_exploitation_rates_1948_1989_CORRECTED.csv",
     "e_mohun",
     "ratio", 1.0, "rate_series",
     {1948: 1.6666, 1989: None}),  # endpoint TBD from CSV; None ⇒ skip
    ("ES1402", "productive_labor_share_mohun2005",
     "Productive Labor Share — Mohun Classification (Mohun 2005)",
     "Mohun_mohun_employment_annual_1948_1989.csv",
     "Lp_mohun_L_ratio",
     "share", 1.0, "share_series",
     {1948: 0.5662}),
    ("ES1403", "variable_capital_mohun2005",
     "Variable Capital — Mohun Classification (Mohun 2005)",
     "Mohun_mohun_variable_capital_1948_1989_CORRECTED.csv",
     "V_star_mohun",
     "ratio", 1.0, "rate_series",  # tolerance class
     {1948: 1112758.197}),

    # ----- Cronin 2001 NZ -----
    ("ES1701", "nz_surplus_share_cronin2001",
     "NZ Surplus Share of Total Value (Cronin 2001)",
     "Cronin2001_cronin_table2_ratios_1972_1995.csv",
     "surplus_share_of_total_value_pct",
     "percent", 1.0, "share_series",
     {1972: 34}),
    ("ES1702", "nz_rate_surplus_value_cronin2001",
     "NZ Rate of Surplus Value (Cronin 2001)",
     "Cronin2001_cronin_table2_ratios_1972_1995.csv",
     "rate_of_surplus_value_pct",
     "percent", 1.0, "share_series",
     {1972: 206}),
    ("ES1703", "nz_value_composition_cronin2001",
     "NZ Value Composition of Capital (Cronin 2001)",
     "Cronin2001_cronin_table2_ratios_1972_1995.csv",
     "value_composition_of_capital_pct",
     "percent", 1.0, "share_series",
     {1972: 293}),
    ("ES1704", "nz_total_value_cronin2001",
     "NZ Total Value (Cronin 2001)",
     "Cronin2001_cronin_table1_nzsna_classical_1972_1995.csv",
     "total_value_mNZD",
     "millions_nzd", 1.0, "dollar_series",
     {1972: 10423}),
]


LOADER_TPL = '''"""L01_{sid} — Load {name}, external study (Wave 4).

Source: external_studies/{src_file}, column `{src_col}`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "{sid}",
    subseries_id  = "{sid}-A",
    source_file   = EXTERNAL_STUDIES / "{src_file}",
    source_column = "{src_col}",
    units         = "{units}",
    unit_scale    = {scale},
)


def run():
    df = LOADER.load()
    print(f"    [L01_{sid}] loaded {{len(df)}} rows; "
          f"period {{df['year'].min()}}-{{df['year'].max()}}; "
          f"first={{df.iloc[0]['value']:.4f}}, last={{df.iloc[-1]['value']:.4f}}")
    return df


if __name__ == "__main__":
    run()
'''


PROCESSOR_TPL = '''"""P02_{sid} — Process {name}; pass-through."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_{sid}_{slug} import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "{src_file}:{src_col}")
    print(f"    [P02_{sid}] wrote {{final_path.name}}")


if __name__ == "__main__":
    run()
'''


VALIDATOR_TPL = '''"""V03_{sid} — Validate {name}."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "{sid}",
    tolerance_class  = "{tol_class}",
    benchmarks       = {benchmarks},
    subseries_filter = "{sid}-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "{sid}.csv")
    print(f"    [V03_{sid}] status={{result['status']}} bench_pass={{result['n_pass']}}/{{result['n_pass']+result['n_fail']+result['n_missing']}}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
'''


for sid, slug, name, src_file, src_col, units, scale, tol, benchmarks in SPECS_DIRECT:
    # Drop None benchmarks
    benchmarks = {k: v for k, v in benchmarks.items() if v is not None}
    (L_DIR / f"L01_{sid}_{slug}.py").write_text(LOADER_TPL.format(
        sid=sid, name=name, src_file=src_file, src_col=src_col,
        units=units, scale=scale,
    ), encoding="utf-8")
    (P_DIR / f"P02_{sid}_{slug}.py").write_text(PROCESSOR_TPL.format(
        sid=sid, slug=slug, name=name, src_file=src_file, src_col=src_col,
    ), encoding="utf-8")
    (V_DIR / f"V03_{sid}_{slug}.py").write_text(VALIDATOR_TPL.format(
        sid=sid, name=name, tol_class=tol, benchmarks=repr(benchmarks),
    ), encoding="utf-8")
    print(f"  Wrote L01/P02/V03 for {sid}")


# ES1404 = derived (S506 / ES1401 ratio)
ES1404_PROC = '''"""P02_ES1404 — Compute ST/Mohun Exploitation Rate Ratio.

ES1404 = S506 (book e) / ES1401 (Mohun e). A cross-classification sensitivity
metric: how much does the productive/unproductive boundary choice affect the
headline exploitation finding?
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "ES1404"
SUBSERIES = "ES1404-A"


def compute() -> pd.DataFrame:
    s506    = pd.read_csv(DATA_FINAL / "S506.csv")
    es1401  = pd.read_csv(DATA_FINAL / "ES1401.csv")
    s506    = s506[s506["series_id"] == "S506-A"][["year","value"]].rename(columns={"value":"e_ST"})
    es1401  = es1401[es1401["series_id"] == "ES1401-A"][["year","value"]].rename(columns={"value":"e_Mohun"})
    merged  = s506.merge(es1401, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["e_ST"] / merged["e_Mohun"]
    merged["series_id"]  = SUBSERIES
    merged["units"]      = "ratio"
    merged["stage"]      = "cross_validation"
    merged["provenance"] = "S506 / ES1401"
    return merged[["series_id","year","value","units","stage","provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
'''
ES1404_VAL = '''"""V03_ES1404 — Validate ST/Mohun exploitation ratio range check."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "ES1404"


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    df = df[df["series_id"] == "ES1404-A"]
    # Range check: ST exploitation rate should be 0.7x to 1.5x Mohun's (book finding)
    in_range = df["value"].between(0.7, 1.5).all()
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "range_check": {
            "expected_range": [0.7, 1.5],
            "actual_min": float(df["value"].min()) if len(df) else None,
            "actual_max": float(df["value"].max()) if len(df) else None,
            "n_rows": len(df),
        },
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} range=[{df['value'].min():.3f}, {df['value'].max():.3f}]")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
'''
(P_DIR / "P02_ES1404_st_mohun_ratio.py").write_text(ES1404_PROC, encoding="utf-8")
(V_DIR / "V03_ES1404_st_mohun_ratio.py").write_text(ES1404_VAL, encoding="utf-8")
print("  Wrote P02_ES1404 + V03_ES1404 (derived)")

print("\nDone: 10 ES series generated (9 direct-column + 1 derived).")
