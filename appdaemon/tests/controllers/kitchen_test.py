import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import entities
import services
from controllers.kitchen_controller import KitchenController
from test_utils import awaitable
from utils import states


@automation_fixture(KitchenController)
def kitchen_activity():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, kitchen_activity, assert_that):
    assert_that(kitchen_activity) \
        .listens_to.state([entities.BINARY_SENSOR_KITCHEN_MOTION]) \
        .with_callback(kitchen_activity.controller_handler)


@pytest.mark.asyncio
def test_when_away(given_that, kitchen_activity, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_KITCHEN_MOTION).is_set_to(awaitable(states.OFF))

    kitchen_activity.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.Kitchen.helper, activities.Kitchen.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, kitchen_activity, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_KITCHEN_MOTION).is_set_to(awaitable(states.ON))

    kitchen_activity.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.Kitchen.helper, activities.Kitchen.PRESENT)
