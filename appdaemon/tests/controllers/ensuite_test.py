import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import entities
import services
from controllers.ensuite_controller import EnsuiteController
from test_utils import awaitable
from utils import states


@automation_fixture(EnsuiteController)
def ensuite_activity():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, ensuite_activity, assert_that):
    assert_that(ensuite_activity) \
        .listens_to.state([entities.BINARY_SENSOR_ENSUITE_MOTION]) \
        .with_callback(ensuite_activity.controller_handler)


@pytest.mark.asyncio
def test_when_away(given_that, ensuite_activity, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_ENSUITE_MOTION).is_set_to(awaitable(states.OFF))

    ensuite_activity.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.Ensuite.helper, activities.Ensuite.EMPTY)


@pytest.mark.asyncio
def test_when_present(given_that, ensuite_activity, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_ENSUITE_MOTION).is_set_to(awaitable(states.ON))

    ensuite_activity.controller_handler(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.Ensuite.helper, activities.Ensuite.PRESENT)
