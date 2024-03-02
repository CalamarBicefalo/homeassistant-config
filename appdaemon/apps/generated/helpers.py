from typing import NewType
from datetime import datetime
Helper = NewType('Helper', str)
HELPER_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


LAST_COOKED = Helper("input_datetime.last_cooked")
LAST_CLEANED_FLAT = Helper("input_datetime.last_cleaned_flat")
LAST_CLEANED_VACUUM_MOP = Helper("input_datetime.last_cleaned_vacuum_mop")
LAST_WASHED_CLOTHES = Helper("input_datetime.last_washed_clothes")
GUEST_MODE = Helper("input_boolean.guest_mode")
MODE = Helper("input_select.mode")
WASHING_MACHINE = Helper("input_select.washing_machine")


def datetime_to_helper(d: datetime) -> str:
    return d.strftime(HELPER_DATETIME_FORMAT)

def helper_to_datetime(helper_state: str) -> datetime:
    return datetime.strptime(str(helper_state), HELPER_DATETIME_FORMAT)
