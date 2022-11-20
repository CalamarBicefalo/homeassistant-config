from typing import NewType
Helper = NewType('Helper', str)


LAST_COOKED = Helper("input_datetime.last_cooked")
LAST_CLEANED_KITCHEN = Helper("input_datetime.last_cleaned_kitchen")
LAST_CLEANED_VACUUM_MOP = Helper("input_datetime.last_cleaned_vacuum_mop")
