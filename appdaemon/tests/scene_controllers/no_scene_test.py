import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import helpers
import matchers
import scenes
import states
from modes import Mode
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp

DEFAULT_SCENE = scenes.KITCHEN_TV
ROOM_LIGHTS = "room_lights"
ILLUMINANCE_SENSOR = "illuminance_sensor"
ACTIVITY = activities.RoomActivity


class GenericSceneWithIlluminance(SceneApp):
    activity = ACTIVITY
    illuminance_sensor = entities.Entity(ILLUMINANCE_SENSOR)
    room_lights = entities.Entity(ROOM_LIGHTS)

    def get_light_scene(self, activity: activities.LivingRoom) -> Scene:
        return scene.off()


@automation_fixture(GenericSceneWithIlluminance)
def generic_room_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_present(given_that, generic_room_scene, assert_that):
    initial_state(given_that, activity=activities.RoomActivity.PRESENT, illuminance=30, are_lights_on=False)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(ROOM_LIGHTS).was.turned_off()


def initial_state(self, activity, illuminance=0, are_lights_on=False, mode=Mode.NIGHT):
    self.state_of(helpers.HOMEASSISTANT_MODE).is_set_to(mode)
    self.state_of(ILLUMINANCE_SENSOR).is_set_to(illuminance)
    self.state_of(ACTIVITY.helper).is_set_to(activity)
    if are_lights_on:
        self.state_of(ROOM_LIGHTS).is_set_to(states.ON)
    else:
        self.state_of(ROOM_LIGHTS).is_set_to(states.OFF)


