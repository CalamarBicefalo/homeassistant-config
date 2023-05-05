from typing import NewType
from datetime import datetime
Helper = NewType('Helper', str)
HELPER_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'




def datetime_to_helper(d: datetime) -> str:
    return d.strftime(HELPER_DATETIME_FORMAT)

def helper_to_datetime(helper_state: str) -> datetime:
    return datetime.strptime(str(helper_state), HELPER_DATETIME_FORMAT)
