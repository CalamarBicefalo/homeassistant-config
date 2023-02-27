import matchers
import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import services
from utils import states
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
def test_when_away(given_that, subject, assert_that, time_travel):
    given_that.bedroom_state_is(
        motion=states.OFF,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(1).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.bedroom_helper,
                                                                         activities.Bedroom.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, subject, assert_that):
    given_that.bedroom_state_is(motion=states.ON)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.bedroom_helper,
                                                                         activities.Bedroom.PRESENT)


@pytest.mark.asyncio
def test_presence_going_on_when_relaxing_keeps_relaxing(given_that, subject, assert_that):
    given_that.bedroom_state_is(
        motion=states.ON,
        activity=activities.Bedroom.RELAXING,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(activities.bedroom_helper,
                                                                         activities.Bedroom.PRESENT)

@pytest.mark.asyncio
def test_presence_going_off_when_bedtime_keeps_bedtime(given_that, subject, assert_that):
    given_that.bedroom_state_is(
        motion=states.ON,
        activity=activities.Bedroom.BEDTIME,
    )

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(activities.bedroom_helper,
                                                                         activities.Bedroom.PRESENT)



@pytest.mark.asyncio
def test_presence_going_off_when_relaxing_keeps_relaxing_for_30_minutes(given_that, subject, assert_that, time_travel):
    given_that.bedroom_state_is(
        motion=states.OFF,
        activity=activities.Bedroom.RELAXING,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(29).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(activities.bedroom_helper,
                                                                             activities.Bedroom.EMPTY)

@pytest.mark.asyncio
def test_presence_going_off_when_relaxing_sets_empty_after_30_minutes(given_that, subject, assert_that, time_travel):
    given_that.bedroom_state_is(
        motion=states.OFF,
        activity=activities.Bedroom.RELAXING,
    )

    subject.controller_handler(None, None, None, None, None)
    time_travel.fast_forward(31).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.bedroom_helper,
                                                                         activities.Bedroom.EMPTY)



@pytest.mark.asyncio
def test_after_3_hours_of_inactivity(given_that, subject, assert_that, time_travel):
    given_that.bedroom_state_is(
        motion=states.ON,
    )
    subject.controller_handler(None, None, None, None, None)

    time_travel.fast_forward(180).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION). \
        was.set_to_activity(activities.bedroom_helper, activities.Bedroom.EMPTY)


def bedroom_state_is(self, motion=states.OFF, activity=activities.Bedroom.EMPTY):
    self.state_of(entities.BINARY_SENSOR_BEDROOM_MS_MOTION).is_set_to(motion)
    self.state_of(activities.bedroom_helper).is_set_to(activity)


given.GivenThatWrapper.bedroom_state_is = bedroom_state_is
