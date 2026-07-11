"""Show the AppDaemon add-on log — the `self.log(...)` output from the apps.

These lines live in the add-on log (fetched via the HA->Supervisor proxy), not
in HA's core system_log that `ops.logs` reads, so this is a separate command.
Each line looks like:

    2026-07-11 17:44:34.543540 INFO AppDaemon: App initialization complete

i.e. `<timestamp> <LEVEL> <App name>: <message>`. Tracebacks and other wrapped
output arrive as continuation lines with no header; we attach them to the entry
above so level/grep filtering keeps a multi-line error together.
"""
from __future__ import annotations

import re
import sys
import zlib
from dataclasses import dataclass, field
from typing import Optional

import typer

from ops.client import HaClient

# Kept in sync with APPDAEMON_ADDON in appdaemon's install.py.
APPDAEMON_ADDON = "a0d7b954_appdaemon"

# Ordered low -> high so --level can include everything at or above a threshold.
LEVEL_ORDER = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

_HEADER = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+"
    r"(?P<level>[A-Z]+)\s+(?P<rest>.*)$"
)
_ANSI = re.compile(r"\x1b\[[0-9;]*m")

# Fixed colour per level; the app name gets a stable colour hashed from its name.
_LEVEL_COLOUR = {
    "DEBUG": "bright_black",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bright_red",
}
_APP_PALETTE = [
    "cyan", "magenta", "blue", "bright_cyan",
    "bright_magenta", "bright_blue", "bright_green",
]


@dataclass
class Entry:
    ts: str
    level: str
    app: str
    message: str
    extra: list[str] = field(default_factory=list)  # continuation/traceback lines

    @property
    def text(self) -> str:
        """Everything searchable in this entry, for --grep."""
        return " ".join([self.app, self.message, *self.extra])


def _levels_at_or_above(level: str) -> set[str]:
    if level not in LEVEL_ORDER:
        return {level}
    return set(LEVEL_ORDER[LEVEL_ORDER.index(level):])


def parse(raw: str) -> list[Entry]:
    """Group the raw add-on log text into entries (headers + continuation lines)."""
    entries: list[Entry] = []
    for line in _ANSI.sub("", raw).splitlines():
        match = _HEADER.match(line)
        if match:
            rest = match["rest"]
            app, sep, message = rest.partition(": ")
            if not sep:  # no "App: message" split; treat the whole thing as message
                app, message = "", rest
            entries.append(Entry(match["ts"], match["level"], app, message))
        elif entries and line.strip():
            entries[-1].extra.append(line)
        # blank lines with no current entry are add-on boot noise; drop them.
    return entries


def _app_colour(app: str) -> str:
    if not app:
        return "white"
    return _APP_PALETTE[zlib.crc32(app.encode()) % len(_APP_PALETTE)]


def _format(entry: Entry, colour: bool) -> str:
    time_only = entry.ts.split(" ", 1)[1][:12]  # HH:MM:SS.mmm
    if not colour:
        head = f"{time_only}  {entry.level:<8} {entry.app}: {entry.message}"
        return "\n".join([head, *entry.extra])

    level_colour = _LEVEL_COLOUR.get(entry.level, "white")
    parts = [
        typer.style(time_only, fg="bright_black"),
        "  ",
        typer.style(f"{entry.level:<8}", fg=level_colour, bold=True),
        " ",
        typer.style(entry.app, fg=_app_colour(entry.app), bold=True),
        typer.style(": ", fg="bright_black") if entry.app else "",
        typer.style(entry.message, fg=level_colour) if entry.level in ("ERROR", "CRITICAL", "WARNING") else entry.message,
    ]
    lines = ["".join(parts)]
    lines += [typer.style(x, fg=level_colour or "red") for x in entry.extra]
    return "\n".join(lines)


def run(level: str = "INFO", grep: Optional[str] = None, app: Optional[str] = None,
        tail: int = 50, color: Optional[bool] = None) -> None:
    """Print AppDaemon app logs. Shared by the module CLI and `ops.cli`."""
    use_colour = sys.stdout.isatty() if color is None else color

    # Over-fetch so level/grep filtering still leaves roughly `tail` entries.
    fetch = min(max(tail * 8, 400), 5000)
    raw = HaClient().addon_logs(APPDAEMON_ADDON, lines=fetch)

    wanted = _levels_at_or_above(level.upper())
    entries = [e for e in parse(raw) if e.level in wanted]
    if app:
        needle = app.lower()
        entries = [e for e in entries if needle in e.app.lower()]
    if grep:
        needle = grep.lower()
        entries = [e for e in entries if needle in e.text.lower()]

    if not entries:
        print("(no matching AppDaemon log entries)")
        return
    for entry in entries[-tail:]:
        print(_format(entry, use_colour))
