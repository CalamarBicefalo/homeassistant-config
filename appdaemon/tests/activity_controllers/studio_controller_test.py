import matchers
import pytest
from appdaemontestframework import automation_fixture, given_that as given

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
        entities.SENSOR_DRUMKIT_ACTIVE_POWER,
        entities.BINARY_SENSOR_SNYK_LAPTOP_AUDIO_INPUT_IN_USE
    ]) \
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_when_away(given_that, subject, assert_that, time_travel):
    given_that.studio_state_is(
        motion = states.OFF,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(11).seconds()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, subject, assert_that):
    given_that.studio_state_is(
        motion = states.ON,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.PRESENT)


@pytest.mark.asyncio
def test_when_playing_drums(given_that, subject, assert_that):
    given_that.studio_state_is(
        drumkit_power = 5.0,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.DRUMMING)
@pytest.mark.asyncio
def test_when_spurious_power_reading(given_that, subject, assert_that):
    given_that.studio_state_is(
        drumkit_power = 5.0,
    )

    subject.controller_handler(entities.SENSOR_DRUMKIT_ACTIVE_POWER, None, 1, "0.1", None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.DRUMMING)


@pytest.mark.asyncio
def test_when_working(given_that, subject, assert_that):
    given_that.studio_state_is(
        chair = states.ON
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.WORKING)


@pytest.mark.asyncio
def test_when_meeting(given_that, subject, assert_that):
    given_that.studio_state_is(
        laptop_audio = states.ON,
        chair = states.ON
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.MEETING)


def studio_state_is(self, motion=states.OFF, chair=states.OFF, drumkit_power=0, laptop_audio=states.OFF):
    self.state_of(Studio._activity_helper).is_set_to(Studio.Activity.EMPTY)
    self.state_of(entities.SENSOR_SNYK_LAPTOP_SSID).is_set_to('SETE-2SE-5G')
    self.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(motion)
    self.state_of(entities.SENSOR_DRUMKIT_ACTIVE_POWER).is_set_to(drumkit_power)
    self.state_of(entities.BINARY_SENSOR_DESK_CHAIR_PS).is_set_to(chair)
    self.state_of(entities.BINARY_SENSOR_SNYK_LAPTOP_AUDIO_INPUT_IN_USE).is_set_to(laptop_audio)


given.GivenThatWrapper.studio_state_is = studio_state_is
