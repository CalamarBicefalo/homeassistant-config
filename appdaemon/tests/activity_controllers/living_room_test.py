import matchers
import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
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
        .listens_to.state([entities.BINARY_SENSOR_LIVING_ROOM_MOTION, entities.MEDIA_PLAYER_TV]) \
        .with_callback(living_room_activity.controller_handler)


@pytest.mark.asyncio
async def test_when_away(given_that, living_room_activity, assert_that):
    given_that.living_room_state_is(
        motion=states.OFF,
        tv=states.OFF,
        sofa=states.OFF,
    )

    await living_room_activity.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY,
                                                                         activities.LivingRoom.EMPTY)


@pytest.mark.asyncio
async def test_when_present(given_that, living_room_activity, assert_that):
    given_that.living_room_state_is(
        motion=states.ON,
        tv=states.OFF,
        sofa=states.OFF,
    )

    await living_room_activity.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY,
                                                                         activities.LivingRoom.PRESENT)


@pytest.mark.asyncio
async def test_when_watching_tv(given_that, living_room_activity, assert_that):
    given_that.living_room_state_is(
        motion=states.ON,
        tv=states.ON,
        sofa=states.ON,
    )

    await living_room_activity.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY,
                                                                         activities.LivingRoom.WATCHING_TV)


@pytest.mark.asyncio
async def test_when_sitting_on_sofa(given_that, living_room_activity, assert_that):
    given_that.living_room_state_is(
        motion=states.ON,
        tv=states.OFF,
        sofa=states.ON,
    )

    await living_room_activity.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION). \
        was.set_to_activity(helpers.LIVING_ROOM_ACTIVITY, activities.LivingRoom.READING)


def living_room_state_is(self, motion, tv, sofa):
    self.state_of(entities.BINARY_SENSOR_LIVING_ROOM_MOTION).is_set_to(awaitable(motion))
    self.state_of(entities.MEDIA_PLAYER_TV).is_set_to(awaitable(tv))
    self.state_of(entities.BINARY_SENSOR_SOFA_PS_WATER).is_set_to(awaitable(sofa))


given.GivenThatWrapper.living_room_state_is = living_room_state_is
