from typing import NewType
from datetime import datetime
Helper = NewType('Helper', str)
HELPER_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


LAST_COOKED = Helper("input_datetime.last_cooked")
LAST_CLEANED_FLAT = Helper("input_datetime.last_cleaned_flat")
LAST_CLEANED_VACUUM_MOP = Helper("input_datetime.last_cleaned_vacuum_mop")
HOMEASSISTANT_MODE = Helper("input_select.homeassistant_mode")


def datetime_to_helper(d: datetime) -> str:
    return d.strftime(HELPER_DATETIME_FORMAT)

def helper_to_datetime(helper_state: str) -> datetime:
    return datetime.strptime(str(helper_state), HELPER_DATETIME_FORMAT)
