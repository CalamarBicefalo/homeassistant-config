import pytest
from appdaemontestframework import automation_fixture, given_that as given

from fakes.blinds_handler_fake import FakeBlindsHandler, BEST_FOR_TEMPERATURE
from fakes.music_handler_fake import FakeMusicHandler
from rooms import *
import entities
import helpers
import matchers
import selects
import scenes
import states
from scene_controllers.studio_scene import StudioScene


@automation_fixture(StudioScene)
def studio_scene() -> None:
    matchers.init()
    pass


@pytest.fixture
def fake_blinds():
    return FakeBlindsHandler()


@pytest.fixture
def fake_music():
    return FakeMusicHandler()


@pytest.fixture(autouse=True)
def setup_fakes(studio_scene, fake_blinds, fake_music):
    studio_scene.handlers.blinds = fake_blinds
    studio_scene.handlers.music = fake_music


@pytest.mark.asyncio
def test_when_working(given_that, studio_scene, fake_music, assert_that):
    given_that.studio_scene_is(activity=Studio.Activity.WORKING, illuminance=30)

    studio_scene.handle_scene(Studio._activity_helper, None, None, None, None)

    assert fake_music.is_playing()
    assert_that(scenes.STUDIO_WORKING.get()).was.turned_on()
    assert_that(entities.SWITCH_MONITOR).was.turned_on()


@pytest.mark.asyncio
def test_when_meeting(given_that, studio_scene, fake_music, assert_that):
    given_that.studio_scene_is(activity=Studio.Activity.MEETING, illuminance=30)

    studio_scene.handle_scene(Studio._activity_helper, None, None, None, None)

    assert not fake_music.is_playing()


@pytest.mark.asyncio
def test_when_empty_turns_off_monitor_and_adjusts_blinds(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=Studio.Activity.EMPTY, illuminance=30)

    studio_scene.handle_scene(Studio._activity_helper, None, None, None, None)

    assert_that(entities.SWITCH_MONITOR).was.turned_off()


@pytest.mark.asyncio
def test_mode_change_always_adjusts_blinds(given_that, studio_scene, fake_blinds):
    given_that.studio_scene_is(activity=Studio.Activity.WORKING, illuminance=30, mode=selects.Mode.DAY)

    studio_scene.on_mode_change(selects.Mode.NIGHT, selects.Mode.DAY)
    
    assert fake_blinds.get_position() == BEST_FOR_TEMPERATURE


def studio_scene_is(self, activity, illuminance, mode=selects.Mode.DAY):
    self.state_of(helpers.MODE).is_set_to(mode)
    self.state_of(entities.LIGHT_STUDIO).is_set_to(states.OFF)
    self.state_of(entities.SENSOR_MS_STUDIO_EP1_ILLUMINANCE).is_set_to(illuminance)
    self.state_of(Studio._activity_helper).is_set_to(activity)


given.GivenThatWrapper.studio_scene_is = studio_scene_is
