"""High-level query helpers that sit on top of the loaded registry dict.

All functions accept a ``registry`` dict (the output of
``config_loader.load_registry()``) so that callers never need to know
the internal JSON schema.
"""

from __future__ import annotations

import json
from typing import Any

from .paths import RESEARCH


def get_series(registry: dict, series_id: str) -> dict[str, Any]:
    """Return the full series entry, or raise ``KeyError``."""
    try:
        return registry["series"][series_id]
    except KeyError:
        raise KeyError(f"Series '{series_id}' not found in registry.")


def get_subseries(registry: dict, series_id: str) -> dict[str, Any]:
    """Return the *subseries* mapping for a series."""
    return get_series(registry, series_id).get("subseries", {})


def get_construction_steps(registry: dict, series_id: str) -> list[dict]:
    """Return the ordered list of construction / processing steps."""
    return get_series(registry, series_id).get("construction", [])


def get_extension_config(registry: dict, series_id: str) -> dict | None:
    """Return the extension configuration block, or ``None``."""
    return get_series(registry, series_id).get("extension")


def get_validation_config(registry: dict, series_id: str) -> dict:
    """Return the validation block (defaults to empty dict)."""
    return get_series(registry, series_id).get("validation", {})


def get_research(series_id: str) -> dict[str, Any] | None:
    """Load the per-series research JSON (``T###_research.json``).

    Returns ``None`` if the file does not exist.
    """
    path = RESEARCH / f"{series_id}_research.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def get_color(registry: dict, subseries_id: str) -> str:
    """Return the hex colour string for a subseries.

    Walks every series to find the matching subseries.  Falls back to
    ``"#333333"`` if no colour is defined.
    """
    for entry in registry["series"].values():
        sub = entry.get("subseries", {}).get(subseries_id)
        if sub is not None:
            return sub.get("color", "#333333")
    return "#333333"


def get_display_name(
    registry: dict,
    series_id: str,
    subseries_id: str,
) -> str:
    """Return a human-readable name, appending ``[R:YYYY]`` when reindexed."""
    sub = get_subseries(registry, series_id).get(subseries_id, {})
    name = sub.get("name", subseries_id)
    reindex_year = sub.get("reindex_year")
    if reindex_year is not None:
        return f"{name} [R:{reindex_year}]"
    return name


def get_all_series_ids(registry: dict) -> list[str]:
    """Return a sorted list of every series ID in the registry."""
    return sorted(registry.get("series", {}).keys())


def get_series_for_chapter(registry: dict, chapter: int) -> list[str]:
    """Return series IDs that belong to *chapter* (sorted)."""
    return sorted(
        sid
        for sid, entry in registry.get("series", {}).items()
        if entry.get("chapter") == chapter
    )
