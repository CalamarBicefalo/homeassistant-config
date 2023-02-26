import requests
import yaml


def generate_services(root_dir: str, homeassistant_url: str):
    GENERATED_SERVICES = f'{root_dir}/services.py'
    with open("secrets/secrets.yaml", "r") as stream:
        token = yaml.safe_load(stream)['apiToken']
        resp = requests.get(url=f'{homeassistant_url}/api/services',
                            headers={"Authorization": f'Bearer {token}'}).json()
        resp.sort(key=lambda x: x["domain"])
        with open(GENERATED_SERVICES, 'w') as f:
            f.write("from typing import NewType\n"
                    "Service  = NewType('UserId', str)\n")

            for d in resp:
                services_ = list(d['services'].keys())
                services_.sort()
                for s in services_:
                    f.write(
                        f'{d["domain"].replace(".", "_").upper()}_{s.replace(".", "_").upper()}: Service = Service("{d["domain"]}/{s}")\n')
