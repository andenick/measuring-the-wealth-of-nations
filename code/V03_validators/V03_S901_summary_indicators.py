"""V03_S901 - summary indicators round-trip + registry anchors + composite stats.

Refactored 2026-05-23 per Decision 0008 (and 0002):
  - `validation.reference_values` carries year-keyed scalars for the headline
    'e' (exploitation rate, S506) column: {1948: 1.7, 1989: 2.44}.
  - `validation.derived_statistics` carries the legacy year+variable composite
    keys for the multi-column summary table (1948_LpL, 1948_VW, 1948_e,
    1989_LpL, 1989_VW, 1989_e, 1989_NSW_V).

S901 is a multi-column summary table. The headline finding (book Ch7 §7.1)
is e_1948=1.70 -> e_1989=2.44 (+44%); reference_values captures that on
column S901-A/e_S506. The wider 7 composite checks ride in derived_statistics
and exercise every populated column round-trip against its upstream source.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import (  # noqa: E402
    get_derived_statistics,
    get_reference_values,
)


SERIES_ID = "S901"
ANCHOR_TOL_ABS = 0.05  # registry anchor for e column (S506 round-trip)
COMPOSITE_TOL_ABS = 0.01  # tight for upstream round-trip

# Maps registry composite-key suffix -> S901 wide column -> upstream SID.
# The round-trip check derives its column set from this map: every summary
# column is validated by COMPONENT IDENTITY against its independent upstream
# data/final/<sid>.csv series (never against S901's own chopped output — this
# is the de-tautologising anchor; review 2026-07 workpackage D). r_S513 / r_adj_S514
# were added once S513/S514 were built (internal build-log item); NaN-only rows (S514 pre-1949,
# S608 pre-1952) are skipped by the notna() guard, not flagged.
COMPOSITE_KEY_MAP = {
    "e":     ("S901-A/e_S506",     "S506"),
    "LpL":   ("S901-A/LpL_S511",   "S511"),
    "VW":    ("S901-A/VW_S512",    "S512"),
    "NSW_V": ("S901-A/NSW_V_S608", "S608"),
    "r":     ("S901-A/r_S513",     "S513"),
    "r_adj": ("S901-A/r_adj_S514", "S514"),
}

# Column that the year-keyed reference_values anchors apply to (the headline
# exploitation-rate column).
ANCHOR_COLUMN = "S901-A/e_S506"


def run():
    s901 = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    wide = s901.pivot_table(
        index="year", columns="series_id", values="value", aggfunc="first"
    ).reset_index()

    # 1) Upstream round-trip check (every populated column vs its upstream)
    columns_to_check = {sd[0]: sd[1] for sd in COMPOSITE_KEY_MAP.values()}
    fails = []
    compared = 0
    for s901_col, upstream_id in columns_to_check.items():
        if s901_col not in wide.columns:
            continue
        upstream = pd.read_csv(DATA_FINAL / f"{upstream_id}.csv")
        upstream = upstream[upstream["series_id"] == f"{upstream_id}-A"][["year", "value"]]
        merged = wide[["year", s901_col]].merge(upstream, on="year", how="inner")
        merged["abs_err"] = (merged[s901_col] - merged["value"]).abs()
        bad = merged[(merged["abs_err"] > 1e-9) & merged[s901_col].notna()]
        compared += len(merged)
        if len(bad) > 0:
            fails.append({"column": s901_col, "fail_years": bad["year"].tolist(),
                          "max_abs_err": float(bad["abs_err"].max())})

    # 2) Registry year-keyed anchors (per Decision 0008) on the headline e column
    anchors = get_reference_values(SERIES_ID)
    anchor_checks = []
    for year, expected in anchors.items():
        if ANCHOR_COLUMN not in wide.columns:
            anchor_checks.append({"year": year, "expected": expected,
                                  "status": "MISSING",
                                  "note": f"anchor column {ANCHOR_COLUMN} not present"})
            continue
        row = wide[wide["year"] == year]
        if row.empty or pd.isna(row[ANCHOR_COLUMN].iloc[0]):
            anchor_checks.append({"year": year, "expected": expected,
                                  "status": "MISSING", "note": "no value for year"})
            continue
        actual = float(row[ANCHOR_COLUMN].iloc[0])
        abs_err = abs(actual - float(expected))
        anchor_checks.append({
            "year": year, "expected": expected, "actual": round(actual, 6),
            "abs_err": round(abs_err, 6),
            "status": "PASS" if abs_err <= ANCHOR_TOL_ABS else "FAIL",
        })
    n_anchor_fail = sum(1 for c in anchor_checks if c["status"] == "FAIL")
    n_anchor_miss = sum(1 for c in anchor_checks if c["status"] == "MISSING")

    # 3) Composite year+variable checks (per Decision 0008), DE-TAUTOLOGISED
    #    (review 2026-07 workpackage D). The registry `derived_statistics` scalars are
    #    frozen copies of a past chopped output — using them as the expectation
    #    is tautological AND goes stale when an upstream series is corrected
    #    (S608/Appendix N net-social-wage was rebuilt, so the frozen
    #    1989_NSW_V=-0.0837 no longer matches the canonical S608). The
    #    expectation is therefore taken from the LIVE UPSTREAM series
    #    (component identity); the registry scalar is retained only as
    #    `registry_frozen` and, when it disagrees with the upstream truth, the
    #    check is annotated `registry_stale` (a patch is emitted to refresh it)
    #    but PASS/FAIL is driven by the independent upstream value, never by the
    #    frozen scalar or S901's own chopped output.
    stats = get_derived_statistics(SERIES_ID)
    composite_checks = []
    for composite_key, registry_frozen in stats.items():
        if "_" not in str(composite_key):
            continue
        year_str, suffix = str(composite_key).split("_", 1)
        try:
            year = int(year_str)
        except ValueError:
            continue
        if suffix not in COMPOSITE_KEY_MAP:
            composite_checks.append({"key": composite_key,
                                     "registry_frozen": registry_frozen,
                                     "status": "SKIP",
                                     "note": f"unknown suffix {suffix!r}"})
            continue
        s901_col, upstream_id = COMPOSITE_KEY_MAP[suffix]
        if s901_col not in wide.columns:
            composite_checks.append({"key": composite_key,
                                     "registry_frozen": registry_frozen,
                                     "status": "MISSING",
                                     "note": f"column {s901_col} not present"})
            continue
        row = wide[wide["year"] == year]
        if row.empty or pd.isna(row[s901_col].iloc[0]):
            composite_checks.append({"key": composite_key,
                                     "registry_frozen": registry_frozen,
                                     "status": "MISSING", "note": "no value for year"})
            continue
        actual = float(row[s901_col].iloc[0])
        # Independent expectation = live upstream series value for this year.
        upstream = pd.read_csv(DATA_FINAL / f"{upstream_id}.csv")
        upstream = upstream[upstream["series_id"] == f"{upstream_id}-A"]
        urow = upstream[upstream["year"] == year]
        if urow.empty or pd.isna(urow["value"].iloc[0]):
            composite_checks.append({"key": composite_key,
                                     "registry_frozen": registry_frozen,
                                     "actual": round(actual, 6),
                                     "status": "MISSING",
                                     "note": f"no upstream {upstream_id}-A value for year"})
            continue
        expected = float(urow["value"].iloc[0])
        abs_err = abs(actual - expected)
        registry_stale = (registry_frozen is not None
                          and abs(float(registry_frozen) - expected) > COMPOSITE_TOL_ABS)
        composite_checks.append({
            "key": composite_key,
            "expected_upstream": round(expected, 6),
            "actual": round(actual, 6),
            "abs_err": round(abs_err, 6),
            "registry_frozen": registry_frozen,
            "registry_stale": registry_stale,
            "anchor": f"component identity vs {upstream_id}-A",
            "status": "PASS" if abs_err <= COMPOSITE_TOL_ABS else "FAIL",
        })
    n_comp_pass = sum(1 for c in composite_checks if c["status"] == "PASS")
    n_comp_stale = sum(1 for c in composite_checks if c.get("registry_stale"))
    n_comp_fail = sum(1 for c in composite_checks if c["status"] == "FAIL")
    n_comp_miss = sum(1 for c in composite_checks if c["status"] == "MISSING")

    n_total_rows = len(s901)
    n_pending = int(s901["value"].isna().sum())

    ok = (not fails and n_anchor_fail == 0 and n_anchor_miss == 0
          and n_comp_fail == 0 and n_comp_miss == 0)
    status = "PASS" if ok else "FAIL"

    result = {
        "series_id":       SERIES_ID,
        "run_at":          datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status":          status,
        "n_pass":          (sum(1 for c in anchor_checks if c["status"] == "PASS")
                            + n_comp_pass),
        "n_fail":          len(fails) + n_anchor_fail + n_comp_fail,
        "n_missing":       n_anchor_miss + n_comp_miss,
        "round_trip_check": {
            "compared_pairs":     compared,
            "fails":              fails,
            "rows_pending_K_TCU": n_pending,
            "rows_total":         n_total_rows,
        },
        "anchors":             {"checks": anchor_checks,
                                "column": ANCHOR_COLUMN},
        "derived_statistics":  {"checks": composite_checks,
                                "anchor_basis": "live_upstream_component_identity",
                                "n_registry_stale": n_comp_stale},
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} round_trip_pairs={compared} pending={n_pending}/{n_total_rows} anchors={sum(1 for c in anchor_checks if c['status']=='PASS')}/{len(anchor_checks)} composite={n_comp_pass}/{len(composite_checks)} registry_stale={n_comp_stale}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
