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
from scene_controllers.office_scene import OfficeScene


@automation_fixture(OfficeScene)
def office_scene() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_working_activity_plays_music_and_manages_blinds(given_that, office_scene, assert_that):
    given_that.office_scene_is(activity=Office.Activity.WORKING, illuminance=30)

    with mock.patch.object(MusicHandler, 'play') as music:
        music.is_playing = lambda *_: False
        office_scene.handlers.music = music
        
        with mock.patch.object(office_scene.handlers.blinds, 'best_for_temperature') as blinds:
            office_scene.handle_scene(Office._activity_helper, None, None, None, None)

            music.play.assert_called_once()
            blinds.assert_called_once()
            assert_that(scenes.OFFICE_NATURAL_LIGHT_3.get()).was.turned_on()


@pytest.mark.asyncio
def test_meeting_activity_pauses_music(given_that, office_scene, assert_that):
    given_that.office_scene_is(activity=Office.Activity.MEETING, illuminance=30)

    with mock.patch.object(MusicHandler, 'pause') as music:
        office_scene.handlers.music = music
        
        with mock.patch.object(office_scene.handlers.blinds, 'best_for_temperature'):
            office_scene.handle_scene(Office._activity_helper, None, None, None, None)

            music.pause.assert_called_once()


@pytest.mark.asyncio
def test_drumming_activity_closes_blinds_and_stops_media(given_that, office_scene, assert_that):
    given_that.office_scene_is(activity=Office.Activity.DRUMMING, illuminance=30)

    with mock.patch.object(office_scene.handlers.blinds, 'close') as blinds_close:
        office_scene.handle_scene(Office._activity_helper, None, None, None, None)

        assert_that(scenes.OFFICE_DRUMMING.get()).was.turned_on()
        assert_that(entities.LIGHT_DRUM_POWER_STRIP_SPEAKERS).was.turned_on()
        assert_that(entities.LIGHT_DRUM_POWER_STRIP_LIGHT).was.turned_on()
        assert_that(entities.LIGHT_DRUM_POWER_STRIP_USB).was.turned_on()
        assert_that(entities.LIGHT_DRUM_POWER_STRIP_FOCUSRITE).was.turned_on()
        assert_that(entities.LIGHT_DRUM_POWER_STRIP_DRUMS).was.turned_on()
        blinds_close.assert_called_once()


@pytest.mark.asyncio
def test_snaring_activity_closes_blinds_and_stops_media(given_that, office_scene, assert_that):
    given_that.office_scene_is(activity=Office.Activity.SNARING, illuminance=30)

    with mock.patch.object(office_scene.handlers.blinds, 'close') as blinds_close:
        office_scene.handle_scene(Office._activity_helper, None, None, None, None)

        assert_that(scenes.OFFICE_SNARING.get()).was.turned_on()
        blinds_close.assert_called_once()


@pytest.mark.asyncio
def test_empty_activity_turns_off_lights(given_that, office_scene, assert_that):
    given_that.office_scene_is(activity=Office.Activity.EMPTY, illuminance=30)

    office_scene.handle_scene(Office._activity_helper, None, None, None, None)

    assert_that(entities.LIGHT_OFFICE).was.turned_off()


def office_scene_is(self, activity, illuminance, mode=selects.Mode.DAY):
    self.state_of(helpers.MODE).is_set_to(mode)
    self.state_of(entities.LIGHT_OFFICE).is_set_to(states.OFF)
    self.state_of(entities.SENSOR_MS_STUDIO_EP1_ILLUMINANCE).is_set_to(illuminance)
    self.state_of(Office._activity_helper).is_set_to(activity)


given.GivenThatWrapper.office_scene_is = office_scene_is
