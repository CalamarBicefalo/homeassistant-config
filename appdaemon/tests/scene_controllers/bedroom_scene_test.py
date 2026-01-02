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
from scene_controllers.bedroom_scene import BedroomScene


@automation_fixture(BedroomScene)
def bedroom_scene():
    matchers.init()
    pass


@pytest.fixture
def fake_blinds():
    return FakeBlindsHandler()


@pytest.fixture
def fake_music():
    return FakeMusicHandler()


@pytest.fixture(autouse=True)
def setup_fakes(bedroom_scene, fake_blinds, fake_music):
    bedroom_scene.handlers.blinds = fake_blinds
    bedroom_scene.handlers.music = fake_music


@pytest.mark.asyncio
def test_relaxing_sets_relaxing_scene(given_that, bedroom_scene, assert_that):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.RELAXING, illuminance=30, are_lights_on=False)

    bedroom_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.BEDROOM_RELAXING.get()).was.turned_on()


@pytest.mark.asyncio
def test_relaxing_plays_music(given_that, bedroom_scene, fake_music) -> None:
    given_that.bedroom_scene_is(activity=Bedroom.Activity.RELAXING)

    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)

    assert fake_music.is_playing()


@pytest.mark.asyncio
def test_empty_activity_adjusts_blinds(given_that, bedroom_scene, assert_that):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.EMPTY, illuminance=30)

    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)

    assert_that(entities.LIGHT_BEDROOM).was.turned_off()


@pytest.mark.asyncio
def test_mode_change_adjusts_blinds_when_empty(given_that, bedroom_scene, fake_blinds):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.EMPTY, mode=selects.Mode.DAY)

    bedroom_scene.on_mode_change(selects.Mode.NIGHT, selects.Mode.DAY)
    
    assert fake_blinds.get_position() == BEST_FOR_TEMPERATURE


@pytest.mark.asyncio
def test_mode_change_adjusts_blinds_when_away(given_that, bedroom_scene, fake_blinds):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.PRESENT, mode=selects.Mode.DAY)

    bedroom_scene.on_mode_change(selects.Mode.AWAY, selects.Mode.DAY)
    
    assert fake_blinds.get_position() == BEST_FOR_TEMPERATURE


@pytest.mark.asyncio
def test_bedtime_starts_music(given_that, bedroom_scene, fake_music):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.BEDTIME)
    
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)
    
    assert fake_music.is_playing()


@pytest.mark.asyncio
def test_bedtime_closes_blinds(given_that, bedroom_scene, fake_blinds):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.BEDTIME)
    
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)
    
    assert fake_blinds.is_closed()


@pytest.mark.asyncio
def test_present_day_mode_turns_on_bright_scene(given_that, bedroom_scene, assert_that):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.PRESENT, mode=selects.Mode.DAY)
    
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)
    
    assert_that(scenes.BEDROOM_BRIGHT.get()).was.turned_on()


@pytest.mark.asyncio
def test_present_night_mode_turns_on_nightlight(given_that, bedroom_scene, assert_that):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.PRESENT, mode=selects.Mode.NIGHT)
    
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)
    
    assert_that(scenes.BEDROOM_NIGHTLIGHT.get()).was.turned_on()


@pytest.mark.asyncio
def test_present_sleeping_mode_turns_off_lights(given_that, bedroom_scene, assert_that):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.PRESENT, mode=selects.Mode.SLEEPING)
    
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)
    
    assert_that(entities.LIGHT_BEDROOM).was.turned_off()


@pytest.mark.asyncio
def test_mode_change_to_sleeping_turns_off_lights(given_that, bedroom_scene, assert_that):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.PRESENT, mode=selects.Mode.NIGHT)
    
    bedroom_scene.on_mode_change(selects.Mode.SLEEPING, selects.Mode.NIGHT)
    
    assert_that(entities.LIGHT_BEDROOM).was.turned_off()


@pytest.mark.asyncio
def test_mode_change_to_sleeping_starts_rain_sounds(given_that, bedroom_scene, fake_music, time_travel):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.PRESENT, mode=selects.Mode.NIGHT)
    
    bedroom_scene.on_mode_change(selects.Mode.SLEEPING, selects.Mode.NIGHT)
    time_travel.fast_forward(3).seconds()
    
    assert fake_music.is_playing()


def test_waking_up_starts_birds_music(given_that, bedroom_scene, fake_music):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.WAKING_UP, illuminance=30)
    given_that.state_of(entities.SENSOR_LIVING_ROOM_ILLUMINANCE).is_set_to(30)
    
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)
    
    assert fake_music.is_playing()
    assert fake_music.get_volume() == 0.2


def test_waking_up_plays_radio_after_completion(given_that, bedroom_scene, fake_music, time_travel):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.WAKING_UP, illuminance=30)
    given_that.state_of(entities.SENSOR_LIVING_ROOM_ILLUMINANCE).is_set_to(30)
    
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)
    time_travel.fast_forward(bedroom_scene.wakeup_duration_minutes).minutes()
    time_travel.fast_forward(61).seconds()
    
    assert fake_music.is_playing()
    assert fake_music.get_volume() == 0.3


def test_music_stops_when_bedroom_empty_after_waking(given_that, bedroom_scene, fake_music):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.WAKING_UP, illuminance=30, mode=selects.Mode.SLEEPING)
    given_that.state_of(entities.SENSOR_LIVING_ROOM_ILLUMINANCE).is_set_to(30)
    
    bedroom_scene.mode_controller(None, None, selects.Mode.SLEEPING, selects.Mode.DAY, None)
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, None, None, None)
    
    assert fake_music.is_playing()
    
    given_that.bedroom_scene_is(activity=Bedroom.Activity.EMPTY, illuminance=30, mode=selects.Mode.DAY)
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, Bedroom.Activity.WAKING_UP, None, None)
    
    assert not fake_music.is_playing()


def test_present_day_mode_does_not_adjust_blinds_when_just_woke_up_and_open(given_that, bedroom_scene, fake_blinds):
    given_that.bedroom_scene_is(activity=Bedroom.Activity.EMPTY, illuminance=100, mode=selects.Mode.SLEEPING)
    fake_blinds.open()
    
    bedroom_scene.mode_controller(None, None, selects.Mode.SLEEPING, selects.Mode.DAY, None)
    assert bedroom_scene.just_woke_up
    assert fake_blinds.get_position() == 100.0
    
    given_that.bedroom_scene_is(activity=Bedroom.Activity.PRESENT, illuminance=100, mode=selects.Mode.DAY)
    bedroom_scene.handle_scene(Bedroom._activity_helper, None, Bedroom.Activity.EMPTY, None, None)
    
    assert fake_blinds.get_position() == 100.0


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
