from __future__ import annotations

from datetime import datetime
from typing import Any

from ops.wsclient import system_log

# Ordered low -> high so --level can include everything at or above a threshold.
LEVEL_ORDER = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def _levels_at_or_above(level: str) -> set[str]:
    if level not in LEVEL_ORDER:
        return {level}
    return set(LEVEL_ORDER[LEVEL_ORDER.index(level):])


def _searchable_text(entry: dict[str, Any]) -> str:
    parts = [entry.get("name", ""), (entry.get("source") or [""])[0]]
    parts.extend(entry.get("message") or [])
    return " ".join(p for p in parts if p)


def _format(entry: dict[str, Any]) -> str:
    ts = entry.get("timestamp")
    when = datetime.fromtimestamp(ts).isoformat(timespec="seconds") if ts else "?"
    level = entry.get("level", "?")
    source = (entry.get("source") or ["?"])[0]
    message = (entry.get("message") or [""])[0]
    count = entry.get("count") or 1
    repeats = f"  (x{count})" if count > 1 else ""
    return f"{when}  {level:<8} {source}  {message}{repeats}"


def run(level: str = "WARNING", grep: str | None = None, tail: int = 30) -> None:
    """Print HA core warnings/errors. Shared by the module CLI and `ops.cli`."""
    wanted = _levels_at_or_above(level.upper())
    entries = [e for e in system_log() if e.get("level") in wanted]
    if grep:
        needle = grep.lower()
        entries = [e for e in entries if needle in _searchable_text(e).lower()]

    # system_log/list returns newest first; print the most recent N chronologically.
    for entry in reversed(entries[:tail]):
        print(_format(entry))
