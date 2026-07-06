"""Generate typed AppDaemon stubs from the local config and live HA state."""
from __future__ import annotations

import os

from ops.client import HaClient
from ops.codegen.entities import generate_entities
from ops.codegen.helpers import generate_helpers
from ops.codegen.rooms import generate_rooms
from ops.codegen.scenes import generate_scenes
from ops.codegen.selects import generate_selects
from ops.codegen.services import generate_services

GENERATED_PATH = "appdaemon/apps/generated"


def generate() -> None:
    os.makedirs(GENERATED_PATH, exist_ok=True)

    # From local config files.
    print("Parsing config files...")
    print("    🏠 Generating select types")
    generate_selects(GENERATED_PATH)
    print("    🗺️ Generating rooms")
    generate_rooms(GENERATED_PATH)
    print("    🔢 Generating helpers types")
    generate_helpers(GENERATED_PATH)

    # From live HA (one client, states fetched once).
    print("\n\nConnecting to hub...")
    client = HaClient()
    if client.is_reachable():
        states = client.states()
        print("    👻 Generating entities types")
        generate_entities(GENERATED_PATH, states)
        print("    🎆 Generating scenes types")
        generate_scenes(GENERATED_PATH, states)
        print("    🦮 Generating services types")
        generate_services(GENERATED_PATH, client.services())
    else:
        print("Hub is not reachable, skipping entity and service generation.")
    print("\n✅  All types generated, happy coding!")
