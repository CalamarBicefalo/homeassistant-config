import pytest
from appdaemontestframework import automation_fixture

import activities
import matchers
import services
from utils import states as door
from activity_controllers.storage_room_controller import StorageRoomController


@automation_fixture(StorageRoomController)
def subject():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_doors_open(given_that, subject, assert_that):
    subject.controller_handler(None, None, None, door.OPEN, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.storageroom_helper,
                                                                         activities.StorageRoom.PRESENT)


@pytest.mark.asyncio
def test_when_doors_close(given_that, subject, assert_that):
    subject.controller_handler(None, None, None, door.CLOSED, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.storageroom_helper,
                                                                         activities.StorageRoom.EMPTY)
@pytest.mark.asyncio
def test_when_doors_open_for_more_than_10_minutes(given_that, subject, assert_that, time_travel):
    subject.controller_handler(None, None, None, door.OPEN, None)

    time_travel.fast_forward(11).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.storageroom_helper,
                                                                         activities.StorageRoom.EMPTY)
