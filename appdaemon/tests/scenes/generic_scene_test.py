import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import matchers
from utils import states
import utils
from scenes.scene_app import SceneApp

DEFAULT_SCENE = "default_scene"
ROOM_LIGHTS = "room_lights"
ILLUMINANCE_SENSOR = "illuminance_sensor"
ACTIVITY = activities.RoomActivity


class GenericSceneWithIlluminance(SceneApp):
    activity = ACTIVITY
    illuminance_sensor = ILLUMINANCE_SENSOR
    room_lights = ROOM_LIGHTS

    def get_light_scene(self, activity: activities.LivingRoom):
        return DEFAULT_SCENE


@automation_fixture(GenericSceneWithIlluminance)
def generic_room_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_empty(given_that, generic_room_scene, assert_that):
    given_that.generic_scene_is(activity=activities.RoomActivity.EMPTY, illuminance=100, are_lights_on=False)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(ROOM_LIGHTS).was.turned_off()


@pytest.mark.asyncio
def test_when_bright(given_that, generic_room_scene, assert_that):
    given_that.generic_scene_is(activity=activities.RoomActivity.PRESENT, illuminance=100, are_lights_on=False)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(ROOM_LIGHTS).was.turned_off()


@pytest.mark.asyncio
def test_when_bright_because_of_light(given_that, generic_room_scene, assert_that):
    given_that.generic_scene_is(activity=activities.RoomActivity.PRESENT, illuminance=100, are_lights_on=True)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(ROOM_LIGHTS).was_not.turned_off()


@pytest.mark.asyncio
def test_when_present(given_that, generic_room_scene, assert_that):
    given_that.generic_scene_is(activity=activities.RoomActivity.PRESENT, illuminance=30, are_lights_on=False)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(DEFAULT_SCENE).was.turned_on()


def generic_scene_is(self, activity, illuminance, are_lights_on):
    self.state_of(ILLUMINANCE_SENSOR).is_set_to((illuminance))
    self.state_of(ACTIVITY.helper).is_set_to((activity))
    if are_lights_on:
        self.state_of(ROOM_LIGHTS).is_set_to((states.ON))
    else:
        self.state_of(ROOM_LIGHTS).is_set_to((states.OFF))


given.GivenThatWrapper.generic_scene_is = generic_scene_is
