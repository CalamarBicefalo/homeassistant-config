import glob

import yaml


def generate_helpers(root_dir: str):
    GENERATED_HELPERS = f'{root_dir}/helpers.py'
    helper_files = glob.glob("helpers/input_*.yaml")
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
                            if i.endswith("_activity"):
                                continue
                            output.write(
                                f'{i.upper()} = Helper("{f.replace(".yaml", ".").replace("helpers/", "") + i}")\n')
                    except yaml.YAMLError as exc:
                        print(exc)
