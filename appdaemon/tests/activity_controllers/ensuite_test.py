import pytest, matchers

import activities
import entities
import services
from activity_controllers.ensuite_controller import EnsuiteController
import states
from appdaemontestframework import automation_fixture, given_that as given


@automation_fixture(EnsuiteController)
def subject():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_away(given_that, subject, assert_that):
    given_that.ensuite_state_is(motion=states.NOT_DETECTED)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.ensuite_helper,
                                                                         activities.Ensuite.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, subject, assert_that):
    given_that.ensuite_state_is(motion=states.DETECTED)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.ensuite_helper,
                                                                         activities.Ensuite.PRESENT)


@pytest.mark.asyncio
def test_when_door_closed_and_motion_detected(given_that, subject, assert_that):
    given_that.ensuite_state_is(motion=states.DETECTED, door=states.CLOSED)

    subject.controller_handler(entities.BINARY_SENSOR_ENSUITE_MOTION, None, None, states.DETECTED, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.ensuite_helper,
                                                                         activities.Ensuite.SHOWERING)

@pytest.mark.asyncio
def test_when_showering_ignores_motion(given_that, subject, assert_that):
    given_that.ensuite_state_is(activity=activities.Ensuite.SHOWERING)

    subject.controller_handler(entities.BINARY_SENSOR_ENSUITE_MOTION, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(activities.ensuite_helper,
                                                                         activities.Ensuite.EMPTY)


def ensuite_state_is(self, motion=states.NOT_DETECTED, activity=activities.Ensuite.EMPTY, door=states.OPEN):
    activity_handlers = activities.ActivityHandlers(None)
    self.state_of(activity_handlers.ensuite._helper).is_set_to(activity)
    self.state_of(entities.BINARY_SENSOR_BATHROOM_CS_CONTACT).is_set_to(door)
    self.state_of(entities.BINARY_SENSOR_ENSUITE_MOTION).is_set_to(motion)


given.GivenThatWrapper.ensuite_state_is = ensuite_state_is
del ensuite_state_is  # clean up namespace
