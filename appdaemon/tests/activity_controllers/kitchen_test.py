import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import entities
import services
from activity_controllers.kitchen_controller import KitchenController
from test_utils import awaitable
import states


@automation_fixture(KitchenController)
def subject():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, subject, assert_that):
    assert_that(subject) \
        .listens_to.state([entities.BINARY_SENSOR_KITCHEN_MOTION]) \
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_when_away(given_that, subject, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_KITCHEN_MOTION).is_set_to(states.OFF)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.kitchen_helper, activities.Kitchen.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, subject, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_KITCHEN_MOTION).is_set_to(states.ON)

    subject.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.kitchen_helper, activities.Kitchen.PRESENT)
