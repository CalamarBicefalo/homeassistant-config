from datetime import datetime

import devices, vacuum_location, hass
from appdaemontestframework import assert_that


def sent_for_maintenance_to_kitchen(self):
    self.called_with(
        entity_id=devices.VACUUM_CLEANER,
        x_coord=vacuum_location.mop_maintenance.x,
        y_coord=vacuum_location.mop_maintenance.y
    )


def sent_to_clean_kitchen(self):
    self.called_with(
        entity_id=devices.VACUUM_CLEANER,
        segments=vacuum_location.kitchen_segment
    )


def set_to_activity(self, helper, activity):
    self.called_with(
        entity_id=helper,
        option=activity,
    )


def set_to_now(self, helper):
    self.called_with(
        entity_id=helper,
        datetime=hass.datetime_to_helper(datetime.now()),
    )


assert_that.Was.sent_for_maintenance_to_kitchen = sent_for_maintenance_to_kitchen
assert_that.Was.sent_to_clean_kitchen = sent_to_clean_kitchen
assert_that.Was.set_to_now = set_to_now
assert_that.Was.set_to_activity = set_to_activity

del sent_for_maintenance_to_kitchen  # clean up namespace
del sent_to_clean_kitchen  # clean up namespace
del set_to_now  # clean up namespace
del set_to_activity  # clean up namespace


def init():
    return None
