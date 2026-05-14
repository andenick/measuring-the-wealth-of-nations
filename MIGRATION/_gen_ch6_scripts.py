"""Generate explicit L01/P02/V03 scripts for Ch6 NSW series S601-S609.

Each generated file is real, hand-readable Python that an auditor can read
in isolation. The generator just removes the boilerplate from writing 27
near-identical files. After this runs once, the generated files are checked
into the repo and edited directly going forward.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path("D:/Arcanum/Projects/RMWND/Technical")
L_DIR = ROOT / "code" / "L01_loaders"
P_DIR = ROOT / "code" / "P02_processors"
V_DIR = ROOT / "code" / "V03_validators"


# ------------------------- Per-series specs -------------------------

# Each spec: (series_id, slug, name, source_file, source_column,
#             units, unit_scale, tolerance_class, benchmarks_dict)
#
# Benchmarks for Ch6 are not in validation_config.json — they're verified
# round-trip against the source CSV row values.

SPECS = [
    ("S601", "personal_tax_workers", "Personal Tax Workers",
     "Table6_1_TaxAccounts.csv", "personal_income_tax_workers",
     "billions_usd", 1000.0, "dollar_series",
     {1952: 22.7849, 1989: 385.7297}),

    ("S602", "social_insurance_workers", "Social Insurance Tax Workers",
     "Table6_1_TaxAccounts.csv", "social_insurance_workers",
     "billions_usd", 1000.0, "dollar_series",
     {1952: 6.923, 1989: 385.231}),

    ("S603", "property_tax_workers", "Property Tax Workers",
     "Table6_1_TaxAccounts.csv", "property_tax_workers",
     "billions_usd", 1000.0, "dollar_series",
     {1952: 4.1925, 1989: 74.9315}),

    ("S604", "total_tax_workers", "Total Tax Workers (T_w)",
     "Table6_1_TaxAccounts.csv", "total_tax_workers",
     "billions_usd", 1000.0, "dollar_series",
     {1952: 53.2083, 1989: 1116.8898}),

    ("S605", "benefits_workers", "Government Benefits to Workers (B_w)",
     "Table6_2_BenefitAccounts.csv", "total_benefits",
     "billions_usd", 1000.0, "dollar_series",
     {1952: 10.994, 1989: 521.07}),

    ("S606", "govt_services_workers", "Government Services Workers (G_w)",
     "Table6_2_BenefitAccounts.csv", "govt_services_workers",
     "billions_usd", 1000.0, "dollar_series",
     {1952: 32.6949, 1989: 494.8035}),

    ("S607", "net_social_wage", "Net Social Wage (NSW = B_w + G_w - T_w)",
     "Table6_3_NetSocialWage.csv", "nsw",
     "billions_usd", 1000.0, "dollar_series",
     {1952: -9.5194, 1989: -101.0163}),

    ("S609", "nsw_ni_share", "NSW / National Income Share",
     "Table6_3_NetSocialWage.csv", "nsw_ni_share",
     "share", 1.0, "share_series",
     {1952: -0.0337, 1989: -0.0219}),
]


LOADER_TPL = '''"""L01_{sid} — Load {name}, book period (Ch6 NSW).

Source: Appendix Ch6 — `data/source/book_tables/{source_file}`, column
`{source_column}`. {unit_note}

Status: book_period (S607 has extension via Table6_3_Extended; others are
book-only).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "{sid}",
    subseries_id  = "{sid}-A",
    source_file   = BOOK_TABLES / "{source_file}",
    source_column = "{source_column}",
    units         = "{units}",
    unit_scale    = {unit_scale},
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


PROCESSOR_TPL = '''"""P02_{sid} — Process {name}; pass-through for book period."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_{sid}_{slug} import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "{source_file}:{source_column}")
    print(f"    [P02_{sid}] wrote {{final_path.name}}")


if __name__ == "__main__":
    run()
'''


VALIDATOR_TPL = '''"""V03_{sid} — Validate {name} against book benchmark values."""
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


for sid, slug, name, src_file, src_col, units, scale, tol, benchmarks in SPECS:
    unit_note = (
        f"Source values in MILLIONS; loader divides by {int(scale)} for "
        f"BILLIONS output, matching the registry's `units: {units}`."
        if scale != 1.0 else
        f"Source values already in {units}; no unit conversion."
    )
    (L_DIR / f"L01_{sid}_{slug}.py").write_text(LOADER_TPL.format(
        sid=sid, name=name, source_file=src_file, source_column=src_col,
        units=units, unit_scale=scale, unit_note=unit_note,
    ), encoding="utf-8")
    (P_DIR / f"P02_{sid}_{slug}.py").write_text(PROCESSOR_TPL.format(
        sid=sid, slug=slug, name=name, source_file=src_file, source_column=src_col,
    ), encoding="utf-8")
    (V_DIR / f"V03_{sid}_{slug}.py").write_text(VALIDATOR_TPL.format(
        sid=sid, name=name, tol_class=tol,
        benchmarks=repr(benchmarks),
    ), encoding="utf-8")
    print(f"  Wrote L01_{sid}_{slug}.py, P02_..., V03_...")


# S608 is derived (NSW / V*) — write explicit derived processor + validator
S608_PROC = '''"""P02_S608 — Compute NSW/V* ratio from S607 (NSW) and S504 (Variable Capital).

A derived ratio. No L01 loader: reads final/S607.csv and final/S504.csv
directly. The ratio sign indicates whether workers receive net transfers
from the state (positive) or subsidize it (negative).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S608"
SUBSERIES = "S608-A"


def compute() -> pd.DataFrame:
    s607 = pd.read_csv(DATA_FINAL / "S607.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s607 = s607[s607["series_id"] == "S607-A"][["year", "value"]].rename(columns={"value": "NSW"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    merged = s607.merge(s504, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["NSW"] / merged["V_star"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "ratio"
    merged["stage"] = "book_period"
    merged["provenance"] = "S607 / S504"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
'''
S608_VAL = '''"""V03_S608 — Validate NSW/V* ratio (round-trip via S607 and S504)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.io import write_validation_result  # noqa: E402


SERIES_ID = "S608"


def run():
    s607 = pd.read_csv(DATA_FINAL / "S607.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s608 = pd.read_csv(DATA_FINAL / "S608.csv")
    s607 = s607[s607["series_id"] == "S607-A"][["year", "value"]].rename(columns={"value": "NSW"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    s608 = s608[s608["series_id"] == "S608-A"][["year", "value"]].rename(columns={"value": "ratio"})

    overlap = s607.merge(s504, on="year").merge(s608, on="year")
    overlap["implied"] = overlap["NSW"] / overlap["V_star"]
    overlap["abs_err"] = (overlap["implied"] - overlap["ratio"]).abs()

    max_err = float(overlap["abs_err"].max()) if len(overlap) else None
    status = "PASS" if (max_err is None or max_err < 1e-6) else "FAIL"

    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "identity_check": {
            "identity": "S608 = S607 / S504 (NSW / V*)",
            "compared_years": len(overlap),
            "max_abs_err": max_err,
        },
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} identity_check max_err={max_err}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
'''

(P_DIR / "P02_S608_nsw_v_star_ratio.py").write_text(S608_PROC, encoding="utf-8")
(V_DIR / "V03_S608_nsw_v_star_ratio.py").write_text(S608_VAL, encoding="utf-8")
print("  Wrote P02_S608_nsw_v_star_ratio.py + V03_S608 (derived)")

print()
print("Done: 8 series with full L+P+V trios + 1 derived (S608) processor/validator.")
print("Run order: S601, S602, S603, S604, S605, S606, S607, S609, then S608 (depends on S607+S504).")
