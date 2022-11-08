from typing import NewType
Helper = NewType('Helper', str)

LAST_COOKED = Helper("input_datetime.last_cooked")
LAST_CLEANED_KITCHEN = Helper("input_datetime.last_cleaned_kitchen")
LAST_CLEANED_VACUUM_MOP = Helper("input_datetime.last_cleaned_vacuum_mop")
KITCHEN_ACTIVITY = Helper("input_select.kitchen_activity")
LIVING_ROOM_ACTIVITY = Helper("input_select.living_room_activity")
STUDIO_ACTIVITY = Helper("input_select.studio_activity")
ENSUITE_ACTIVITY = Helper("input_select.ensuite_activity")
