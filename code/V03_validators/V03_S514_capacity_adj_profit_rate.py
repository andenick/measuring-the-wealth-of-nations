"""V03_S514 - Validate r*' against the BOOK'S OWN r*' (Table 5.8), DIVIDE form.

D1 DECISION (2026-07-02): S514 now implements r*' = r*/u (divide), matching the
book. Benchmarks are therefore the book's own r*' row (MWoN Table 5.8, KB v2
_combined/5.8.csv), NOT the deprecated multiply-by-TCU anchors.

Two honesty features:
  1. Internal-consistency check: S514-A == S513-A / u_book to numerical
     precision (the divide relationship actually holds).
  2. Registered-divergence years: the build's r* = S*/(K_net + V*) differs from
     the book's r* = S*/K*_gross (the S517 gross-vs-net / 1987-vintage gap, D2 /
     DIV-A15 and the D1 divergence patch). In later book years this pushes S514-A
     modestly above book r*' beyond the 0.01 rate tolerance. Those years are
     listed in KNOWN_DIVERGENCE_YEARS and reported as status DIVERGENCE (surfaced,
     documented) rather than a hard FAIL — per the D1 directive "V03 must PASS
     against book benchmarks (or any residual = registered divergence)."
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S514_capacity_adj_profit_rate import load_book_u  # noqa: E402
from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_variant_reference_values  # noqa: E402
from utils.series import TOLERANCES  # noqa: E402


def _variant_book_checks(subseries: str, tol_class: str) -> list[dict]:
    """Book-anchored check of the GROSS r*' variant vs the book's printed cells.

    K-plan WP-K3: S514-GROSS-A is the book's OWN published r*' (r*_gross/u). All
    residuals are within the rate tolerance — no DIVERGENCE bucket needed (unlike
    the net S514-A), which is precisely the point: the gross variant is
    book-faithful by construction. Returns [] when absent.
    """
    refs = get_variant_reference_values("S514", subseries)
    if not refs:
        return []
    full = pd.read_csv(DATA_FINAL / "S514.csv")
    v = full[full["series_id"] == subseries]
    by_year = dict(zip(v["year"].astype(int), v["value"].astype(float)))
    tol = TOLERANCES[tol_class]
    checks = []
    for yr, expected in sorted(refs.items()):
        actual = by_year.get(yr)
        if actual is None:
            checks.append({"year": yr, "expected": expected, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        ok = (abs_err <= tol["abs"]) or (rel_err <= tol["rel"])
        checks.append({"year": yr, "expected": expected, "actual": round(actual, 6),
                       "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
                       "status": "PASS" if ok else "FAIL"})
    return checks


# Book r*' (= r*/u), MWoN Table 5.8 row "r*' = profit rate adjusted for
# utilization = r*/u" (KB v2 _combined/5.8.csv), benchmark years.
BOOK_RPRIME_BENCHMARKS = {1948: 0.52, 1958: 0.47, 1967: 0.42, 1980: 0.36, 1989: 0.39}

# Years whose residual vs book r*' is a REGISTERED divergence (build r*=S*/(K_net+V*)
# vs book r*=S*/K*_gross; see D1_DIV_PATCHES.json + DIV-A15). Reported, not failed.
KNOWN_DIVERGENCE_YEARS = {1958, 1980, 1989}


def run():
    df = pd.read_csv(DATA_FINAL / "S514.csv")
    a = df[df["series_id"] == "S514-A"]
    valid = a.dropna(subset=["value"])

    # (1) Internal consistency: S514-A == S513-A / u_book
    s513 = pd.read_csv(DATA_FINAL / "S513.csv")
    s513a = s513[s513["series_id"] == "S513-A"][["year", "value"]].rename(columns={"value": "r_star"})
    u = load_book_u()
    check = valid.merge(s513a, on="year").merge(u, on="year")
    check["expected"] = check["r_star"] / check["u"]
    divide_holds = bool((abs(check["value"] - check["expected"]) < 1e-9).all())

    # (2) Book r*' benchmark checks
    tol = TOLERANCES["rate_series"]
    by_year = dict(zip(valid["year"].astype(int), valid["value"].astype(float)))
    bench_checks = []
    for yr, expected in BOOK_RPRIME_BENCHMARKS.items():
        actual = by_year.get(yr)
        if actual is None:
            bench_checks.append({"year": yr, "expected": expected, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        within = (abs_err <= tol["abs"]) or (rel_err <= tol["rel"])
        if within:
            status = "PASS"
        elif yr in KNOWN_DIVERGENCE_YEARS:
            status = "DIVERGENCE"
        else:
            status = "FAIL"
        bench_checks.append({
            "year": yr, "expected": expected, "actual": round(actual, 6),
            "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
            "status": status,
        })
    n_pass = sum(1 for c in bench_checks if c["status"] == "PASS")
    n_div  = sum(1 for c in bench_checks if c["status"] == "DIVERGENCE")
    n_fail = sum(1 for c in bench_checks if c["status"] == "FAIL")
    n_miss = sum(1 for c in bench_checks if c["status"] == "MISSING")

    # Book-anchored GROSS variant check (K-plan WP-K3; independent book anchor)
    variant_checks = _variant_book_checks("S514-GROSS-A", "rate_series")
    n_var_pass = sum(1 for c in variant_checks if c["status"] == "PASS")
    n_var_fail = sum(1 for c in variant_checks if c["status"] == "FAIL")

    status = "PASS" if (divide_holds and len(valid) > 0 and n_fail == 0 and n_miss == 0 and n_var_fail == 0) else "FAIL"
    result = {
        "series_id": "S514",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "rel_tol": tol["rel"], "abs_tol": tol["abs"],
        "status": status,
        "n_pass": n_pass, "n_divergence": n_div, "n_fail": n_fail, "n_missing": n_miss,
        "checks": {
            "divide_relationship_holds": divide_holds,
            "operation": "r*' = r*/u (DIVIDE) per book Table 5.8",
            "n_valid_years": int(len(valid)),
            "known_divergence_years": sorted(KNOWN_DIVERGENCE_YEARS),
        },
        "benchmarks": {"source": "MWoN Table 5.8 r*' row", "checks": bench_checks},
        "variant_book_anchor": {
            "subseries": "S514-GROSS-A",
            "source": "book Table 5.8 published r*' (r*_gross/u); independent (non-tautological) anchor, no divergence bucket",
            "n_pass": n_var_pass, "n_fail": n_var_fail, "checks": variant_checks,
        },
    }
    write_validation_result("S514", result)
    print(f"    [V03_S514] status={status} divide_ok={divide_holds} "
          f"valid_years={len(valid)} bench: {n_pass} PASS / {n_div} DIVERGENCE / {n_fail} FAIL / {n_miss} MISS "
          f"| gross_book_anchor={n_var_pass}/{n_var_pass + n_var_fail}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
