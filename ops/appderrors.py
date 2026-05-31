from __future__ import annotations

import argparse
import json
from typing import Any

from ops.client import HaClient
from ops.timeutil import since_to_iso

# Kept in sync with appdaemon/apps/src/error_reporter.py.
LAST_ERROR_SENSOR = "sensor.appdaemon_last_error"


def _history_rows(client: HaClient, since: str) -> list[dict[str, Any]]:
    # /api/history returns a list of per-entity lists; we asked for one entity.
    result = client.history(LAST_ERROR_SENSOR, since_to_iso(since))
    return result[0] if result else []


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Show AppDaemon app errors reported into HA by error_reporter.")
    parser.add_argument("--since", default="24h", help="History window, e.g. 2h, 24h, 7d (default 24h).")
    args = parser.parse_args()

    client = HaClient()

    latest = client.try_state(LAST_ERROR_SENSOR)
    if latest is None:
        print("No AppDaemon errors reported yet "
            f"({LAST_ERROR_SENSOR} does not exist). Is the error_reporter app running?")
        return

    print("== Latest AppDaemon error ==")
    print(json.dumps(latest, indent=2, sort_keys=True))

    print(f"\n== Error timeline (last {args.since}) ==")
    rows = _history_rows(client, args.since)
    if not rows:
        print("(no recorded changes in window)")
    for row in rows:
        attrs = row.get("attributes", {})
        when = row.get("last_changed", "?")
        print(f"{when}  {attrs.get('level', '?'):<8} [{attrs.get('app', '?')}] {row.get('state', '')}")


if __name__ == "__main__":
    main()
