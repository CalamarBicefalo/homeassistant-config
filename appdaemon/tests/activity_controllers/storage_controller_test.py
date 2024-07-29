import pytest
from appdaemontestframework import automation_fixture, given_that as given

import entities
from rooms import *
import matchers
import services
import states as door
import states as motion
from activity_controllers.storage_controller import StorageController


@automation_fixture(StorageController)
def storage_controller():
    matchers.init()
    pass

current_activity = Storage.Activity
new_activity = Storage.Activity

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
        new_activity.PRESENT                      # then
    ),
    (
        current_activity.PRESENT, door.CLOSED,      # given
        motion.DETECTED,                            # when
        new_activity.PRESENT                      # then
    )
]

door_test_cases = [
    (
        current_activity.EMPTY, motion.NOT_DETECTED,    # given
        door.OPEN,                                      # when
        new_activity.PRESENT                            # then
    ),
    (
        current_activity.EMPTY, motion.DETECTED,        # given
        door.CLOSED,                                    # when
        None                                            # then
    ),
    (
        current_activity.PRESENT, motion.DETECTED,      # given
        door.OPEN,                                      # when
        None                                            # then
    ),
    (
        current_activity.PRESENT, motion.DETECTED,      # given
        door.CLOSED,                                    # when
        None                                            # then
    ),
]

@pytest.mark.parametrize("activity,doors,motion,new_activity", motion_test_cases)
def test_on_motion(activity, doors, motion, new_activity, given_that, storage_controller, assert_that):
    given_that.storage_has(activity=activity, door=doors, motion=motion)

    storage_controller.on_motion(None, None, None, motion, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Storage._activity_helper,
                                                                         new_activity)

@pytest.mark.parametrize("activity,motion,doors,new_activity", door_test_cases)
def test_on_door(activity, motion, doors, new_activity, given_that, storage_controller, assert_that):
    given_that.storage_has(activity=activity, motion=motion)

    storage_controller.on_door(None, None, None, doors, None)

    if new_activity:
        assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Storage._activity_helper,
                                                                             new_activity)
    else:
        assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.called()


def test_after_25_minutes_sets_to_empty(given_that, storage_controller, assert_that, time_travel):
    given_that.storage_has(activity=Storage.Activity.PRESENT, door=door.OPEN)
    storage_controller.on_motion(None, None, None, motion.DETECTED, None)

    time_travel.fast_forward(26).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Storage._activity_helper,
                                                                         Storage.Activity.EMPTY)


def test_after_30_sec_of_inactivity_sets_to_empty(given_that, storage_controller, assert_that, time_travel):
    given_that.storage_has(activity=Storage.Activity.PRESENT, door=door.OPEN, motion=motion.NOT_DETECTED)
    storage_controller.on_motion(None, None, None, motion.NOT_DETECTED, None)

    time_travel.fast_forward(30).seconds()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Storage._activity_helper,
                                                                         Storage.Activity.EMPTY)


def storage_has(self, activity, door=door.OPEN, motion=motion.DETECTED):
    self.state_of(entities.INPUT_BOOLEAN_ACTIVITY_LOCK_STORAGE).is_set_to(False)
    self.state_of(Storage._activity_helper).is_set_to(activity)
    self.state_of(StorageController.contact_sensor).is_set_to(door)
    self.state_of(StorageController.motion_sensor).is_set_to(motion)


given.GivenThatWrapper.storage_has = storage_has
