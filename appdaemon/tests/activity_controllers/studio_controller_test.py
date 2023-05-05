import matchers
import pytest
from appdaemontestframework import automation_fixture

from rooms import *
import entities
import services
from activity_controllers.studio_controller import StudioController
import states


@automation_fixture(StudioController)
def subject():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, subject, assert_that):
    assert_that(subject) \
        .listens_to.state([
        entities.BINARY_SENSOR_STUDIO_MOTION,
        entities.BINARY_SENSOR_DESK_CHAIR_PS,
        entities.SENSOR_DRUMKIT_ACTIVE_POWER
    ]) \
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_when_away(given_that, subject, assert_that, time_travel):
    given_that.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(states.OFF)
    given_that.state_of(entities.SENSOR_DRUMKIT_ACTIVE_POWER).is_set_to(0)
    given_that.state_of(entities.BINARY_SENSOR_DESK_CHAIR_PS).is_set_to(states.OFF)

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(11).seconds()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, subject, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(states.ON)
    given_that.state_of(entities.SENSOR_DRUMKIT_ACTIVE_POWER).is_set_to(0)
    given_that.state_of(entities.BINARY_SENSOR_DESK_CHAIR_PS).is_set_to(states.OFF)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.PRESENT)


@pytest.mark.asyncio
def test_when_playing_drums(given_that, subject, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(states.ON)
    given_that.state_of(entities.SENSOR_DRUMKIT_ACTIVE_POWER).is_set_to(5.0)
    given_that.state_of(entities.BINARY_SENSOR_DESK_CHAIR_PS).is_set_to(states.OFF)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.DRUMMING)
@pytest.mark.asyncio
def test_when_spurious_power_reading(given_that, subject, assert_that):
    given_that.state_of(entities.SENSOR_DRUMKIT_ACTIVE_POWER).is_set_to(5.0)
    given_that.state_of(entities.BINARY_SENSOR_DESK_CHAIR_PS).is_set_to(states.OFF)

    subject.controller_handler(entities.SENSOR_DRUMKIT_ACTIVE_POWER, None, 1, "0.1", None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.DRUMMING)


@pytest.mark.asyncio
def test_when_working(given_that, subject, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(states.ON)
    given_that.state_of(entities.SENSOR_DRUMKIT_ACTIVE_POWER).is_set_to(0)
    given_that.state_of(entities.BINARY_SENSOR_DESK_CHAIR_PS).is_set_to(states.ON)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.WORKING)
