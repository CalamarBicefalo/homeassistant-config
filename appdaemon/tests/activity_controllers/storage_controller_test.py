import pytest
from appdaemontestframework import automation_fixture, given_that as given

import entities
from rooms import *
import matchers
import services
import states as door
from activity_controllers.storage_controller import StorageController


@automation_fixture(StorageController)
def subject():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_doors_open(given_that, subject, assert_that):
    given_that.storage_room_controller_state_is()
    subject.controller_handler(None, None, None, door.OPEN, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Storage._activity_helper,
                                                                         Storage.Activity.PRESENT)


@pytest.mark.asyncio
def test_when_doors_close(given_that, subject, assert_that):
    given_that.storage_room_controller_state_is()
    subject.controller_handler(None, None, None, door.CLOSED, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Storage._activity_helper,
                                                                         Storage.Activity.EMPTY)
@pytest.mark.asyncio
def test_when_doors_open_for_more_than_10_minutes(given_that, subject, assert_that, time_travel):
    given_that.storage_room_controller_state_is(activity=Storage.Activity.PRESENT)
    subject.controller_handler(None, None, None, door.OPEN, None)

    time_travel.fast_forward(11).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Storage._activity_helper,
                                                                         Storage.Activity.EMPTY)


def storage_room_controller_state_is(self, activity=Storage.Activity.EMPTY):
    self.state_of(entities.INPUT_BOOLEAN_ACTIVITY_LOCK_STORAGE).is_set_to(False)
    self.state_of(Storage._activity_helper).is_set_to(activity)

given.GivenThatWrapper.storage_room_controller_state_is = storage_room_controller_state_is
