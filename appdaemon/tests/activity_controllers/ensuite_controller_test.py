import pytest
from appdaemontestframework import automation_fixture, given_that as given

from rooms import *
import matchers
import services
import states as door
import states as motion
from activity_controllers.ensuite_controller import EnsuiteController


@automation_fixture(EnsuiteController)
def ensuite_controller():
    matchers.init()
    pass

current_activity = Ensuite.Activity
new_activity = Ensuite.Activity

motion_test_cases = [
    (
        current_activity.EMPTY, door.OPEN,          # given
        motion.DETECTED,                            # when
        new_activity.PRESENT                        # then
    ),
    (
        current_activity.PRESENT, door.OPEN,        # given
        motion.DETECTED,                            # when
        new_activity.PRESENT                        # then
    ),
    (
        current_activity.EMPTY, door.CLOSED,        # given
        motion.DETECTED,                            # when
        new_activity.SHOWERING                      # then
    ),
    (
        current_activity.PRESENT, door.CLOSED,      # given
        motion.DETECTED,                            # when
        new_activity.SHOWERING                      # then
    )
]

door_test_cases = [
    (
        current_activity.EMPTY,        # given
        door.OPEN,                     # when
        new_activity.PRESENT           # then
    ),
    (
        current_activity.EMPTY,        # given
        door.CLOSED,                   # when
        None                           # then
    ),
    (
        current_activity.PRESENT,      # given
        door.OPEN,                     # when
        None                           # then
    ),
    (
        current_activity.PRESENT,      # given
        door.CLOSED,                   # when
        None                           # then
    ),
    (
        current_activity.SHOWERING,    # given
        door.OPEN,                     # when
        new_activity.PRESENT           # then
    ),
    (
        current_activity.SHOWERING,    # given
        door.CLOSED,                   # when
        new_activity.PRESENT           # then
    ),
]

@pytest.mark.parametrize("activity,doors,motion,new_activity", motion_test_cases)
def test_on_motion(activity, doors, motion, new_activity, given_that, ensuite_controller, assert_that):
    given_that.ensuite_has(activity=activity, door=doors)

    ensuite_controller.on_motion(None, None, None, motion, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Ensuite._activity_helper,
                                                                         new_activity)

@pytest.mark.parametrize("activity,doors,new_activity", door_test_cases)
def test_on_door(activity, doors, new_activity, given_that, ensuite_controller, assert_that):
    given_that.ensuite_has(activity=activity)

    ensuite_controller.on_door(None, None, None, doors, None)

    if new_activity:
        assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Ensuite._activity_helper,
                                                                         new_activity)
    else:
        assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.called()


def test_showering_timer_holds_for_33_minutes(given_that, ensuite_controller, assert_that, time_travel):
    enable_showering(ensuite_controller, given_that)

    time_travel.fast_forward(32).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Ensuite._activity_helper,
                                                                         Ensuite.Activity.EMPTY)
def test_after_34_minutes_showering_mode_is_disabled(given_that, ensuite_controller, assert_that, time_travel):
    enable_showering(ensuite_controller, given_that)

    time_travel.fast_forward(34).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Ensuite._activity_helper,
                                                                         Ensuite.Activity.EMPTY)


def test_after_25_minutes_sets_to_empty(given_that, ensuite_controller, assert_that, time_travel):
    given_that.ensuite_has(activity=Ensuite.Activity.EMPTY, door=door.OPEN)
    ensuite_controller.on_motion(None, None, None, motion.DETECTED, None)

    time_travel.fast_forward(26).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Ensuite._activity_helper,
                                                                         Ensuite.Activity.EMPTY)


def test_after_1_minute_of_inactivity_sets_to_empty(given_that, ensuite_controller, assert_that, time_travel):
    given_that.ensuite_has(activity=Ensuite.Activity.PRESENT, door=door.OPEN)
    ensuite_controller.on_motion(None, None, None, motion.NOT_DETECTED, None)

    time_travel.fast_forward(1).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Ensuite._activity_helper,
                                                                         Ensuite.Activity.EMPTY)


def enable_showering(ensuite_controller, given_that):
    given_that.ensuite_has(activity=Ensuite.Activity.EMPTY, door=door.CLOSED)
    ensuite_controller.on_motion(None, None, None, motion.DETECTED, None)


def ensuite_has(self, activity, door=door.OPEN):
    self.state_of(Ensuite._activity_helper).is_set_to(activity)
    self.state_of(EnsuiteController.contact_sensor).is_set_to(door)


given.GivenThatWrapper.ensuite_has = ensuite_has
