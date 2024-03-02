from datetime import datetime

from appdaemontestframework import assert_that, given_that

import app
import helpers


def set_to_option(self, helper, activity):
    self.called_with(
        entity_id=helper,
        option=activity,
    )

def set_to_activity(self, helper, activity):
    self.called_with(
        entity_id=helper,
        option=activity,
    )


def set_to_now(self, helper):
    self.called_with(
        entity_id=helper,
        datetime=helpers.datetime_to_helper(datetime.now()),
    )


assert_that.Was.set_to_now = set_to_now
assert_that.Was.set_to_activity = set_to_activity
assert_that.Was.set_to_option = set_to_option

del set_to_now  # clean up namespace
del set_to_activity  # clean up namespace
del set_to_option  # clean up namespace


def init():
    return None
