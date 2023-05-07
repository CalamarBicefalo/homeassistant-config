import yaml


def generate_rooms(root_dir: str):
    GENERATED_ROOMS = f'{root_dir}/rooms.py'

    with open("rooms.yaml", "r") as stream:
        rooms = yaml.safe_load(stream)
        try:
            with open(GENERATED_ROOMS, 'w') as f:
                f.write("from room import Room\n")
                f.write("from helpers import Helper\n")
                f.write("from strenum import StrEnum\n")
                f.write("from select_handler import SelectHandler\n")
                f.write("from appdaemon.plugins.hass import hassapi as hass\n")
                f.write("from typing import List\n")
                f.write('\n\n')
                for room in rooms:
                    f.write(f'class {class_name(room)}(Room):\n')
                    f.write(f'    class Activity(StrEnum):\n')
                    for activity in room["activities"]:
                        f.write(f'        {activity.replace(" ", "_").upper()} = "{activity}"\n')
                    f.write('\n')

                    f.write(f'    activity: SelectHandler[Activity]\n')
                    f.write(f'    _activity_helper : Helper = "input_select.{snake_name(room)}_activity"\n')
                    f.write(f'    name = "{room["name"]}"\n')
                    if "room_cleaner_segment" in room:
                        f.write(f'    _room_cleaner_segment = {room["room_cleaner_segment"]}\n')
                    f.write(f'    _last_cleaned_helper = Helper("input_datetime.last_cleaned_{snake_name(room)}")\n')
                    f.write('\n')

                    f.write(f'    def __init__(self, app: hass.Hass) -> None:\n')
                    f.write(f'        super().__init__(app)\n')
                    f.write(f'        self.activity = SelectHandler[{class_name(room)}.Activity](app, {class_name(room)}._activity_helper)\n')

                    f.write('\n\n')

                f.write(f'class RoomHandlers:\n')
                f.write(f'    all: List[Room]\n')
                for room in rooms:
                    f.write(f'    {snake_name(room)}: {class_name(room)}\n')
                f.write(f'    def __init__(self, app) -> None:\n')
                for room in rooms:
                    f.write(f'        self.{snake_name(room)} = {class_name(room)}(app)\n')
                f.write(f'        self.all = [{", ".join(map(lambda r: "self."+snake_name(r), rooms))}]\n')
                f.write('\n\n')
                f.write(f'class CommonActivities(StrEnum):\n')
                for activity in get_common_activities(rooms):
                    f.write(f'    {activity.replace(" ", "_").upper()} = "{activity}"\n')
                f.write('\n')

            with open("helpers/input_datetime/input_datetime_generated.yaml", 'w') as f:
                for room in rooms:
                    f.write(f'last_cleaned_{snake_name(room)}:\n')
                    f.write(f'    name: Last cleaned {room["name"]}\n')
                    f.write("    icon: mdi:broom\n")
                    f.write("    has_date: true\n")
                    f.write("    has_time: true\n")

            with open('helpers/input_select/input_select_generated.yaml', 'w') as f:
                for room in rooms:
                    f.write(f'{snake_name(room)}_activity:\n')
                    f.write(f'  name: {room["name"]} activity\n')
                    f.write(f'  icon: {room["icon"]}\n')
                    f.write(f'  options:\n')
                    for activity in room["activities"]:
                        f.write(f'    - {activity}\n')

        except yaml.YAMLError as exc:
            print(exc)

def get_common_activities(rooms):
    all_activities_by_room = [*map(lambda room: set(room["activities"]), rooms)]
    return set.intersection(*all_activities_by_room)

def generate_activities(root_dir: str):
    GENERATED_ACTIVITIES = f'{root_dir}/activities.py'

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
                    f.write(f'class {activity_enum_name(i)}(Activity):\n')
                    for o in i[1]["options"]:
                        f.write(f'    {o.replace(" ", "_").upper()} = "{o}"\n')

                f.write('\n')

                for i in defined_activities.items():
                    f.write(f'{activity_enum_name(i).lower()}_helper = Helper("input_select.{i[0]}")\n')



                f.write('\n')


                f.write('all_activity_helpers = [')
                for i in defined_activities.items():
                    f.write(f'{activity_enum_name(i).lower()}_helper, ')
                f.write(']')

                f.write('\n\n')

                f.write(f'class ActivityHandlers:\n')
                for i in defined_activities.items():
                    f.write(f'    {activity_enum_name(i).lower()}: SelectHandler[{activity_enum_name(i)}]\n')
                f.write(f'    def __init__(self, app) -> None:\n')
                for i in defined_activities.items():
                    f.write(f'        self.{activity_enum_name(i).lower()} = SelectHandler[{activity_enum_name(i)}](app, {activity_enum_name(i).lower()}_helper)\n')
        except yaml.YAMLError as exc:
            print(exc)


def activity_enum_name(activity_yaml_entries):
    return activity_yaml_entries[0].replace("_activity", "").title().replace("_", "")


def class_name(room_entry):
    return room_entry["name"].title().replace(" ", "")
def snake_name(room_entry):
    return room_entry["name"].lower().replace(" ", "_")
