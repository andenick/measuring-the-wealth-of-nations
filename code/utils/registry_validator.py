"""Registry-backed benchmark loader for V03 validators.

Created 2026-05-24 per Decision 0002 (registry is the canonical source of truth
for `validation.reference_values`). The hyper-review flagged hardcoded benchmark
dicts inside V03 validator scripts as brittle: any change to the registry would
silently diverge from the validator's expectations. Routing every V03 through
`get_reference_values()` keeps both sides in lockstep.

Usage from a V03 script:

    from utils.registry_validator import get_reference_values
    benchmarks = get_reference_values("S506")  # -> {1948: 1.70, 1958: 2.01, ...}

The function:
- Loads `Technical/series_registry.json` once per process (cached).
- Reads `series[<SID>].validation.reference_values`.
- Coerces year keys to `int` and values to `float`.
- Filters out non-year keys (e.g., `1948_e` composite keys used by S901).
- Raises a clear KeyError if the series or its reference_values are missing.

NEVER write to the registry from this module. It is read-only.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

# Project layout: this file lives at Technical/code/utils/registry_validator.py
# Registry lives at Technical/series_registry.json
_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "series_registry.json"


@lru_cache(maxsize=1)
def _load_registry() -> dict:
    if not _REGISTRY_PATH.exists():
        raise FileNotFoundError(
            f"series_registry.json not found at {_REGISTRY_PATH}"
        )
    with _REGISTRY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _series_block(sid: str) -> dict:
    reg = _load_registry()
    series = reg.get("series", {})
    if sid not in series:
        raise KeyError(f"Series {sid!r} not found in series_registry.json")
    return series[sid]


def get_reference_values(sid: str, *, year_keys_only: bool = True) -> dict[int, float]:
    """Return the benchmark dict for a series from the registry.

    Args:
        sid: Canonical series ID (e.g., "S506").
        year_keys_only: If True (default), only include keys parseable as int
            years. Set False to keep composite keys like "1948_e" (S901 case).

    Returns:
        dict mapping int year -> float value. May be empty if the series carries
        no reference values (returns empty dict, not error, to allow validators
        that don't rely on benchmarks).
    """
    block = _series_block(sid)
    validation = block.get("validation") or {}
    raw = validation.get("reference_values")
    if raw is None:
        return {}

    out: dict[int, float] = {}
    composite: dict[str, float] = {}
    for k, v in raw.items():
        try:
            year = int(k)
        except (ValueError, TypeError):
            if not year_keys_only:
                composite[k] = float(v)
            continue
        out[year] = float(v)

    if year_keys_only:
        return out
    # When composite keys are kept, return them merged into a str-keyed dict
    merged: dict = {**{str(y): v for y, v in out.items()}, **composite}
    return merged  # type: ignore[return-value]


def get_variant_reference_values(sid: str, subseries: str) -> dict[int, float]:
    """Return book-anchored reference values for a named variant subseries.

    Reads ``series[<SID>].validation.variant_reference_values[<subseries>]``
    (K-plan WP-K3, 2026-07-07). These are the book's OWN printed cells (Table
    5.8 / 5.7 / 5.11), used to independently anchor the book-faithful GROSS
    variants (S*-GROSS-A) — distinct from ``reference_values`` (which for the
    S517 family is tautological loader output). Returns an empty dict (not an
    error) when absent, so validators can treat absence as "no variant check".
    """
    block = _series_block(sid)
    validation = block.get("validation") or {}
    raw = (validation.get("variant_reference_values") or {}).get(subseries)
    if not raw:
        return {}
    out: dict[int, float] = {}
    for k, v in raw.items():
        try:
            out[int(k)] = float(v)
        except (ValueError, TypeError):
            continue
    return out


def get_derived_statistics(sid: str) -> dict:
    """Return `validation.derived_statistics` for a series per Decision 0008.

    Decision 0008 split the v1.0 `validation.reference_values` field into two:

    - `reference_values` (year-keyed scalars only, `{<year_int>: <float>}`)
    - `derived_statistics` (free-form statistic names, `{<str>: <number>}`)

    Examples of derived statistics: `mean`, `std`, `structural_shift`,
    `n_negative`, `1959_1997_mean`, `1948_e`. Use this helper from V03
    validators that need to consume those statistics; use
    `get_reference_values()` for year-anchor checks.

    Args:
        sid: Canonical series ID (e.g., "XS1601").

    Returns:
        dict mapping statistic name to value. Returns an empty dict (not an
        error) for series that have no derived statistics, so callers can
        safely treat absence as "no stat-based checks to run".
    """
    block = _series_block(sid)
    validation = block.get("validation") or {}
    raw = validation.get("derived_statistics") or {}
    if not isinstance(raw, dict):
        return {}
    # Pass values through unchanged — they may legitimately be int (counts
    # like n_negative) or float (means, stds). Caller decides coercion.
    return dict(raw)


def get_tolerance_class(sid: str, *, default: Optional[str] = None) -> Optional[str]:
    """Return the tolerance class string from the registry, or `default`."""
    block = _series_block(sid)
    validation = block.get("validation") or {}
    return validation.get("tolerance_class") or validation.get("tolerance") or default
