"""
RMWND Dash -- Structured Logger
Writes structured log entries to logs/ for framework cascade compliance.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"


def ensure_log_dir() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR


def get_file_logger() -> logging.Logger:
    logger = logging.getLogger("rmwnd-dash")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        ensure_log_dir()
        fh = logging.FileHandler(
            LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log",
            encoding="utf-8",
        )
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        ))
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(ch)
    return logger


def log_structured(action: str, **details):
    ensure_log_dir()
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        **details,
    }
    log_file = LOG_DIR / "structured.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
