import os

from codegen.generate_helpers import generate_helpers
from codegen.generate_entities import generate_entities
from codegen.generate_selects import generate_selects
from codegen.generate_rooms import generate_rooms
from codegen.generate_scenes import generate_scenes
from codegen.generate_services import generate_services
from codegen.is_hub_reachable import is_hub_reachable

GENERATED_PATH = 'appdaemon/apps/generated'
os.makedirs(GENERATED_PATH, exist_ok=True)


#
# Generation through config files
#
print("Parsing config files...")
print("    🏠 Generating select types")
generate_selects(GENERATED_PATH)
print("    🗺️ Generating rooms")
generate_rooms(GENERATED_PATH)
print("    🔢 Generating helpers types")
generate_helpers(GENERATED_PATH)

#
# Generation through the wire
#
HA_HOST = 'https://calamarbicefalo.uk'
print("")
print("")
print("Connecting to hub...")
if is_hub_reachable(HA_HOST):
    print("    👻 Generating entities types")
    generate_entities(GENERATED_PATH, HA_HOST)
    print("    🎆 Generating scenes types")
    generate_scenes(GENERATED_PATH, HA_HOST)
    print("    🦮 Generating services types")
    generate_services(GENERATED_PATH, HA_HOST)
else:
    print("Hub is not reachable, skipping entity and service generation.")
print("")
print("✅  All types generated, happy coding!")
