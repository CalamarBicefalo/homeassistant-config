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
        entities.SENSOR_AMANDA_M1AIR_C02FX084Q6LX_PRIMARY_DISPLAY_ID,
        entities.BINARY_SENSOR_AMANDA_M1AIR_C02FX084Q6LX_ACTIVE,
        entities.SENSOR_AMANDA_M1AIR_C02FX084Q6LX_ACTIVE_AUDIO_INPUT
    ]) \
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_when_away(given_that, subject, assert_that, time_travel):
    given_that.studio_state_is(
        motion = states.OFF,
        activity = Studio.Activity.PRESENT
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
def test_when_working(given_that, subject, assert_that):
    given_that.studio_state_is(
        laptop_active=states.ON,
        connected_to_monitor=True
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.WORKING)


@pytest.mark.asyncio
def test_when_meeting(given_that, subject, assert_that):
    given_that.studio_state_is(
        laptop_audio=states.ON,
        laptop_active=states.ON,
        connected_to_monitor=True
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Studio._activity_helper,
                                                                         Studio.Activity.MEETING)


def studio_state_is(self, motion=states.OFF, laptop_active=states.OFF, connected_to_monitor=False, 
                    laptop_audio=states.OFF, activity=Studio.Activity.EMPTY):
    self.state_of(entities.INPUT_BOOLEAN_ACTIVITY_LOCK_STUDIO).is_set_to(False)
    self.state_of(Studio._activity_helper).is_set_to(activity)
    self.state_of(entities.SENSOR_AMANDA_M1AIR_C02FX084Q6LX_SSID).is_set_to('SETE-2SE-5G')
    self.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(motion)
    self.state_of(entities.BINARY_SENSOR_AMANDA_M1AIR_C02FX084Q6LX_ACTIVE).is_set_to(laptop_active)
    self.state_of(entities.SENSOR_AMANDA_M1AIR_C02FX084Q6LX_PRIMARY_DISPLAY_ID).is_set_to(
        "388CDA68-6885-B1E3-0857-D6964E3302DB" if connected_to_monitor else "other"
    )
    self.state_of(entities.BINARY_SENSOR_AMANDA_M1AIR_C02FX084Q6LX_AUDIO_INPUT_IN_USE).is_set_to(laptop_audio)
    self.state_of(entities.BINARY_SENSOR_AMANDA_M1AIR_C02FX084Q6LX_AUDIO_OUTPUT_IN_USE).is_set_to(laptop_audio)


given.GivenThatWrapper.studio_state_is = studio_state_is
