from unittest import mock

import pytest
from appdaemontestframework import automation_fixture, given_that as given

from blinds_handler import BlindsHandler
from rooms import *
import entities
import helpers
import matchers
import modes
import scenes
import states
from music import MusicHandler
from scene_controllers.living_room_scene import LivingRoomScene


@automation_fixture(LivingRoomScene)
def living_room_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_reading_sets_reading_scene(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.READING, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.LIVING_ROOM_READING.get()).was.turned_on()


@pytest.mark.asyncio
def test_reading_plays_music(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.READING)

    with mock.patch.object(MusicHandler, 'play') as music:
        music.is_playing = lambda *_: False
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.music = music
        scene.handle_scene(None, None, None, None, None)

        music.play.assert_called_once()


@pytest.mark.asyncio
def test_reading_when_music_playing_does_not_play_music(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.READING)

    with mock.patch.object(MusicHandler, 'play') as music:
        music.is_playing = lambda *_: True
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.music = music
        scene.handle_scene(None, None, None, None, None)

        music.play.assert_not_called()


@pytest.mark.asyncio
def test_reading_when_working_does_not_play_music(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.READING, studio_activity=Studio.Activity.WORKING)

    with mock.patch.object(MusicHandler, 'play') as music:
        music.is_playing = lambda *_: False
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.music = music
        scene.handle_scene(None, None, None, None, None)

        music.play.assert_not_called()


@pytest.mark.asyncio
def test_reading_does_not_replace_if_playing(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.READING, playing_music=states.ON)

    with mock.patch.object(MusicHandler, 'play') as music:
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.music = music
        scene.handle_scene(None, None, None, None, None)

        music.play.assert_not_called()


@pytest.mark.asyncio
def test_watching_tv_sets_movie_scene(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.WATCHING_TV, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.LIVING_ROOM_MOVIE.get()).was.turned_on()


@pytest.mark.asyncio
def test_watching_tv_pauses_music(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.WATCHING_TV)

    with mock.patch.object(MusicHandler, 'pause') as music:
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.music = music
        scene.handle_scene(None, None, None, None, None)

        music.pause.assert_called_once()

@pytest.mark.asyncio
def test_watching_tv_closes_blinds_irrespecitively_of_mode(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.WATCHING_TV, mode=modes.Mode.DAY)

    with mock.patch.object(BlindsHandler, 'close') as blinds:
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.blinds = blinds
        scene.handle_scene(None, None, None, None, None)

        blinds.close.assert_called_once()

@pytest.mark.asyncio
def test_drumming_sets_drumming_scene(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.DRUMMING, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.LIVING_ROOM_DRUMMING.get()).was.turned_on()


@pytest.mark.asyncio
def test_drumming_pauses_music(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.DRUMMING)

    with mock.patch.object(MusicHandler, 'pause') as music:
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.music = music
        scene.handle_scene(None, None, None, None, None)

        music.pause.assert_called_once()


@pytest.mark.asyncio
def test_gaming_sets_gaming_scene(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.GAMING, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.LIVING_ROOM_GAMING.get()).was.turned_on()


@pytest.mark.asyncio
def test_gaming_pauses_music(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.GAMING)

    with mock.patch.object(MusicHandler, 'pause') as music:
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.music = music
        scene.handle_scene(None, None, None, None, None)

        music.pause.assert_called_once()


@pytest.mark.asyncio
def test_gaming_closes_blinds(given_that) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.GAMING, mode=modes.Mode.DAY)

    with mock.patch.object(BlindsHandler, 'close') as blinds:
        scene = LivingRoomScene(None, LivingRoomScene.__class__, None, None, None, None, None)
        scene.handlers.blinds = blinds
        scene.handle_scene(None, None, None, None, None)

        blinds.close.assert_called_once()

def living_room_scene_is(self, activity, illuminance=0, are_lights_on=False, mode=modes.Mode.NIGHT,
                         playing_music=states.OFF, studio_activity=Studio.Activity.EMPTY):
    self.state_of(entities.COVER_BLINDS_CURTAIN).is_set_to(states.OPEN)
    self.state_of(entities.MEDIA_PLAYER_COOKING_AREA_2).is_set_to(playing_music)
    self.state_of(helpers.HOMEASSISTANT_MODE).is_set_to(mode)
    self.state_of(entities.SENSOR_AIR_QUALITY_TEMPERATURE).is_set_to(20)
    self.state_of(entities.SENSOR_STUDIO_MS_ILLUMINANCE).is_set_to(illuminance)
    self.state_of(LivingRoom._activity_helper).is_set_to(activity)
    self.state_of(Studio._activity_helper).is_set_to(studio_activity)
    if are_lights_on:
        self.state_of(entities.LIGHT_LIVING_ROOM).is_set_to(states.ON)
    else:
        self.state_of(entities.LIGHT_LIVING_ROOM).is_set_to(states.OFF)


given.GivenThatWrapper.living_room_scene_is = living_room_scene_is
