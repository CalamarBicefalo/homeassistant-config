import matchers
import pytest
from appdaemontestframework import automation_fixture, given_that as given

from rooms import *
import entities
import services
from activity_controllers.living_room_controller import LivingRoomController
import states


@automation_fixture(LivingRoomController)
def subject() -> None:
    matchers.init()
    pass


def test_triggers_when_motion_or_tv_changes(given_that, subject, assert_that):
    assert_that(subject) \
        .listens_to.state(
        [
            entities.BINARY_SENSOR_LIVING_ROOM_MOTION,
            entities.MEDIA_PLAYER_TV_2,
            entities.MEDIA_PLAYER_SONY_KD_49XF8096,
            entities.BINARY_SENSOR_SOFA_PS
        ]
    )\
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_waits_for_away_before_cooldown(given_that, subject, assert_that, time_travel):
    given_that.living_room_state_is(
        motion=states.OFF,
        tv=states.OFF,
        sofa=states.OFF,
        activity=LivingRoom.Activity.PRESENT
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(10).seconds()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(LivingRoom._activity_helper,
                                                                         LivingRoom.Activity.EMPTY)

@pytest.mark.asyncio
def test_sets_away_after_cooldown(given_that, subject, assert_that, time_travel):
    given_that.living_room_state_is(
        motion=states.OFF,
        tv=states.OFF,
        sofa=states.OFF,
        activity=LivingRoom.Activity.PRESENT
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(30).seconds()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(LivingRoom._activity_helper,
                                                                         LivingRoom.Activity.EMPTY)


@pytest.mark.asyncio
def test_sets_present(given_that, subject, assert_that):
    given_that.living_room_state_is(motion=states.ON)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(LivingRoom._activity_helper,
                                                                         LivingRoom.Activity.PRESENT)


@pytest.mark.asyncio
def test_sets_watching_tv(given_that, subject, assert_that):
    given_that.living_room_state_is(tv=states.ON)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(LivingRoom._activity_helper,
                                                                         LivingRoom.Activity.WATCHING_TV)


@pytest.mark.asyncio
def test_sets_playing_ps5(given_that, subject, assert_that):
    given_that.living_room_state_is(tv=states.ON, tv_attr={'source': 'PlayStation 5'})

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(LivingRoom._activity_helper,
                                                                         LivingRoom.Activity.GAMING)


@pytest.mark.asyncio
def test_presence_going_on_when_drumming_keeps_drumming(given_that, subject, assert_that):
    given_that.living_room_state_is(
        motion=states.ON,
        activity=LivingRoom.Activity.DRUMMING,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(LivingRoom._activity_helper,
                                                                         LivingRoom.Activity.PRESENT)



@pytest.mark.asyncio
def test_presence_going_off_when_drumming_keeps_drumming_for_10_minutes(given_that, subject, assert_that, time_travel):
    given_that.living_room_state_is(
        motion=states.OFF,
        activity=LivingRoom.Activity.DRUMMING,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(9).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(LivingRoom._activity_helper,
                                                                             LivingRoom.Activity.EMPTY)

@pytest.mark.asyncio
def test_presence_going_off_when_drumming_sets_empty_after_10_minutes(given_that, subject, assert_that, time_travel):
    given_that.living_room_state_is(
        motion=states.OFF,
        activity=LivingRoom.Activity.DRUMMING,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(11).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(LivingRoom._activity_helper,
                                                                         LivingRoom.Activity.EMPTY)



@pytest.mark.asyncio
def test_turn_on_tv_when_drumming_enables_watching_tv_activity(given_that, subject, assert_that, time_travel):
    given_that.living_room_state_is(tv=states.ON, activity=LivingRoom.Activity.DRUMMING)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(LivingRoom._activity_helper,
                                                                         LivingRoom.Activity.WATCHING_TV)


# @pytest.mark.asyncio
# def test_sets_relaxing(given_that, subject, assert_that):
#     given_that.living_room_state_is(sofa=states.ON)
#
#     subject.controller_handler(None, None, None, None, None)
#
#     assert_that(services.INPUT_SELECT_SELECT_OPTION). \
#         was.set_to_activity(LivingRoom._activity_helper, LivingRoom.Activity.RELAXING)


@pytest.mark.asyncio
def test_after_3_hours_of_inactivity(given_that, subject, assert_that, time_travel):
    given_that.living_room_state_is(
        motion=states.ON,
        sofa=states.ON,
        activity=LivingRoom.Activity.PRESENT
    )
    subject.controller_handler(None, None, None, None, None)

    time_travel.fast_forward(180).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION). \
        was.set_to_activity(LivingRoom._activity_helper, LivingRoom.Activity.EMPTY)


def living_room_state_is(self, motion=states.OFF, tv=states.OFF, sofa=states.OFF, activity=LivingRoom.Activity.EMPTY, tv_attr=None):
    self.state_of(entities.INPUT_BOOLEAN_ACTIVITY_LOCK_LIVING_ROOM).is_set_to(False)
    self.state_of(entities.MEDIA_PLAYER_SONY_KD_49XF8096).is_set_to(tv, tv_attr)
    self.state_of(entities.BINARY_SENSOR_LIVING_ROOM_MOTION).is_set_to(motion)
    self.state_of(entities.MEDIA_PLAYER_TV_2).is_set_to(tv)
    self.state_of(entities.BINARY_SENSOR_SOFA_PS).is_set_to(sofa)
    self.state_of(LivingRoom._activity_helper).is_set_to(activity)


given.GivenThatWrapper.living_room_state_is = living_room_state_is
