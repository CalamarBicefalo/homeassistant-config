from __future__ import annotations

import json
from typing import Any

from ops.client import HaClient
from ops.timeutil import since_to_iso

# Kept in sync with appdaemon/apps/src/error_reporter.py.
LAST_ERROR_SENSOR = "sensor.appdaemon_last_error"
STATUS_OK = "ok"


def _history_rows(client: HaClient, since: str) -> list[dict[str, Any]]:
    # /api/history returns a list of per-entity lists; we asked for one entity.
    result = client.history(LAST_ERROR_SENSOR, since_to_iso(since))
    return result[0] if result else []


def run(since: str = "24h") -> None:
    """Print AppDaemon errors. Shared by the module CLI and `ops.cli`."""
    client = HaClient()

    latest = client.try_state(LAST_ERROR_SENSOR)
    if latest is None:
        print(f"{LAST_ERROR_SENSOR} does not exist - the error_reporter app is not "
            "running (or hasn't started yet).")
        return

    attrs = latest.get("attributes", {})
    if latest.get("state") == STATUS_OK:
        print(f"error_reporter is running; no AppDaemon errors since "
            f"{attrs.get('initialized_at', '?')}.")
    else:
        print("== Latest AppDaemon error ==")
        print(json.dumps(latest, indent=2, sort_keys=True))

    print(f"\n== Error timeline (last {since}) ==")
    rows = [r for r in _history_rows(client, since) if r.get("state") != STATUS_OK]
    if not rows:
        print("(no errors in window)")
    for row in rows:
        row_attrs = row.get("attributes", {})
        when = row.get("last_changed", "?")
        print(f"{when}  {row_attrs.get('level', '?'):<8} [{row_attrs.get('app', '?')}] {row.get('state', '')}")
