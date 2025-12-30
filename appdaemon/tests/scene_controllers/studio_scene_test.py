from unittest import mock

import pytest
from appdaemontestframework import automation_fixture, given_that as given

from music import MusicHandler
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


@pytest.mark.asyncio
def test_when_working(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=Studio.Activity.WORKING, illuminance=30)

    with mock.patch.object(MusicHandler, 'play') as music:
        music.is_playing = lambda *_: False
        studio_scene.handlers.music = music
        studio_scene.handle_scene(Studio._activity_helper, None, None, None, None)

        music.play.assert_called_once()
        assert_that(scenes.STUDIO_WORKING.get()).was.turned_on()
        assert_that(entities.SWITCH_MONITOR).was.turned_on()


@pytest.mark.asyncio
def test_when_meeting(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=Studio.Activity.MEETING, illuminance=30)

    studio_scene.handle_scene(Studio._activity_helper, None, None, None, None)

    with mock.patch.object(MusicHandler, 'pause') as music:
        studio_scene.handlers.music = music
        studio_scene.handle_scene(Studio._activity_helper, None, None, None, None)

        music.pause.assert_called_once()


@pytest.mark.asyncio
def test_when_away(given_that, studio_scene, assert_that):
    given_that.studio_scene_is(activity=Studio.Activity.EMPTY, illuminance=30)

    with mock.patch.object(studio_scene.handlers.blinds, 'best_for_temperature'):
        studio_scene.handle_scene(Studio._activity_helper, None, None, None, None)

    assert_that(entities.SWITCH_MONITOR).was.turned_off()


def studio_scene_is(self, activity, illuminance, mode=selects.Mode.DAY):
    self.state_of(helpers.MODE).is_set_to(mode)
    self.state_of(entities.LIGHT_STUDIO).is_set_to(states.OFF)
    self.state_of(entities.SENSOR_MS_STUDIO_EP1_ILLUMINANCE).is_set_to(illuminance)
    self.state_of(Studio._activity_helper).is_set_to(activity)


given.GivenThatWrapper.studio_scene_is = studio_scene_is
