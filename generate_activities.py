import os
import yaml

GENERATED_PATH = 'appdaemon/apps/generated'
GENERATED_ACTIVITIES = f'{GENERATED_PATH}/activities.py'

os.makedirs(GENERATED_PATH, exist_ok=True)

with open("helpers/input_select.yaml", "r") as stream:
    try:
        with open(GENERATED_ACTIVITIES, 'w') as f:
            selects = yaml.safe_load(stream)
            f.write("from enum import Enum\n"
                    "\n\n"
                    "class Activity(Enum):\n"
                    "    pass\n")

            for i in selects.items():
                f.write('\n\n')
                f.write(f'class {i[0].replace("_activity", "").title().replace("_", "")}(Activity):\n')
                for o in i[1]["options"]:
                    f.write(f'    {o.replace(" ", "_").upper()} = "{o}"\n')
    except yaml.YAMLError as exc:
        print(exc)
