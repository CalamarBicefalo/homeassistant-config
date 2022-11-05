from datetime import datetime

from appdaemontestframework import assert_that

import app
from activities import Activity


def set_to_activity(self, helper, activity: Activity):
    self.called_with(
        entity_id=helper,
        option=activity,
    )


def set_to_now(self, helper):
    self.called_with(
        entity_id=helper,
        datetime=app.datetime_to_helper(datetime.now()),
    )


assert_that.Was.set_to_now = set_to_now
assert_that.Was.set_to_activity = set_to_activity

del set_to_now  # clean up namespace
del set_to_activity  # clean up namespace


def init():
    return None
