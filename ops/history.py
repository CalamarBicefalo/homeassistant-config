from __future__ import annotations

import argparse
import json

from ops.client import HaClient
from ops.timeutil import since_to_iso


def main() -> None:
    parser = argparse.ArgumentParser(description="Show recorded state history for an entity.")
    parser.add_argument("entity_id", help="e.g. input_select.living_room_activity")
    parser.add_argument("--since", default="2h", help="Lookback window, e.g. 30m, 2h, 1d (default 2h).")
    args = parser.parse_args()

    data = HaClient().history(args.entity_id, since_to_iso(args.since))
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
