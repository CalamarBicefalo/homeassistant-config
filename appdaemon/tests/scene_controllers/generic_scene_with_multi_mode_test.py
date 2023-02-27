import pytest
from appdaemontestframework import automation_fixture

import activities
import entities
import helpers
import matchers
import scenes
import states
from modes import Mode
from scene_controllers import scene
from scene_controllers.scene import SceneSelector
from scene_controllers.scene_app import SceneApp
from handlers.select_handler import SelectHandler

ROOM_LIGHTS = "room_lights"
ILLUMINANCE_SENSOR = "illuminance_sensor"


class GenericSceneWithIlluminance(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom
    illuminance_sensor = None
    room_lights = entities.Entity(ROOM_LIGHTS)

    def get_light_scene(self, activity: activities.Activity) -> SceneSelector:
        return scene.by_mode({
            Mode.DAY: scenes.BEDROOM_BRIGHT,
            Mode.SLEEPING: scene.off(),
        })


@automation_fixture(GenericSceneWithIlluminance)
def generic_room_scene() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_defined_sets_scene(given_that, generic_room_scene, assert_that):
    initial_state(given_that, generic_room_scene, mode=Mode.DAY)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.BEDROOM_BRIGHT.get()).was.turned_on()


@pytest.mark.asyncio
def test_when_off_turns_off_lights(given_that, generic_room_scene, assert_that):
    initial_state(given_that, generic_room_scene, mode=Mode.SLEEPING)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(ROOM_LIGHTS).was.turned_off()


@pytest.mark.asyncio
def test_when_undefined_ignores_lights_and_scene(given_that, generic_room_scene, assert_that):
    initial_state(given_that, generic_room_scene, mode=Mode.NIGHT)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.BEDROOM_BRIGHT.get()).was_not.turned_on()
    assert_that(ROOM_LIGHTS).was_not.turned_off()


@pytest.mark.asyncio
def test_when_undefined_away_turns_lights_off(given_that, generic_room_scene, assert_that):
    initial_state(given_that, generic_room_scene, mode=Mode.AWAY)

    generic_room_scene.handle_scene(None, None, None, None, None)

    assert_that(scenes.BEDROOM_BRIGHT.get()).was_not.turned_on()
    assert_that(ROOM_LIGHTS).was.turned_off()


def initial_state(self, generic_room_scene, mode=Mode.NIGHT):
    self.state_of(helpers.HOMEASSISTANT_MODE).is_set_to(mode)
    self.state_of(ILLUMINANCE_SENSOR).is_set_to(0)
    self.state_of(generic_room_scene.activity._helper).is_set_to(activities.Common.PRESENT)
    self.state_of(ROOM_LIGHTS).is_set_to(states.OFF)
