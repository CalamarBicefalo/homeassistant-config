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
from scene_controllers.living_room_scene import LivingRoomScene


@automation_fixture(LivingRoomScene)
def living_room_scene():
    matchers.init()
    pass


@pytest.fixture
def fake_blinds():
    return FakeBlindsHandler()


@pytest.fixture
def fake_music():
    return FakeMusicHandler()


@pytest.fixture(autouse=True)
def setup_fakes(living_room_scene, fake_blinds, fake_music):
    living_room_scene.handlers.blinds = fake_blinds
    living_room_scene.handlers.music = fake_music


@pytest.mark.asyncio
def test_relaxing_sets_cozy_scene(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.RELAXING, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.LIVING_ROOM_COZY.get()).was.turned_on()


@pytest.mark.asyncio
def test_relaxing_plays_music(given_that, living_room_scene, fake_music) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.RELAXING)

    living_room_scene.handle_scene(LivingRoom._activity_helper, None, None, None, None)

    assert fake_music.is_playing()


@pytest.mark.asyncio
def test_relaxing_when_music_playing_does_not_play_music(given_that, living_room_scene, fake_music) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.RELAXING)
    fake_music.play()  # Given: music is already playing

    living_room_scene.handle_scene(None, None, None, None, None)

    assert fake_music.is_playing()  # Still playing, no change


@pytest.mark.asyncio
def test_relaxing_when_working_does_not_play_music(given_that, living_room_scene, fake_music) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.RELAXING, studio_activity=Studio.Activity.WORKING)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert not fake_music.is_playing()  # Music not started


@pytest.mark.asyncio
def test_relaxing_does_not_replace_if_playing(given_that, living_room_scene, fake_music) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.RELAXING, playing_music=states.ON)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert not fake_music.is_playing()  # Music not started


@pytest.mark.asyncio
def test_watching_tv_sets_movie_scene(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.WATCHING_TV, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.LIVING_ROOM_MOVIE.get()).was.turned_on()


@pytest.mark.asyncio
def test_watching_tv_pauses_music(given_that, living_room_scene, fake_music) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.WATCHING_TV)

    living_room_scene.handle_scene(LivingRoom._activity_helper, None, None, None, None)

    assert not fake_music.is_playing()

@pytest.mark.asyncio
def test_watching_tv_closes_blinds_irrespecitively_of_mode(given_that, living_room_scene, fake_blinds) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.WATCHING_TV, mode=selects.Mode.DAY)

    living_room_scene.handle_scene(LivingRoom._activity_helper, None, None, None, None)

    assert fake_blinds.is_closed()

@pytest.mark.asyncio
def test_drumming_sets_drumming_scene(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.DRUMMING, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.LIVING_ROOM_DRUMMING.get()).was.turned_on()


@pytest.mark.asyncio
def test_drumming_pauses_music(given_that, living_room_scene, fake_music) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.DRUMMING)

    living_room_scene.handle_scene(LivingRoom._activity_helper, None, None, None, None)

    assert not fake_music.is_playing()


@pytest.mark.asyncio
def test_gaming_sets_gaming_scene(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.GAMING, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.LIVING_ROOM_GAMING.get()).was.turned_on()


@pytest.mark.asyncio
def test_gaming_pauses_music(given_that, living_room_scene, fake_music) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.GAMING)

    living_room_scene.handle_scene(LivingRoom._activity_helper, None, None, None, None)

    assert not fake_music.is_playing()


@pytest.mark.asyncio
def test_gaming_closes_blinds(given_that, living_room_scene, fake_blinds) -> None:
    given_that.living_room_scene_is(activity=LivingRoom.Activity.GAMING, mode=selects.Mode.DAY)

    living_room_scene.handle_scene(LivingRoom._activity_helper, None, None, None, None)

    assert fake_blinds.is_closed()


@pytest.mark.asyncio
def test_empty_activity_turns_off_lights(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.EMPTY, illuminance=30)

    living_room_scene.handle_scene(LivingRoom._activity_helper, None, None, None, None)

    assert_that(entities.LIGHT_LIVING_ROOM).was.turned_off()


@pytest.mark.asyncio
def test_mode_change_adjusts_blinds(given_that, living_room_scene, fake_blinds):
    given_that.living_room_scene_is(activity=LivingRoom.Activity.EMPTY, mode=selects.Mode.DAY)

    living_room_scene.on_mode_change(selects.Mode.NIGHT, selects.Mode.DAY)
    
    assert fake_blinds.get_position() == BEST_FOR_TEMPERATURE


def living_room_scene_is(self, activity, illuminance=0, are_lights_on=False, mode=selects.Mode.NIGHT,
                         playing_music=states.OFF, studio_activity=Studio.Activity.EMPTY):
    self.state_of(entities.COVER_LIVING_ROOM_BLINDS).is_set_to(states.OPEN)
    self.state_of(entities.MEDIA_PLAYER_LIVING_ROOM_STEREO).is_set_to(playing_music)
    self.state_of(helpers.MODE).is_set_to(mode)
    self.state_of(entities.SENSOR_BEDROOM_AIR_QUALITY_TEMPERATURE).is_set_to(20)
    self.state_of(entities.SENSOR_MS_STUDIO_EP1_ILLUMINANCE).is_set_to(illuminance)
    self.state_of(LivingRoom._activity_helper).is_set_to(activity)
    self.state_of(Studio._activity_helper).is_set_to(studio_activity)
    if are_lights_on:
        self.state_of(entities.LIGHT_LIVING_ROOM).is_set_to(states.ON)
    else:
        self.state_of(entities.LIGHT_LIVING_ROOM).is_set_to(states.OFF)


given.GivenThatWrapper.living_room_scene_is = living_room_scene_is
