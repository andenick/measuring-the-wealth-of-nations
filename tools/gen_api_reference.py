"""Generate API reference markdown for Technical/code/utils/ modules.

Walks the utils package, introspects each public function/class via `inspect`,
and renders a single Markdown reference at Technical/docs/API_REFERENCE.md.

Read-only: never writes to series_registry.json or pipeline-state files.
"""
from __future__ import annotations

import importlib
import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
UTILS_DIR = ROOT / "code" / "utils"
OUT_PATH = ROOT / "docs" / "API_REFERENCE.md"

# Module name -> (display label, short purpose)
MODULES = [
    ("registry_validator", "Registry-backed benchmark/derived-statistic loader for V03 validators."),
    ("bls_cache",          "Cached BLS CES employment reader (productive vs total)."),
    ("series",             "Parametrized building blocks: BookColumnLoader, BenchmarkValidator, pipeline glue."),
    ("io",                 "IO helpers: book-table reader, registry loader, per-series CSV writers."),
    ("paths",              "Canonical project paths (ROOT, DATA_*, REGISTRY, …)."),
    ("dpr_status_sync",    "Sync each `**Status**:` DPR header with the registry's series status."),
    ("precommit_check",    "Pre-commit checks for Decisions 0001-0008 (extenbook, refs, naming, chopped, verbatim, year-keys)."),
]


def _ensure_utils_importable() -> None:
    # Allow `import utils.<mod>` against Technical/code/utils
    code_dir = str(ROOT / "code")
    if code_dir not in sys.path:
        sys.path.insert(0, code_dir)


def _import(mod_name: str):
    return importlib.import_module(f"utils.{mod_name}")


def _signature(obj: Any) -> str:
    try:
        return f"{obj.__name__}{inspect.signature(obj)}"
    except (TypeError, ValueError):
        return f"{obj.__name__}(...)"


def _docstring(obj: Any) -> str:
    raw = inspect.getdoc(obj) or "_(no docstring)_"
    return raw


def _is_public(name: str, obj: Any, mod_name: str) -> bool:
    if name.startswith("__"):
        return False
    # Keep the explicit `_load_registry` private helper requested in the task.
    if mod_name == "registry_validator" and name == "_load_registry":
        return True
    if name.startswith("_"):
        return False
    mod = getattr(obj, "__module__", None)
    if mod is None:
        return False
    # Only document objects defined in the target module (not re-imports).
    return mod.endswith(f"utils.{mod_name}") or mod == f"utils.{mod_name}"


def _module_constants(mod, mod_name: str) -> list[tuple[str, Any]]:
    out = []
    for name in dir(mod):
        if name.startswith("_"):
            continue
        obj = getattr(mod, name)
        if inspect.isfunction(obj) or inspect.isclass(obj) or inspect.ismodule(obj):
            continue
        # Heuristics for "interesting" module-level constants: UPPER_SNAKE only.
        if not name.isupper():
            continue
        out.append((name, obj))
    return out


def render_function(func) -> str:
    sig = _signature(func)
    doc = _docstring(func)
    return f"### `{sig}`\n\n{doc}\n"


def render_class(cls) -> str:
    parts = [f"### class `{cls.__name__}`\n"]
    parts.append(_docstring(cls) + "\n")
    # Constructor signature if useful (dataclass instances)
    try:
        init_sig = inspect.signature(cls)
        parts.append(f"\n**Constructor:** `{cls.__name__}{init_sig}`\n")
    except (TypeError, ValueError):
        pass

    # Methods (skip dataclass-generated)
    methods = []
    for name, member in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name.startswith("_"):
            continue
        if getattr(member, "__module__", "") != cls.__module__:
            continue
        methods.append((name, member))
    if methods:
        parts.append("\n**Methods:**\n")
        for name, m in methods:
            try:
                msig = inspect.signature(m)
            except (TypeError, ValueError):
                msig = "(...)"
            mdoc = inspect.getdoc(m) or "_(no docstring)_"
            parts.append(f"\n- `{name}{msig}`\n  \n  {mdoc.splitlines()[0] if mdoc else ''}\n")
    return "\n".join(parts) + "\n"


def build() -> tuple[str, dict]:
    _ensure_utils_importable()
    sections: list[str] = []
    counts = {"modules": 0, "functions": 0, "classes": 0, "constants": 0}

    header = [
        "# RMWND Utilities API Reference",
        "",
        "Auto-generated from docstrings in `Technical/code/utils/` via `inspect`. ",
        "Run `python Technical/tools/gen_api_reference.py` to regenerate after touching any utils module.",
        "",
        "> **Read-only contract**: every documented function here is safe to call from L01/P02/V03 ",
        "> scripts. None of these helpers write to `series_registry.json`, `PIPELINE_STATE.json`, ",
        "> the LEDGER, the MANIFEST, or `SUBSERIES_PLAN.json`.",
        "",
        "## Modules",
        "",
    ]
    for name, blurb in MODULES:
        header.append(f"- [`{name}`](#module-{name.replace('_','-')}) — {blurb}")
    header.append("")

    for mod_name, blurb in MODULES:
        try:
            mod = _import(mod_name)
        except ImportError as e:
            sections.append(f"\n---\n\n## Module: `{mod_name}`\n\n_Failed to import: {e}_\n")
            continue
        counts["modules"] += 1
        sec: list[str] = [f"\n---\n\n## Module: `{mod_name}`\n",
                          f"**Purpose:** {blurb}\n",
                          f"**Source:** `Technical/code/utils/{mod_name}.py`\n"]

        modoc = inspect.getdoc(mod)
        if modoc:
            sec.append(f"\n**Overview:**\n\n{modoc}\n")

        consts = _module_constants(mod, mod_name)
        if consts:
            counts["constants"] += len(consts)
            sec.append("\n### Constants\n")
            sec.append("| Name | Value |\n|---|---|")
            for name, val in consts:
                if isinstance(val, Path):
                    pretty = f"`{val}`"
                else:
                    s = repr(val)
                    if len(s) > 80:
                        s = s[:77] + "..."
                    pretty = f"`{s}`"
                sec.append(f"| `{name}` | {pretty} |")
            sec.append("")

        classes = []
        functions = []
        for name in sorted(dir(mod)):
            obj = getattr(mod, name)
            if not _is_public(name, obj, mod_name):
                continue
            if inspect.isclass(obj):
                classes.append(obj)
            elif inspect.isfunction(obj):
                functions.append(obj)

        if classes:
            sec.append("\n### Classes\n")
            for cls in classes:
                counts["classes"] += 1
                sec.append(render_class(cls))

        if functions:
            sec.append("\n### Functions\n")
            for fn in functions:
                counts["functions"] += 1
                sec.append(render_function(fn))

        sections.append("\n".join(sec))

    text = "\n".join(header) + "\n".join(sections) + "\n"
    return text, counts


def main() -> int:
    text, counts = build()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    print(f"  modules:   {counts['modules']}")
    print(f"  functions: {counts['functions']}")
    print(f"  classes:   {counts['classes']}")
    print(f"  constants: {counts['constants']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
