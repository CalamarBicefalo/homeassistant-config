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
                f.write("from helpers import Helper\n")
                f.write("from strenum import StrEnum\n")
                f.write("from select_handler import SelectHandler\n")
                f.write('\n\n')
                f.write("class Activity(StrEnum):\n")
                f.write("    pass\n")
                f.write('\n\n')
                f.write(f'class Common(Activity):\n')
                for c in common_activities:
                    f.write(f'    {c.replace(" ", "_").upper()} = "{c}"\n')

                for i in defined_activities.items():
                    f.write('\n\n')
                    f.write(f'class {enum_name(i)}(Activity):\n')
                    for o in i[1]["options"]:
                        f.write(f'    {o.replace(" ", "_").upper()} = "{o}"\n')

                f.write('\n')

                for i in defined_activities.items():
                    f.write(f'{enum_name(i).lower()}_helper = Helper("input_select.{i[0]}")\n')


                f.write(f'class ActivityHandlers:\n')
                for i in defined_activities.items():
                    f.write(f'    {enum_name(i).lower()}: SelectHandler[{enum_name(i)}]\n')
                f.write(f'    def __init__(self, app) -> None:\n')
                for i in defined_activities.items():
                    f.write(f'        self.{enum_name(i).lower()} = SelectHandler[{enum_name(i)}](app, {enum_name(i).lower()}_helper)\n')
        except yaml.YAMLError as exc:
            print(exc)


def enum_name(activity_yaml_entries):
    return activity_yaml_entries[0].replace("_activity", "").title().replace("_", "")
