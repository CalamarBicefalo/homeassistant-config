import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import devices
import helpers
import services
import states
from activity_controllers.kitchen import KitchenActivity


@automation_fixture(KitchenActivity)
def kitchen_activity():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, kitchen_activity, assert_that):
    assert_that(kitchen_activity) \
        .listens_to.state(devices.KITCHEN_MOTION) \
        .with_callback(kitchen_activity.kitchen_activity_controller)


@pytest.mark.asyncio
async def test_when_away(given_that, kitchen_activity, assert_that):
    given_that.state_of(devices.KITCHEN_MOTION).is_set_to(states.OFF)

    await kitchen_activity.kitchen_activity_controller()

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.KITCHEN_ACTIVITY, activities.AWAY)


@pytest.mark.asyncio
async def test_when_present(given_that, kitchen_activity, assert_that):
    given_that.state_of(devices.KITCHEN_MOTION).is_set_to(states.ON)

    await kitchen_activity.kitchen_activity_controller()

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.KITCHEN_ACTIVITY, activities.PRESENT)
