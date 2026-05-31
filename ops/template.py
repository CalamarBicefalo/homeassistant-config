from __future__ import annotations

import argparse

from ops.client import HaClient


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a Jinja template against live HA state (debug conditions).")
    parser.add_argument("template", help="e.g. \"{{ states('sensor.living_room_illuminance') }}\"")
    args = parser.parse_args()

    print(HaClient().render_template(args.template))


if __name__ == "__main__":
    main()
