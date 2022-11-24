import requests
import yaml


def generate_scenes(root_dir: str, homeassistant_url: str):
    GENERATED_SCENES = f'{root_dir}/scenes.py'
    with open("secrets.yaml", "r") as stream:
        token = yaml.safe_load(stream)['apiToken']
        resp = requests.get(url=f'{homeassistant_url}/api/states', headers={"Authorization": f'Bearer {token}'}).json()
        with open(GENERATED_SCENES, 'w') as scenes_file:
            scenes_file.write("from scene_controllers import scene\n"
                              "from entities import Entity\n"
                              "from scene_controllers.scene import Scene\n")
            for s in resp:
                if s["entity_id"].startswith("scene."):
                    scenes_file.write(
                        f'{s["entity_id"].replace("scene.", "").replace(".", "_").upper()}: Scene = scene.from_entity(Entity("{s["entity_id"]}"))\n')
