from unittest import mock

import pytest
from appdaemontestframework import automation_fixture, given_that as given

from rooms import *
import entities
import helpers
import matchers
import selects
import scenes
import states
from music import MusicHandler
from scene_controllers.bedroom_scene import BedroomScene


@automation_fixture(BedroomScene)
def bedroom_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_relaxing_sets_relaxing_scene(given_that, bedroom_scene, assert_that):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.RELAXING, illuminance=30, are_lights_on=False)

    bedroom_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.BEDROOM_RELAXING.get()).was.turned_on()


@pytest.mark.asyncio
def test_relaxing_plays_music(given_that, bedroom_scene) -> None:
    given_that.bedroom_scene_is(activity=Bedroom.Activity.RELAXING)

    with mock.patch.object(MusicHandler, 'play') as music:
        music.is_playing = lambda *_: False
        bedroom_scene.handlers.music = music
        bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)

        music.play.assert_called_once()


@pytest.mark.asyncio
def test_empty_activity_adjusts_blinds(given_that, bedroom_scene, assert_that):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.EMPTY, illuminance=30)

    with mock.patch.object(bedroom_scene.handlers.blinds, 'best_for_temperature'):
        bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)

    assert_that(entities.LIGHT_BEDROOM).was.turned_off()


@pytest.mark.asyncio
def test_mode_change_adjusts_blinds_when_empty(given_that, bedroom_scene):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.EMPTY, mode=selects.Mode.DAY)

    with mock.patch.object(bedroom_scene.handlers.blinds, 'best_for_temperature') as blinds_mock:
        bedroom_scene.on_mode_change(selects.Mode.NIGHT, selects.Mode.DAY)
        blinds_mock.assert_called_once()


@pytest.mark.asyncio
def test_mode_change_adjusts_blinds_when_away(given_that, bedroom_scene):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.PRESENT, mode=selects.Mode.DAY)

    with mock.patch.object(bedroom_scene.handlers.blinds, 'best_for_temperature') as blinds_mock:
        bedroom_scene.on_mode_change(selects.Mode.AWAY, selects.Mode.DAY)
        blinds_mock.assert_called_once()


def bedroom_scene_is(self, activity, illuminance=0, are_lights_on=False, mode=selects.Mode.NIGHT,
                         playing_music=states.OFF):
    self.state_of(entities.COVER_BEDROOM_CURTAIN_COVER).is_set_to(states.OPEN)
    self.state_of(entities.MEDIA_PLAYER_BEDROOM_SPEAKERS).is_set_to(playing_music)
    self.state_of(helpers.MODE).is_set_to(mode)
    self.state_of(entities.SENSOR_BEDROOM_MS_EPL_ILLUMINANCE).is_set_to(illuminance)
    self.state_of(Bedroom._activity_helper).is_set_to(activity)
    if are_lights_on:
        self.state_of(entities.LIGHT_BEDROOM).is_set_to(states.ON)
    else:
        self.state_of(entities.LIGHT_BEDROOM).is_set_to(states.OFF)


given.GivenThatWrapper.bedroom_scene_is = bedroom_scene_is
