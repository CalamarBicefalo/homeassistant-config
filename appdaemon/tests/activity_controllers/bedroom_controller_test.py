import pytest
from appdaemontestframework import automation_fixture, given_that as given

from rooms import *
import entities
import matchers
import services
import states
from activity_controllers.bedroom_controller import BedroomController


@automation_fixture(BedroomController)
def subject() -> None:
    matchers.init()
    pass


def test_triggers_when_motion(given_that, subject, assert_that):
    assert_that(subject) \
        .listens_to.state(
        [entities.BINARY_SENSOR_BEDROOM_MS_MOTION]) \
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_when_no_motion_then_empty(given_that, subject, assert_that, time_travel):
    given_that.bedroom_state_is(
        motion=states.OFF,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(1).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Bedroom._activity_helper,
                                                                         Bedroom.Activity.EMPTY)


@pytest.mark.asyncio
def test_when_motion_then_present(given_that, subject, assert_that):
    given_that.bedroom_state_is(motion=states.ON)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Bedroom._activity_helper,
                                                                         Bedroom.Activity.PRESENT)


@pytest.mark.asyncio
def test_given_relaxing_when_motion_then_keeps_relaxing(given_that, subject, assert_that):
    given_that.bedroom_state_is(
        motion=states.ON,
        activity=Bedroom.Activity.RELAXING,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Bedroom._activity_helper,
                                                                             Bedroom.Activity.PRESENT)


@pytest.mark.asyncio
def test_given_bedtime_when_motion_then_keeps_bedtime(given_that, subject, assert_that):
    given_that.bedroom_state_is(
        motion=states.ON,
        activity=Bedroom.Activity.BEDTIME,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Bedroom._activity_helper,
                                                                             Bedroom.Activity.PRESENT)


@pytest.mark.asyncio
def test_given_relaxing_when_no_motion_then_keeps_relaxing_for_up_to_30_minutes(given_that, subject, assert_that,
                                                                                time_travel):
    given_that.bedroom_state_is(
        motion=states.OFF,
        activity=Bedroom.Activity.RELAXING,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(29).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Bedroom._activity_helper,
                                                                             Bedroom.Activity.EMPTY)


@pytest.mark.asyncio
def test_given_relaxing_when_no_motion_then_sets_empty_afger_30_minutes(given_that, subject, assert_that, time_travel):
    given_that.bedroom_state_is(
        motion=states.OFF,
        activity=Bedroom.Activity.RELAXING,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(31).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(Bedroom._activity_helper,
                                                                         Bedroom.Activity.EMPTY)


@pytest.mark.asyncio
def test_after_3_hours_of_inactivity_then_empty(given_that, subject, assert_that, time_travel):
    given_that.bedroom_state_is(
        motion=states.ON,
    )
    subject.controller_handler(None, None, None, None, None)

    time_travel.fast_forward(180).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION). \
        was.set_to_activity(Bedroom._activity_helper, Bedroom.Activity.EMPTY)


def bedroom_state_is(self, motion=states.OFF, activity=Bedroom.Activity.EMPTY):
    self.state_of(entities.BINARY_SENSOR_BEDROOM_MS_MOTION).is_set_to(motion)
    self.state_of(Bedroom._activity_helper).is_set_to(activity)


given.GivenThatWrapper.bedroom_state_is = bedroom_state_is
