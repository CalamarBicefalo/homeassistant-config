import matchers
import pytest
from appdaemontestframework import automation_fixture, given_that as given

from rooms import *
import entities
import services
import states
from activity_controllers.wardrobe_controller import WardrobeController


@automation_fixture(WardrobeController)
def subject() -> None:
    matchers.init()
    pass


def test_triggers_when_motion_or_doors_changes(given_that, subject, assert_that):
    assert_that(subject) \
        .listens_to.state(
        [
            entities.BINARY_SENSOR_WARDROBE_MS_MOTION,
            entities.BINARY_SENSOR_VS_WARDROBE_MIDDLE_DOOR_VIBRATION,
            entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR,
            entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE,
            entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE,
        ]).with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_when_away(given_that, subject, assert_that, time_travel):
    given_that.wardrobe_state_is(
        motion=states.OFF,
        activity=Wardrobe.Activity.PRESENT,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(1).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Wardrobe._activity_helper,
                                                                         Wardrobe.Activity.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, subject, assert_that):
    given_that.wardrobe_state_is(motion=states.ON)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Wardrobe._activity_helper,
                                                                         Wardrobe.Activity.PRESENT)

@pytest.mark.asyncio
def test_given_wardrobe_open_when_entering(given_that, subject, assert_that):
    given_that.wardrobe_state_is(motion=states.ON, wardrobe_right_door=states.OPEN)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Wardrobe._activity_helper,
                                                                         Wardrobe.Activity.PRESENT)

@pytest.mark.asyncio
def test_when_dressing(given_that, subject, assert_that):
    given_that.wardrobe_state_is(motion=states.ON, wardrobe_right_door=states.OPEN)

    subject.controller_handler(entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Wardrobe._activity_helper,
                                                                         Wardrobe.Activity.DRESSING)

@pytest.mark.asyncio
def test_when_dressing_and_close_doors_waits_for_a_bit(given_that, subject, assert_that, time_travel):
    given_that.wardrobe_state_is(activity=Wardrobe.Activity.DRESSING)

    subject.controller_handler(entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Wardrobe._activity_helper,
                                                                         Wardrobe.Activity.EMPTY)
    time_travel.fast_forward(1).minutes()
    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Wardrobe._activity_helper,
                                                                             Wardrobe.Activity.EMPTY)

@pytest.mark.asyncio
def test_given_dressing_when_all_wardrobe_sensors_off(given_that, subject, assert_that):
    given_that.wardrobe_state_is(motion=states.OFF)

    subject.controller_handler(entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Wardrobe._activity_helper,
                                                                         Wardrobe.Activity.PRESENT)

@pytest.mark.asyncio
def test_given_dressing_timesout_after_10_minutes(given_that, subject, assert_that, time_travel):
    given_that.wardrobe_state_is(
        motion=states.OFF,
        wardrobe_right_door=states.OPEN,
        activity=Wardrobe.Activity.DRESSING,
    )

    subject.controller_handler(entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE, None, None, None, None)
    time_travel.fast_forward(11).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Wardrobe._activity_helper,
                                                                         Wardrobe.Activity.EMPTY)


@pytest.mark.asyncio
def test_after_3_hours_of_inactivity(given_that, subject, assert_that, time_travel):
    given_that.wardrobe_state_is(
        motion=states.ON,
        activity=Wardrobe.Activity.PRESENT,
    )
    subject.controller_handler(None, None, None, None, None)

    time_travel.fast_forward(180).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION). \
        was.set_to_activity(Wardrobe._activity_helper, Wardrobe.Activity.EMPTY)


def wardrobe_state_is(self,
                      motion=states.OFF,
                      activity=Wardrobe.Activity.EMPTY,
                      wardrobe_motion=states.OFF,
                      wardrobe_right_door=states.CLOSED,
                      wardrobe_left_door=states.CLOSED):
    self.state_of(entities.INPUT_BOOLEAN_ACTIVITY_LOCK_WARDROBE).is_set_to(False)
    self.state_of(entities.BINARY_SENSOR_WARDROBE_MS_MOTION).is_set_to(motion)
    self.state_of(entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR).is_set_to(wardrobe_motion)
    self.state_of(entities.BINARY_SENSOR_VS_WARDROBE_MIDDLE_DOOR_VIBRATION).is_set_to(states.OFF)
    self.state_of(entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE).is_set_to(wardrobe_right_door)
    self.state_of(entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE).is_set_to(wardrobe_left_door)
    self.state_of(Wardrobe._activity_helper).is_set_to(activity)


given.GivenThatWrapper.wardrobe_state_is = wardrobe_state_is
