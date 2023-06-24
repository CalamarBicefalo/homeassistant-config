import yaml

def generate_modes(root_dir: str):
    GENERATED_MODES = f'{root_dir}/modes.py'
    SELECT_NAME = "homeassistant_mode"
    with open("helpers/input_select/input_select.yaml", "r") as stream:
        selects = yaml.safe_load(stream)
        homeassistant_mode = selects[SELECT_NAME]
        try:
            with open(GENERATED_MODES, 'w') as f:

                f.write("from enum import StrEnum\n")
                f.write('\n')
                f.write(f'class Mode(StrEnum):\n')
                for o in homeassistant_mode["options"]:
                    f.write(f'    {o.replace(" ", "_").upper()} = "{o}"\n')
                f.write(f'\n')
        except yaml.YAMLError as exc:
            print(exc)
