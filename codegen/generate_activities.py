import yaml


def generate_activities(root_dir: str):
    GENERATED_ACTIVITIES = f'{root_dir}/activities.py'

    def get_common_activities(act):
        all_options = [*map(lambda select: set(select['options']), act.values())]
        return set.intersection(*all_options)

    with open("helpers/input_select.yaml", "r") as stream:
        selects = yaml.safe_load(stream)
        defined_activities = {k: v for k, v in selects.items() if k.endswith('_activity')}
        common_activities = get_common_activities(defined_activities)
        try:
            with open(GENERATED_ACTIVITIES, 'w') as f:

                f.write("from typing import NewType\n"
                        "from helpers import Helper\n"
                        "from abc import abstractmethod\n"
                        "Activity = NewType('Activity', str)\n"
                        "class RoomActivity:\n"
                        "    @property\n"
                        "    @abstractmethod\n"
                        "    def helper(self) -> Helper:\n"
                        "        pass\n")
                for c in common_activities:
                    f.write(f'    {c.replace(" ", "_").upper()} : Activity = Activity("{c}")\n')

                for i in defined_activities.items():
                    f.write('\n\n')
                    f.write(f'class {i[0].replace("_activity", "").title().replace("_", "")}(RoomActivity):\n')
                    f.write(f'    helper = Helper("input_select.{i[0]}")\n')
                    if len(i[1]["options"]) == len(common_activities):
                        f.write('    pass')
                    for o in i[1]["options"]:
                        if o not in common_activities:
                            f.write(f'    {o.replace(" ", "_").upper()}: Activity = Activity("{o}")\n')
        except yaml.YAMLError as exc:
            print(exc)