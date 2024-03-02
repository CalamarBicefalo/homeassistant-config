import pytest
from appdaemontestframework import automation_fixture

from rooms import *
import entities
import helpers
import matchers
import scene_controllers.scene
import states
from selects import Mode
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler

DEFAULT_SCENE = entities.SCENE_KITCHEN_TV
ROOM_LIGHTS = "room_lights"
ILLUMINANCE_SENSOR = "illuminance_sensor"


class GenericSceneWithIlluminance(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.living_room.activity
    illuminance_sensor = entities.Entity(ILLUMINANCE_SENSOR)
    room_lights = entities.Entity(ROOM_LIGHTS)

    def get_light_scene(self, activity: LivingRoom.Activity) -> Scene:
        return scene_controllers.scene.from_entity(DEFAULT_SCENE)


@automation_fixture(GenericSceneWithIlluminance)
def generic_room_scene() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_bright_not_night_then_lights_off(given_that, generic_room_scene, assert_that):
    initial_state(given_that, activity=CommonActivities.PRESENT, illuminance=100, are_lights_on=False)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(ROOM_LIGHTS).was.turned_off()

@pytest.mark.asyncio
def test_when_bright_at_night_then_lights_on(given_that, generic_room_scene, assert_that):
    initial_state(given_that, activity=CommonActivities.PRESENT, mode=Mode.NIGHT, illuminance=500)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(DEFAULT_SCENE).was.turned_on()


@pytest.mark.asyncio
def test_when_bright_because_of_light_then_lights_on(given_that, generic_room_scene, assert_that):
    initial_state(given_that, activity=CommonActivities.PRESENT, are_lights_on=True)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(ROOM_LIGHTS).was_not.turned_off()


def initial_state(self, activity, illuminance=0, are_lights_on=False, mode=Mode.DAY):
    self.state_of(helpers.MODE).is_set_to(mode)
    self.state_of(ILLUMINANCE_SENSOR).is_set_to(illuminance)
    self.state_of(LivingRoom._activity_helper).is_set_to(activity)
    if are_lights_on:
        self.state_of(ROOM_LIGHTS).is_set_to(states.ON)
    else:
        self.state_of(ROOM_LIGHTS).is_set_to(states.OFF)
