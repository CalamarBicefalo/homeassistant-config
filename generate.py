import os

from codegen.generators import generate_activities, generate_helpers, generate_entities, generate_services, \
    is_hub_reachable

GENERATED_PATH = 'appdaemon/apps/generated'
os.makedirs(GENERATED_PATH, exist_ok=True)


#
# Generation through config files
#
generate_activities(GENERATED_PATH)
generate_helpers(GENERATED_PATH)

#
# Generation through the wire
#
HA_HOST = 'http://homeassistant:8123'
if is_hub_reachable(HA_HOST):
    generate_entities(GENERATED_PATH, HA_HOST)
    generate_services(GENERATED_PATH, HA_HOST)
else:
    print("Hub is not reachable, skipping entity and service generation.")
