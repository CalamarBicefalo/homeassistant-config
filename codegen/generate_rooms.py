from typing import Any

import yaml
from jinja2 import Environment, PackageLoader


def generate_rooms(root_dir: str) -> None:
    GENERATED_ROOMS = f'{root_dir}/rooms.py'
    env = Environment(
        loader=PackageLoader("codegen"),
    )
    env.globals['get_common_activities'] = get_common_activities
    with open("rooms.yaml", "r") as stream:
        rooms_descriptor = yaml.safe_load(stream)
        rooms = load_rooms(rooms_descriptor)
        try:
            with open(GENERATED_ROOMS, 'w') as f:
                template = env.get_template("rooms.py.jinja2")
                f.write(template.render(rooms=rooms))

            with open("devices/templates/templates_generated.yaml", 'w') as f:
                template = env.get_template("templates_generated.yaml.jinja2")
                f.write(template.render(rooms=rooms))

            with open("helpers/input_boolean/input_boolean_generated.yaml", 'w') as f:
                for room in rooms:
                    f.write(f'activity_lock_{snake_name(room)}:\n')
                    f.write(f'    name: Activity lock {room["name"]}\n')
                    f.write("    icon: mdi:lock\n")

                    f.write("\n\n")

            with open("helpers/input_datetime/input_datetime_generated.yaml", 'w') as f:
                for room in rooms:
                    f.write(f'last_cleaned_{snake_name(room)}:\n')
                    f.write(f'    name: Last cleaned {room["name"]}\n')
                    f.write("    icon: mdi:broom\n")
                    f.write("    has_date: true\n")
                    f.write("    has_time: true\n")

                    f.write("\n\n")

                    f.write(f'last_present_{snake_name(room)}:\n')
                    f.write(f'    name: Last present {room["name"]}\n')
                    f.write("    icon: mdi:account-check\n")
                    f.write("    has_date: true\n")
                    f.write("    has_time: true\n")

            with open('helpers/input_select/input_select_generated.yaml', 'w') as f:
                for room in rooms:
                    f.write(f'{snake_name(room)}_activity:\n')
                    f.write(f'  name: {room["name"]} activity\n')
                    f.write(f'  icon: {room["icon"]}\n')
                    f.write(f'  options:\n')
                    for activity in room["activities"]:
                        f.write(f'    - {activity["name"]}\n')

        except yaml.YAMLError as exc:
            print(exc)


def load_rooms(rooms_descriptor) -> list[Any]:
    open_floor_tuples = rooms_descriptor["open_floor"]
    rooms = rooms_descriptor["rooms"]
    for tuple in open_floor_tuples:
        for room in rooms:
            if room["name"] in tuple:
                room["open_floor"] = list(filter(lambda x: x != room["name"], tuple))

    return rooms


def get_common_activities(rooms):
    all_activities_by_room = [*map(lambda room: set(map(lambda activity: activity["name"], room["activities"])), rooms)]
    ca = list(set.intersection(*all_activities_by_room))
    ca.sort()
    return ca


def activity_enum_name(activity_yaml_entries):
    return activity_yaml_entries[0].replace("_activity", "").title().replace("_", "")


def class_name(room_entry):
    return room_entry["name"].title().replace(" ", "")


def snake_name(room_entry):
    return room_entry["name"].lower().replace(" ", "_")
