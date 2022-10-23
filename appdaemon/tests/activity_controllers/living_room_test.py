import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import devices
import helpers
import services
import states
from activity_controllers.living_room import LivingRoomActivity


@automation_fixture(LivingRoomActivity)
def living_room_activity():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, living_room_activity, assert_that):
    assert_that(living_room_activity) \
        .listens_to.state(devices.LIVING_ROOM_MOTION) \
        .with_callback(living_room_activity.living_room_activity_controller)


@pytest.mark.asyncio
async def test_when_away(given_that, living_room_activity, assert_that):
    given_that.state_of(devices.LIVING_ROOM_MOTION).is_set_to(states.OFF)
    given_that.state_of(devices.TV).is_set_to(states.OFF)

    await living_room_activity.living_room_activity_controller()

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY, activities.AWAY)


@pytest.mark.asyncio
async def test_when_present(given_that, living_room_activity, assert_that):
    given_that.state_of(devices.LIVING_ROOM_MOTION).is_set_to(states.ON)
    given_that.state_of(devices.TV).is_set_to(states.OFF)

    await living_room_activity.living_room_activity_controller()

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY, activities.PRESENT)


@pytest.mark.asyncio
async def test_when_watching_tv(given_that, living_room_activity, assert_that):
    given_that.state_of(devices.LIVING_ROOM_MOTION).is_set_to(states.ON)
    given_that.state_of(devices.TV).is_set_to(states.ON)

    await living_room_activity.living_room_activity_controller()

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY, activities.WATCHING_TV)
