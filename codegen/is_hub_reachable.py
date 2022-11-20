import requests
import yaml


def is_hub_reachable(homeassistant_url: str):
    with open("secrets.yaml", "r") as stream:
        token = yaml.safe_load(stream)['apiToken']
        try:
            return requests.get(url=f'{homeassistant_url}/api/states', headers={"Authorization": f'Bearer {token}'}).ok
        except:
            return False
