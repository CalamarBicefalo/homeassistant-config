import glob

import requests
import yaml


def generate_services(root_dir: str, homeassistant_url: str):
    global stream, token, resp, f, s
    GENERATED_SERVICES = f'{root_dir}/services.py'
    with open("secrets.yaml", "r") as stream:
        token = yaml.safe_load(stream)['apiToken']
        resp = requests.get(url=f'{homeassistant_url}/api/services',
                            headers={"Authorization": f'Bearer {token}'}).json()
        with open(GENERATED_SERVICES, 'w') as f:
            f.write("from typing import NewType\n"
                    "Service  = NewType('UserId', str)\n")

            for d in resp:
                for s in d['services']:
                    f.write(
                        f'{d["domain"].replace(".", "_").upper()}_{s.replace(".", "_").upper()}: Service = Service("{d["domain"]}/{s}")\n')


def generate_entities(root_dir: str, homeassistant_url: str):
    global stream, token, resp, f, s
    GENERATED_ENTITIES = f'{root_dir}/entities.py'
    with open("secrets.yaml", "r") as stream:
        token = yaml.safe_load(stream)['apiToken']
        resp = requests.get(url=f'{homeassistant_url}/api/states', headers={"Authorization": f'Bearer {token}'}).json()
        with open(GENERATED_ENTITIES, 'w') as f:
            f.write("from typing import NewType\n"
                    "Entity = NewType('Entity', str)\n")
            for s in resp:
                f.write(f'{s["entity_id"].replace(".", "_").upper()}: Entity = Entity("{s["entity_id"]}")\n')


def generate_helpers(root_dir: str):
    global f, stream, exc, i
    GENERATED_HELPERS = f'{root_dir}/helpers.py'
    helper_files = glob.glob("helpers/*")
    with open(GENERATED_HELPERS, 'w') as output:
        output.write("from typing import NewType\n"
                     "Helper = NewType('Helper', str)\n")
        output.write('\n\n')
        for f in helper_files:
            with open(f, "r") as stream:
                yml = yaml.safe_load(stream)
                if yml is not None:
                    try:
                        for i in yml.keys():
                            output.write(
                                f'{i.upper()} = Helper("{f.replace(".yaml", ".").replace("helpers/", "") + i}")\n')
                    except yaml.YAMLError as exc:
                        print(exc)


def generate_activities(root_dir: str):
    global stream, f, i, exc
    GENERATED_ACTIVITIES = f'{root_dir}/activities.py'

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
                    if len(i[1]["options"]) == len(common_activities):
                        f.write('    pass')
                    for o in i[1]["options"]:
                        if o not in common_activities:
                            f.write(f'    {o.replace(" ", "_").upper()}: Activity = Activity("{o}")\n')
        except yaml.YAMLError as exc:
            print(exc)
