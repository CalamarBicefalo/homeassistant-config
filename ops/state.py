from __future__ import annotations

import argparse
import json

from ops.client import HaClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Show an entity's current state and attributes.")
    parser.add_argument("entity_id", help="e.g. sensor.living_room_illuminance")
    args = parser.parse_args()

    print(json.dumps(HaClient().state(args.entity_id), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
