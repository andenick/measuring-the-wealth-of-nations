"""Load and validate the series registry configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import REGISTRY

REQUIRED_SERIES_FIELDS = {"name", "chapter", "subseries"}
REQUIRED_SUBSERIES_FIELDS = {"name"}


def load_registry(path: Path | None = None) -> dict[str, Any]:
    """Read *series_registry.json* and return it as a Python dict.

    Parameters
    ----------
    path : Path, optional
        Override the default registry location (useful for tests).

    Raises
    ------
    FileNotFoundError
        If the registry file does not exist.
    json.JSONDecodeError
        If the file is not valid JSON.
    """
    path = path or REGISTRY
    if not path.exists():
        raise FileNotFoundError(
            f"Series registry not found at {path}.\n"
            "Run the project setup or create the file manually."
        )
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def validate_registry(registry: dict[str, Any]) -> list[str]:
    """Check that every series entry contains the required fields.

    Returns a list of human-readable error strings.  An empty list means
    the registry is valid.
    """
    errors: list[str] = []

    if "series" not in registry:
        errors.append("Registry missing top-level 'series' key.")
        return errors

    for sid, entry in registry["series"].items():
        missing = REQUIRED_SERIES_FIELDS - set(entry.keys())
        if missing:
            errors.append(f"Series '{sid}' missing fields: {', '.join(sorted(missing))}")

        for sub_id, sub in entry.get("subseries", {}).items():
            sub_missing = REQUIRED_SUBSERIES_FIELDS - set(sub.keys())
            if sub_missing:
                errors.append(
                    f"Subseries '{sub_id}' in '{sid}' missing fields: "
                    f"{', '.join(sorted(sub_missing))}"
                )

    return errors
