import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import devices
import helpers
import services
import states
from activity_controllers.living_room import LivingRoomActivity
from utils import awaitable


@automation_fixture(LivingRoomActivity)
def living_room_activity():
    matchers.init()
    pass


def test_triggers_when_motion_or_tv_changes(given_that, living_room_activity, assert_that):
    assert_that(living_room_activity) \
        .listens_to.state([devices.LIVING_ROOM_MOTION, devices.TV]) \
        .with_callback(living_room_activity.living_room_activity_controller)


@pytest.mark.asyncio
async def test_when_away(given_that, living_room_activity, assert_that):
    given_that.state_of(devices.LIVING_ROOM_MOTION).is_set_to(awaitable(states.OFF))
    given_that.state_of(devices.TV).is_set_to(awaitable(states.OFF))

    await living_room_activity.living_room_activity_controller(None, None, None, None, None)

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY, activities.EMPTY)


@pytest.mark.asyncio
async def test_when_present(given_that, living_room_activity, assert_that):
    given_that.state_of(devices.LIVING_ROOM_MOTION).is_set_to(awaitable(states.ON))
    given_that.state_of(devices.TV).is_set_to(awaitable(states.OFF))

    await living_room_activity.living_room_activity_controller(None, None, None, None, None)

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY, activities.PRESENT)


@pytest.mark.asyncio
async def test_when_watching_tv(given_that, living_room_activity, assert_that):
    given_that.state_of(devices.LIVING_ROOM_MOTION).is_set_to(awaitable(states.ON))
    given_that.state_of(devices.TV).is_set_to(awaitable(states.ON))

    await living_room_activity.living_room_activity_controller(None, None, None, None, None)

    assert_that(services.HELPER_SELECT_SET).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY, activities.WATCHING_TV)
