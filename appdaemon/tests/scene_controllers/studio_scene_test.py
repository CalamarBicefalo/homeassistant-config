import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import helpers
import matchers
import modes
import scenes
import states
from scene_controllers.studio_scene import StudioScene


@automation_fixture(StudioScene)
def studio_scene() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_working(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=activities.Studio.WORKING, illuminance=30)

    studio_scene.handle_scene(activities.studio_helper, None, None, None, None)

    assert_that(scenes.STUDIO_WORKING.get()).was.turned_on()
    assert_that(entities.SWITCH_MONITOR_PLUG).was.turned_on()


@pytest.mark.asyncio
def test_when_drumming(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=activities.Studio.DRUMMING, illuminance=30)

    studio_scene.handle_scene(activities.studio_helper, None, None, None, None)

    assert_that(scenes.STUDIO_DRUMMING.get()).was.turned_on()


def studio_scene_is(self, activity, illuminance, mode=modes.Mode.DAY):
    self.state_of(helpers.HOMEASSISTANT_MODE).is_set_to(mode)
    self.state_of(entities.LIGHT_STUDIO).is_set_to(states.OFF)
    self.state_of(entities.SENSOR_DESK_MS_ILLUMINANCE).is_set_to(illuminance)
    self.state_of(activities.studio_helper).is_set_to(activity)


given.GivenThatWrapper.studio_scene_is = studio_scene_is
