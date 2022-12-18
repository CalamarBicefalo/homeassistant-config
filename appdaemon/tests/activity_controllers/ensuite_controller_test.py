import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import matchers
import services
import states as door
import states as motion
from activity_controllers.ensuite_controller import EnsuiteController


@automation_fixture(EnsuiteController)
def ensuite_controller():
    matchers.init()
    pass

current_activity = activities.Ensuite
new_activity = activities.Ensuite

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
    ),
    (
        current_activity.PRESENT, door.CLOSED,      # given
        motion.NOT_DETECTED,                        # when
        new_activity.EMPTY                          # then
    ),
]

door_test_cases = [
    (
        current_activity.EMPTY,        # given
        door.OPEN,                     # when
        new_activity.PRESENT           # then
    ),
    (
        current_activity.PRESENT,      # given
        door.OPEN,                     # when
        new_activity.PRESENT           # then
    ),
    (
        current_activity.SHOWERING,    # given
        door.OPEN,                     # when
        new_activity.PRESENT           # then
    ),
    (
        current_activity.EMPTY,        # given
        door.CLOSED,                   # when
        new_activity.EMPTY             # then
    ),
    (
        current_activity.PRESENT,      # given
        door.CLOSED,                   # when
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

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.ensuite_helper,
                                                                         new_activity)

@pytest.mark.parametrize("activity,doors,new_activity", door_test_cases)
def test_on_door(activity, doors, new_activity, given_that, ensuite_controller, assert_that):
    given_that.ensuite_has(activity=activity)

    ensuite_controller.on_door(None, None, None, doors, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.ensuite_helper,
                                                                         new_activity)


def ensuite_has(self, activity, door=door.OPEN):
    self.state_of(activities.ensuite_helper).is_set_to(activity)
    self.state_of(EnsuiteController.contact_sensor).is_set_to(door)


given.GivenThatWrapper.ensuite_has = ensuite_has
