import matchers
import pytest
from appdaemontestframework import automation_fixture

import activities
import entities
import helpers
import services
import states
from activity_controllers.studio import StudioActivity
from utils import awaitable


@automation_fixture(StudioActivity)
def studio_activity():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, studio_activity, assert_that):
    assert_that(studio_activity) \
        .listens_to.state(entities.BINARY_SENSOR_STUDIO_MOTION) \
        .with_callback(studio_activity.studio_activity_controller)


def test_triggers_when_working_chair(given_that, studio_activity, assert_that):
    assert_that(studio_activity) \
        .listens_to.state(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER) \
        .with_callback(studio_activity.studio_activity_controller)


def test_triggers_when_drum_plug(given_that, studio_activity, assert_that):
    assert_that(studio_activity) \
        .listens_to.state(entities.SENSOR_DRUMS_PLUG_POWER) \
        .with_callback(studio_activity.studio_activity_controller)


@pytest.mark.asyncio
async def test_when_away(given_that, studio_activity, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(awaitable(states.OFF))
    given_that.state_of(entities.SENSOR_DRUMS_PLUG_POWER).is_set_to(awaitable(0))
    given_that.state_of(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER).is_set_to(awaitable(states.OFF))

    await studio_activity.studio_activity_controller(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(helpers.STUDIO_ACTIVITY, activities.Studio.EMPTY)


@pytest.mark.asyncio
async def test_when_present(given_that, studio_activity, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(awaitable(states.ON))
    given_that.state_of(entities.SENSOR_DRUMS_PLUG_POWER).is_set_to(awaitable(0))
    given_that.state_of(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER).is_set_to(awaitable(states.OFF))

    await studio_activity.studio_activity_controller(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(helpers.STUDIO_ACTIVITY, activities.Studio.PRESENT)


@pytest.mark.asyncio
async def test_when_playing_drums(given_that, studio_activity, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(awaitable(states.ON))
    given_that.state_of(entities.SENSOR_DRUMS_PLUG_POWER).is_set_to(awaitable(5.0))
    given_that.state_of(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER).is_set_to(awaitable(states.OFF))

    await studio_activity.studio_activity_controller(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(helpers.STUDIO_ACTIVITY, activities.Studio.DRUMMING)


@pytest.mark.asyncio
async def test_when_working(given_that, studio_activity, assert_that):
    given_that.state_of(entities.BINARY_SENSOR_STUDIO_MOTION).is_set_to(awaitable(states.ON))
    given_that.state_of(entities.SENSOR_DRUMS_PLUG_POWER).is_set_to(awaitable(0))
    given_that.state_of(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER).is_set_to(awaitable(states.ON))

    await studio_activity.studio_activity_controller(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(helpers.STUDIO_ACTIVITY, activities.Studio.WORKING)
