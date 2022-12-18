import matchers
import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import services
from activity_controllers.living_room_controller import LivingRoomController
from test_utils import awaitable
import states


@automation_fixture(LivingRoomController)
def subject():
    matchers.init()
    pass


def test_triggers_when_motion_or_tv_changes(given_that, subject, assert_that):
    assert_that(subject) \
        .listens_to.state([entities.BINARY_SENSOR_LIVING_ROOM_MOTION, entities.MEDIA_PLAYER_TV, entities.BINARY_SENSOR_SOFA_PS_WATER]) \
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_when_away(given_that, subject, assert_that):
    given_that.living_room_state_is(
        motion=states.OFF,
        tv=states.OFF,
        sofa=states.OFF,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.livingroom_helper,
                                                                         activities.LivingRoom.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, subject, assert_that):
    given_that.living_room_state_is(
        motion=states.ON,
        tv=states.OFF,
        sofa=states.OFF,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.livingroom_helper,
                                                                         activities.LivingRoom.PRESENT)


@pytest.mark.asyncio
def test_when_watching_tv(given_that, subject, assert_that):
    given_that.living_room_state_is(
        motion=states.ON,
        tv=states.ON,
        sofa=states.ON,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.livingroom_helper,
                                                                         activities.LivingRoom.WATCHING_TV)


@pytest.mark.asyncio
def test_when_sitting_on_sofa(given_that, subject, assert_that):
    given_that.living_room_state_is(
        motion=states.ON,
        tv=states.OFF,
        sofa=states.ON,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION). \
        was.set_to_activity(activities.livingroom_helper, activities.LivingRoom.READING)

@pytest.mark.asyncio
def test_after_3_hours_of_inactivity(given_that, subject, assert_that, time_travel):
    given_that.living_room_state_is(
        motion=states.ON,
        tv=states.OFF,
        sofa=states.ON,
    )
    subject.controller_handler(None, None, None, None, None)

    time_travel.fast_forward(180).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION). \
        was.set_to_activity(activities.livingroom_helper, activities.LivingRoom.EMPTY)


def living_room_state_is(self, motion, tv, sofa):
    self.state_of(entities.BINARY_SENSOR_LIVING_ROOM_MOTION).is_set_to(motion)
    self.state_of(entities.MEDIA_PLAYER_TV).is_set_to(tv)
    self.state_of(entities.BINARY_SENSOR_SOFA_PS_WATER).is_set_to(sofa)


given.GivenThatWrapper.living_room_state_is = living_room_state_is
