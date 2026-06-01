"""Shared pytest configuration for the RMWND test suite.

Makes `Technical/code/utils/` importable so tests can `from utils.registry_validator
import ...` and friends, regardless of the cwd pytest is invoked from.

CAVEAT: `Technical/code/__init__.py` exists, so `code/` is a package. If we
simply prepended `code/` to sys.path, `import code` would resolve to the
project's package instead of the stdlib `code` module that pdb depends on.
To avoid that name clash we:

  1. Pre-import `pdb` (which pulls in stdlib `code`) before mutating sys.path.
  2. Prepend `code/` so `from utils.X import Y` resolves cleanly.

Pre-importing `pdb` ensures the stdlib `code` reference is already cached in
`sys.modules` before our path manipulation can shadow it.
"""
from __future__ import annotations

import sys
from pathlib import Path

# 1. Force stdlib `code` to be cached in sys.modules BEFORE pytest's debugging
#    plugin imports pdb (which needs stdlib `code.InteractiveConsole`).
#    The project's Technical/code/__init__.py shadows stdlib `code` whenever
#    cwd or Technical/ is on sys.path. We load stdlib `code` by its absolute
#    path via importlib.util to bypass the shadowing.
import importlib.util as _imp_util
import sysconfig as _sysconfig
from pathlib import Path as _Path

_stdlib_dir = _Path(_sysconfig.get_paths()["stdlib"])
_code_path = _stdlib_dir / "code.py"
if _code_path.exists() and "code" not in sys.modules:
    _spec = _imp_util.spec_from_file_location("code", _code_path)
    _mod = _imp_util.module_from_spec(_spec)
    sys.modules["code"] = _mod
    _spec.loader.exec_module(_mod)
import pdb as _pdb  # noqa: F401, E402  (now safe — stdlib code is cached)

import pytest

TECHNICAL_ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = TECHNICAL_ROOT / "code"
CHOPPED_DIR = TECHNICAL_ROOT / "chopped"
GOLDEN_DIR = Path(__file__).resolve().parent / "golden_chopped"

# 2. Inject code/ on sys.path so `from utils.X import Y` works in tests.
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))


@pytest.fixture(scope="session")
def technical_root() -> Path:
    return TECHNICAL_ROOT


@pytest.fixture(scope="session")
def chopped_dir() -> Path:
    return CHOPPED_DIR


@pytest.fixture(scope="session")
def golden_dir() -> Path:
    return GOLDEN_DIR
