import os

from codegen.generate_activities import generate_activities
from codegen.generate_helpers import generate_helpers
from codegen.generate_entities import generate_entities
from codegen.generate_modes import generate_modes
from codegen.generate_services import generate_services
from codegen.is_hub_reachable import is_hub_reachable

GENERATED_PATH = 'appdaemon/apps/generated'
os.makedirs(GENERATED_PATH, exist_ok=True)


#
# Generation through config files
#
generate_modes(GENERATED_PATH)
generate_activities(GENERATED_PATH)
generate_helpers(GENERATED_PATH)

#
# Generation through the wire
#
HA_HOST = 'https://kywev6rly341hnoyts4rd7h2msfp5uga.ui.nabu.casa'
if is_hub_reachable(HA_HOST):
    generate_entities(GENERATED_PATH, HA_HOST)
    generate_services(GENERATED_PATH, HA_HOST)
else:
    print("Hub is not reachable, skipping entity and service generation.")
