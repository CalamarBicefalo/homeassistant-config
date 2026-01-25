import matchers
import pytest
from appdaemontestframework import automation_fixture, given_that as given

from rooms import *
import entities
import services
from activity_controllers.office_controller import OfficeController
import states


@automation_fixture(OfficeController)
def subject():
    matchers.init()
    pass


def test_listens_to_relevant_sensors(given_that, subject, assert_that):
    assert_that(subject) \
        .listens_to.state([
        entities.BINARY_SENSOR_OFFICE_MOTION,
        entities.BINARY_SENSOR_DESK_CHAIR_PS,
        entities.BINARY_SENSOR_SNYK_LAPTOP_AUDIO_INPUT_IN_USE,
        entities.BINARY_SENSOR_DRUMS_VIBRATION
    ]) \
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_transitions_to_empty_after_timeout(given_that, subject, assert_that, time_travel):
    given_that.office_state_is(
        motion=states.OFF,
        activity=Office.Activity.PRESENT
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(2).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Office._activity_helper,
                                                                         Office.Activity.EMPTY)


@pytest.mark.asyncio
def test_detects_presence_from_motion(given_that, subject, assert_that):
    given_that.office_state_is(
        motion=states.ON,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Office._activity_helper,
                                                                         Office.Activity.PRESENT)


@pytest.mark.asyncio
def test_detects_working_when_sitting_at_desk(given_that, subject, assert_that):
    given_that.office_state_is(
        chair=states.ON
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Office._activity_helper,
                                                                         Office.Activity.WORKING)


@pytest.mark.asyncio
def test_detects_meeting_when_audio_active(given_that, subject, assert_that):
    given_that.office_state_is(
        laptop_audio=states.ON,
        chair=states.ON
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Office._activity_helper,
                                                                         Office.Activity.MEETING)


@pytest.mark.asyncio
def test_detects_drumming_from_vibration_sensor(given_that, subject, assert_that):
    given_that.office_state_is(
        drums_vibration=states.ON
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Office._activity_helper,
                                                                         Office.Activity.DRUMMING)


@pytest.mark.asyncio
def test_maintains_drumming_state_without_interruption(given_that, subject, assert_that):
    given_that.office_state_is(
        motion=states.ON,
        activity=Office.Activity.DRUMMING
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Office._activity_helper,
                                                                         Office.Activity.PRESENT)


@pytest.mark.asyncio
def test_snaring_state_prevents_interruption(given_that, subject, assert_that):
    given_that.office_state_is(
        motion=states.ON,
        chair=states.ON,
        activity=Office.Activity.SNARING
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Office._activity_helper,
                                                                         Office.Activity.WORKING)


def office_state_is(self, motion=states.OFF, chair=states.OFF, laptop_audio=states.OFF, 
                    drums_vibration=states.OFF, activity=Office.Activity.EMPTY):
    self.state_of(entities.INPUT_BOOLEAN_ACTIVITY_LOCK_OFFICE).is_set_to(False)
    self.state_of(Office._activity_helper).is_set_to(activity)
    self.state_of(entities.SENSOR_SNYK_LAPTOP_SSID).is_set_to('SETE-2SE-5G')
    self.state_of(entities.BINARY_SENSOR_OFFICE_MOTION).is_set_to(motion)
    self.state_of(entities.BINARY_SENSOR_DESK_CHAIR_PS).is_set_to(chair)
    self.state_of(entities.BINARY_SENSOR_SNYK_LAPTOP_AUDIO_INPUT_IN_USE).is_set_to(laptop_audio)
    self.state_of(entities.BINARY_SENSOR_SNYK_LAPTOP_AUDIO_OUTPUT_IN_USE).is_set_to(laptop_audio)
    self.state_of(entities.BINARY_SENSOR_DRUMS_VIBRATION).is_set_to(drums_vibration)


given.GivenThatWrapper.office_state_is = office_state_is
