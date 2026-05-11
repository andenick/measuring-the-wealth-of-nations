"""Rich console output using box-drawing characters."""

from __future__ import annotations

import io
import os
import sys
from typing import Any

if sys.stdout.encoding and sys.stdout.encoding.lower().replace("-", "") != "utf8":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
    )

BOX_H = "\u2500"
BOX_V = "\u2502"
BOX_TL = "\u250c"
BOX_TR = "\u2510"
BOX_BL = "\u2514"
BOX_BR = "\u2518"
TREE_BRANCH = "\u251c\u2500\u2500 "
TREE_LAST = "\u2514\u2500\u2500 "

STATUS_ICONS = {
    "ok": "\u2713",
    "warn": "\u26a0",
    "fail": "\u2717",
    "skip": "\u2013",
    "info": "\u00b7",
}


def _hline(width: int = 60) -> str:
    return BOX_H * width


def _box(text: str, width: int = 60) -> str:
    inner = width - 4
    padded = f" {text[:inner]:<{inner}} "
    return (
        f"{BOX_TL}{BOX_H * (width - 2)}{BOX_TR}\n"
        f"{BOX_V}{padded}{BOX_V}\n"
        f"{BOX_BL}{BOX_H * (width - 2)}{BOX_BR}"
    )


def print_banner(version: str, registry: dict[str, Any]) -> None:
    n_series = len(registry.get("series", {}))
    bea_ok = bool(os.environ.get("BEA_API_KEY"))
    fred_ok = bool(os.environ.get("FRED_API_KEY"))
    bls_ok = bool(os.environ.get("BLS_API_KEY"))

    api_parts = []
    if bea_ok:
        api_parts.append(f"{STATUS_ICONS['ok']} BEA")
    else:
        api_parts.append(f"{STATUS_ICONS['warn']} BEA")
    if fred_ok:
        api_parts.append(f"{STATUS_ICONS['ok']} FRED")
    else:
        api_parts.append(f"{STATUS_ICONS['warn']} FRED")
    if bls_ok:
        api_parts.append(f"{STATUS_ICONS['ok']} BLS")
    else:
        api_parts.append(f"{STATUS_ICONS['warn']} BLS")

    print()
    print(_box(f"AS2 Anu Replicator  v{version}", width=50))
    print(f"  {STATUS_ICONS['info']} Registry : {n_series} series loaded")
    print(f"  {STATUS_ICONS['info']} API keys : {', '.join(api_parts)}")
    print()


def print_load_summary(results: list[dict[str, Any]]) -> None:
    ok = sum(1 for r in results if r.get("status") == "ok")
    warn = sum(1 for r in results if r.get("status") == "warn")
    fail = sum(1 for r in results if r.get("status") == "fail")
    total = len(results)

    print()
    print(_hline(50))
    print(f"  Loading complete: {total} series")
    print(f"    {STATUS_ICONS['ok']} {ok} loaded    {STATUS_ICONS['warn']} {warn} warnings    {STATUS_ICONS['fail']} {fail} failed")
    print(_hline(50))
    print()


def print_process_summary(results: list[dict[str, Any]]) -> None:
    ok = sum(1 for r in results if r.get("status") == "ok")
    warn = sum(1 for r in results if r.get("status") == "warn")
    fail = sum(1 for r in results if r.get("status") == "fail")
    total = len(results)

    col_w = 20
    header = f"{'Series':<{col_w}} {'Status':<10} {'Steps':<8} {'Notes'}"
    sep = _hline(len(header) + 4)

    print()
    print(sep)
    print("  PROCESSING SUMMARY")
    print(sep)
    print(f"  {header}")
    print(f"  {'-' * len(header)}")

    for r in results:
        sid = r.get("series_id", "???")[:col_w]
        status = r.get("status", "?")
        n_steps = len(r.get("steps", []))
        notes = r.get("notes", "")
        icon = STATUS_ICONS.get(status, "?")
        print(f"  {sid:<{col_w}} {icon} {status:<8} {n_steps:<8} {notes}")

    print(sep)
    print(f"  Totals: {total} series \u2014 {ok} ok, {warn} warnings, {fail} failed")
    print(sep)
    print()
