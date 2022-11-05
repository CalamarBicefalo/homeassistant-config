import os

import requests
import yaml

GENERATED_PATH = 'appdaemon/apps/generated'
HA_HOST = 'http://homeassistant:8123'
os.makedirs(GENERATED_PATH, exist_ok=True)

GENERATED_ACTIVITIES = f'{GENERATED_PATH}/activities.py'


def get_common_activities(selects):
    all_options = [*map(lambda select: set(select['options']), selects.values())]
    common_activities = set.intersection(*all_options)
    return common_activities


with open("helpers/input_select.yaml", "r") as stream:
    selects = yaml.safe_load(stream)
    common_activities = get_common_activities(selects)
    try:
        with open(GENERATED_ACTIVITIES, 'w') as f:

            f.write("from typing import NewType\n"
                    "Activity = NewType('Activity', str)\n"
                    "class Common:\n")
            for c in common_activities:
                f.write(f'    {c.replace(" ", "_").upper()} : Activity = Activity("{c}")\n')

            for i in selects.items():
                f.write('\n\n')
                f.write(f'class {i[0].replace("_activity", "").title().replace("_", "")}(Common):\n')
                for o in i[1]["options"]:
                    if o not in common_activities:
                        f.write(f'    {o.replace(" ", "_").upper()}: Activity = Activity("{o}")\n')
    except yaml.YAMLError as exc:
        print(exc)


GENERATED_ENTITIES = f'{GENERATED_PATH}/entities.py'

with open("secrets.yaml", "r") as stream:
    token = yaml.safe_load(stream)['apiToken']
    resp = requests.get(url=f'{HA_HOST}/api/states', headers={"Authorization": f'Bearer {token}'}).json()
    with open(GENERATED_ENTITIES, 'w') as f:
        f.write("from typing import NewType\n"
                "Entity = NewType('Entity', str)\n")
        for s in resp:
            f.write(f'{s["entity_id"].replace(".","_").upper()}: Entity = Entity("{s["entity_id"]}")\n')


GENERATED_SERVICES = f'{GENERATED_PATH}/services.py'
with open("secrets.yaml", "r") as stream:
    token = yaml.safe_load(stream)['apiToken']
    resp = requests.get(url=f'{HA_HOST}/api/services', headers={"Authorization": f'Bearer {token}'}).json()
    with open(GENERATED_SERVICES, 'w') as f:
        f.write("from typing import NewType\n"
                "Service  = NewType('UserId', str)\n")

        for d in resp:
            for s in d['services']:
                f.write(f'{d["domain"].replace(".","_").upper()}_{s.replace(".","_").upper()}: Service = Service("{d["domain"]}/{s}")\n')
