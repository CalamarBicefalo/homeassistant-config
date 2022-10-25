import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import devices
import helpers
import services
import states
from activity_controllers.studio import StudioActivity


@automation_fixture(StudioActivity)
def studio_activity():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, studio_activity, assert_that):
    assert_that(studio_activity) \
        .listens_to.state(devices.STUDIO_MOTION) \
        .with_callback(studio_activity.studio_activity_controller)


@pytest.mark.asyncio
async def test_when_away(given_that, studio_activity, assert_that):
    given_that.state_of(devices.STUDIO_MOTION).is_set_to(states.OFF)

    await studio_activity.studio_activity_controller(None, None, None, None, None)

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.STUDIO_ACTIVITY, activities.AWAY)


@pytest.mark.asyncio
async def test_when_present(given_that, studio_activity, assert_that):
    given_that.state_of(devices.STUDIO_MOTION).is_set_to(states.ON)

    await studio_activity.studio_activity_controller(None, None, None, None, None)

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.STUDIO_ACTIVITY, activities.PRESENT)
