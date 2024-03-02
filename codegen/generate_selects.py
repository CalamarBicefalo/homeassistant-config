import yaml

def generate_selects(root_dir: str):
    GENERATED_MODES = f'{root_dir}/selects.py'
    with open("helpers/input_select/input_select.yaml", "r") as stream:
        selects = yaml.safe_load(stream)
        try:
            with open(GENERATED_MODES, 'w') as f:
                f.write("from enum import StrEnum\n")
                for key in selects.keys():
                    f.write('\n')
                    f.write(f'class {key.title().replace(" ", "").replace("_", "")}(StrEnum):\n')
                    for o in selects[key]["options"]:
                        f.write(f'    {o.replace(" ", "_").upper()} = "{o}"\n')
                    f.write(f'\n')
        except yaml.YAMLError as exc:
            print(exc)
