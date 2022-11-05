import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import helpers
import matchers
import utils
from scenes_controller.studio_scene import StudioScene


@automation_fixture(StudioScene)
def studio_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
async def test_when_empty(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=activities.Studio.EMPTY, illuminance=100)

    await studio_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.LIGHT_STUDIO).was.turned_off()


@pytest.mark.asyncio
async def test_when_bright(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=activities.Studio.PRESENT, illuminance=100)

    await studio_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.LIGHT_STUDIO).was.turned_off()

@pytest.mark.asyncio
async def test_when_present(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=activities.Studio.PRESENT, illuminance=30)

    await studio_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.SCENE_STUDIO_CONCENTRATE).was.turned_on()


@pytest.mark.asyncio
async def test_when_working_and_dark(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=activities.Studio.WORKING, illuminance=30)

    await studio_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.SCENE_STUDIO_WORKING).was.turned_on()
    assert_that(entities.SWITCH_MONITOR_PLUG).was.turned_on()


@pytest.mark.asyncio
async def test_when_working_and_bright(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=activities.Studio.WORKING, illuminance=100)

    await studio_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.LIGHT_STUDIO).was.turned_off()
    assert_that(entities.SWITCH_MONITOR_PLUG).was.turned_on()


@pytest.mark.asyncio
async def test_when_drumming_and_dark(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=activities.Studio.DRUMMING, illuminance=30)

    await studio_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.SCENE_STUDIO_DRUMMING).was.turned_on()


def studio_scene_is(self, activity, illuminance):
    self.state_of(entities.SENSOR_DESK_MS_ILLUMINANCE).is_set_to(utils.awaitable(illuminance))
    self.state_of(helpers.STUDIO_ACTIVITY).is_set_to(utils.awaitable(activity))


given.GivenThatWrapper.studio_scene_is = studio_scene_is
