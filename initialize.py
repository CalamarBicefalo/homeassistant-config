import os

import requests
import yaml

GENERATED_PATH = 'appdaemon/apps/generated'
HA_HOST = 'http://homeassistant:8123'
os.makedirs(GENERATED_PATH, exist_ok=True)

GENERATED_ACTIVITIES = f'{GENERATED_PATH}/activities.py'
with open("helpers/input_select.yaml", "r") as stream:
    try:
        with open(GENERATED_ACTIVITIES, 'w') as f:
            selects = yaml.safe_load(stream)
            f.write("from enum import Enum\n"
                    "\n\n"
                    "class Activity(Enum):\n"
                    "    pass\n")

            for i in selects.items():
                f.write('\n\n')
                f.write(f'class {i[0].replace("_activity", "").title().replace("_", "")}(Activity):\n')
                for o in i[1]["options"]:
                    f.write(f'    {o.replace(" ", "_").upper()} = "{o}"\n')
    except yaml.YAMLError as exc:
        print(exc)


GENERATED_ENTITIES = f'{GENERATED_PATH}/entities.py'
with open("secrets.yaml", "r") as stream:
    token = yaml.safe_load(stream)['apiToken']
    resp = requests.get(url=f'{HA_HOST}/api/states', headers={"Authorization": f'Bearer {token}'}).json()
    with open(GENERATED_ENTITIES, 'w') as f:
        for s in resp:
            f.write(f'{s["entity_id"].replace(".","_").upper()} = "{s["entity_id"]}"\n')


GENERATED_SERVICES = f'{GENERATED_PATH}/services.py'
with open("secrets.yaml", "r") as stream:
    token = yaml.safe_load(stream)['apiToken']
    resp = requests.get(url=f'{HA_HOST}/api/services', headers={"Authorization": f'Bearer {token}'}).json()
    with open(GENERATED_SERVICES, 'w') as f:
        for d in resp:
            for s in d['services']:
                f.write(f'{d["domain"].replace(".","_").upper()}_{s.replace(".","_").upper()} = "{d["domain"]}/{s}"\n')
