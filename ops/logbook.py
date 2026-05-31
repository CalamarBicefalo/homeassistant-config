from __future__ import annotations

import argparse
import json

from ops.client import HaClient
from ops.timeutil import since_to_iso


def main() -> None:
    parser = argparse.ArgumentParser(description="Show Home Assistant logbook entries.")
    parser.add_argument("--entity", help="Filter to a single entity_id.")
    parser.add_argument("--since", default="2h", help="Lookback window, e.g. 30m, 2h, 1d (default 2h).")
    args = parser.parse_args()

    data = HaClient().logbook(since_to_iso(args.since), args.entity)
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
