import pytest
from appdaemontestframework import automation_fixture, given_that as given

from fakes.music_handler_fake import FakeMusicHandler
from rooms import *
import entities
import helpers
import matchers
import selects
import scenes
import states
from scene_controllers.kitchen_scene import KitchenScene


@automation_fixture(KitchenScene)
def kitchen_scene():
    matchers.init()
    pass


@pytest.fixture
def fake_music():
    return FakeMusicHandler()


@pytest.fixture(autouse=True)
def setup_fakes(kitchen_scene, fake_music):
    kitchen_scene.handlers.music = fake_music


def test_morning_arrival_plays_radio_after_waking(given_that, kitchen_scene, fake_music):
    given_that.kitchen_scene_is(activity=Kitchen.Activity.EMPTY, mode=selects.Mode.SLEEPING)
    
    kitchen_scene.mode_controller(None, None, selects.Mode.SLEEPING, selects.Mode.DAY, None)
    given_that.kitchen_scene_is(activity=Kitchen.Activity.PRESENT, mode=selects.Mode.DAY)
    
    kitchen_scene.handle_scene(Kitchen._activity_helper, None, Kitchen.Activity.EMPTY, None, None)
    
    assert fake_music.is_playing()
    assert fake_music.get_volume() == 0.3


def test_arrival_without_sleeping_does_not_play_radio(given_that, kitchen_scene, fake_music):
    given_that.kitchen_scene_is(activity=Kitchen.Activity.EMPTY, mode=selects.Mode.DAY)
    given_that.kitchen_scene_is(activity=Kitchen.Activity.PRESENT, mode=selects.Mode.DAY)
    
    kitchen_scene.handle_scene(Kitchen._activity_helper, None, Kitchen.Activity.EMPTY, None, None)
    
    assert not fake_music.is_playing()


def test_morning_radio_only_plays_once(given_that, kitchen_scene, fake_music, time_travel):
    given_that.kitchen_scene_is(activity=Kitchen.Activity.EMPTY, mode=selects.Mode.SLEEPING)
    
    kitchen_scene.mode_controller(None, None, selects.Mode.SLEEPING, selects.Mode.DAY, None)
    given_that.kitchen_scene_is(activity=Kitchen.Activity.PRESENT, mode=selects.Mode.DAY)
    
    kitchen_scene.handle_scene(Kitchen._activity_helper, None, Kitchen.Activity.EMPTY, None, None)
    
    assert fake_music.is_playing()
    
    time_travel.fast_forward(121).seconds()
    
    fake_music.pause()
    given_that.kitchen_scene_is(activity=Kitchen.Activity.EMPTY, mode=selects.Mode.DAY)
    given_that.kitchen_scene_is(activity=Kitchen.Activity.PRESENT, mode=selects.Mode.DAY)
    
    kitchen_scene.handle_scene(Kitchen._activity_helper, None, Kitchen.Activity.EMPTY, None, None)
    
    assert not fake_music.is_playing()


def kitchen_scene_is(self, activity, illuminance=50, mode=selects.Mode.DAY):
    self.state_of(entities.SENSOR_KITCHEN_MS_ILLUMINANCE).is_set_to(illuminance)
    self.state_of(Kitchen._activity_helper).is_set_to(activity)
    self.state_of(helpers.MODE).is_set_to(mode)
    self.state_of(entities.LIGHT_KITCHEN).is_set_to(states.OFF)
    self.state_of(entities.MEDIA_PLAYER_LIVING_ROOM_STEREO).is_set_to(states.OFF)


given.GivenThatWrapper.kitchen_scene_is = kitchen_scene_is
