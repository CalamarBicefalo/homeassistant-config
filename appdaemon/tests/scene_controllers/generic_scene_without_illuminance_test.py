import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import helpers
import matchers
import scenes
import states
from modes import Mode
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler

DEFAULT_SCENE = scenes.KITCHEN_TV
ROOM_LIGHTS = "room_lights"


class GenericSceneWithoutIlluminance(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom
    room_lights = entities.Entity(ROOM_LIGHTS)

    def get_light_scene(self, activity: activities.LivingRoom) -> Scene:
        return DEFAULT_SCENE


@automation_fixture(GenericSceneWithoutIlluminance)
def generic_room_scene() -> None:
    matchers.init()
    pass



@pytest.mark.asyncio
def test_when_present(given_that, generic_room_scene, assert_that):
    given_that.scene_is(generic_room_scene, activity=activities.Common.PRESENT, are_lights_on=False)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(DEFAULT_SCENE.get()).was.turned_on()


def scene_is(self, room_scene, activity, are_lights_on=False, mode=Mode.NIGHT):
    self.state_of(room_scene.activity._helper).is_set_to(activity)
    self.state_of(helpers.HOMEASSISTANT_MODE).is_set_to(mode)
    if are_lights_on:
        self.state_of(ROOM_LIGHTS).is_set_to(states.ON)
    else:
        self.state_of(ROOM_LIGHTS).is_set_to(states.OFF)


given.GivenThatWrapper.scene_is = scene_is
