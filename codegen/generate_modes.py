import yaml

def generate_modes(root_dir: str):
    GENERATED_MODES = f'{root_dir}/modes.py'
    SELECT_NAME = "homeassistant_mode"
    with open("helpers/input_select.yaml", "r") as stream:
        selects = yaml.safe_load(stream)
        homeassistant_mode = selects[SELECT_NAME]
        try:
            with open(GENERATED_MODES, 'w') as f:

                f.write("from typing import NewType\n"
                        "from helpers import Helper\n"
                        "from enum import Enum\n"
                        "from abc import abstractmethod\n"
                        "import app\n"
                       )

                f.write('\n\n')
                f.write(f'class Home:\n')
                f.write(f'    _helper = Helper("input_select.{SELECT_NAME}")\n')
                f.write(f'\n')
                f.write(f'    class Mode(Enum):\n')
                for o in homeassistant_mode["options"]:
                    f.write(f'        {o.replace(" ", "_").upper()} = "{o}"\n')
                f.write(f'\n')
                f.write(f'    def __init__(self, app: App):\n')
                f.write(f'        self._app = app\n')
                f.write(f'\n')
                f.write(f'    def set_mode(self, mode: Mode):\n')
                f.write(f'        self.log("Setting mode " + mode.value, level="DEBUG")\n')
                f.write(f'        self.call_service(\n')
                f.write(f'            services.INPUT_SELECT_SELECT_OPTION,\n')
                f.write(f'            entity_id=self._helper,\n')
                f.write(f'            option=mode.value\n')
                f.write(f'        )\n')
                f.write(f'\n')
                f.write(f'    def is_mode(self, helper: Helper, mode: Mode):\n')
                f.write(f'        return self._app.has_state(self._helper, mode.value)\n')
                f.write(f'\n')
                f.write(f'    def get_mode(self) -> Mode:\n')
                f.write(f'        return  Mode(self.get_state(helper))\n')
                f.write(f'\n')
        except yaml.YAMLError as exc:
            print(exc)
