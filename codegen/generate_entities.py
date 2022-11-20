import requests
import yaml


def generate_entities(root_dir: str, homeassistant_url: str):
    GENERATED_ENTITIES = f'{root_dir}/entities.py'
    with open("secrets.yaml", "r") as stream:
        token = yaml.safe_load(stream)['apiToken']
        resp = requests.get(url=f'{homeassistant_url}/api/states', headers={"Authorization": f'Bearer {token}'}).json()
        with open(GENERATED_ENTITIES, 'w') as f:
            f.write("from typing import NewType\n"
                    "Entity = NewType('Entity', str)\n")
            for s in resp:
                f.write(f'{s["entity_id"].replace(".", "_").upper()}: Entity = Entity("{s["entity_id"]}")\n')
