import pytest
from appdaemontestframework import automation_fixture

from rooms import *
import entities
import helpers
import matchers
import scenes
import states
from selects import Mode
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler

DEFAULT_SCENE = scenes.KITCHEN_TV
ROOM_LIGHTS = "room_lights"
ILLUMINANCE_SENSOR = "illuminance_sensor"


class GenericSceneWithIlluminance(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.bedroom.activity
    illuminance_sensor = entities.Entity(ILLUMINANCE_SENSOR)
    room_lights = entities.Entity(ROOM_LIGHTS)

    def get_light_scene(self, activity: LivingRoom.Activity) -> Scene:
        return scene.off()


@automation_fixture(GenericSceneWithIlluminance)
def generic_room_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_present(given_that, generic_room_scene, assert_that):
    initial_state(given_that, generic_room_scene, activity=CommonActivities.PRESENT, illuminance=30, are_lights_on=False)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(ROOM_LIGHTS).was.turned_off()


def initial_state(self, generic_room_scene, activity, illuminance=0, are_lights_on=False, mode=Mode.NIGHT):
    self.state_of(helpers.MODE).is_set_to(mode)
    self.state_of(ILLUMINANCE_SENSOR).is_set_to(illuminance)
    self.state_of(generic_room_scene.activity._helper).is_set_to(activity)
    if are_lights_on:
        self.state_of(ROOM_LIGHTS).is_set_to(states.ON)
    else:
        self.state_of(ROOM_LIGHTS).is_set_to(states.OFF)


