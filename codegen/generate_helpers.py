import glob

import yaml


def generate_helpers(root_dir: str):
    GENERATED_HELPERS = f'{root_dir}/helpers.py'
    helper_files = glob.glob("helpers/**/input_*.yaml")
    with open(GENERATED_HELPERS, 'w') as output:
        output.write("from typing import NewType\n"
                     "from datetime import datetime\n"
                     "Helper = NewType('Helper', str)\n"
                     "HELPER_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'\n")
        output.write('\n\n')
        for f in helper_files:
            if f.endswith("_generated.yaml"):
                continue
            with open(f, "r") as stream:
                yml = yaml.safe_load(stream)
                if yml is not None:
                    try:
                        for i in yml.keys():
                            output.write(
                                f'{i.upper()} = Helper("{f.replace("_generated", "").replace(".yaml", ".").rsplit("/", 1)[1] + i}")\n')
                    except yaml.YAMLError as exc:
                        print(exc)
        output.write('\n\n')
        output.write("def datetime_to_helper(d: datetime) -> str:\n"
                     "    return d.strftime(HELPER_DATETIME_FORMAT)\n")

        output.write('\n')
        output.write("def helper_to_datetime(helper_state: str) -> datetime:\n"
                     "    return datetime.strptime(str(helper_state), HELPER_DATETIME_FORMAT)\n"
                     )
