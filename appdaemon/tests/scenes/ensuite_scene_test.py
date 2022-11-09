import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import helpers
import matchers
import utils
from scenes_controller.ensuite_scene import EnsuiteScene


@automation_fixture(EnsuiteScene)
def ensuite_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
async def test_when_empty(given_that, ensuite_scene, assert_that):
    given_that.ensuite_scene_is(activity=activities.Ensuite.EMPTY, illuminance=100)

    await ensuite_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.LIGHT_BATHROOM).was.turned_off()

@pytest.mark.asyncio
async def test_when_present(given_that, ensuite_scene, assert_that):
    given_that.ensuite_scene_is(activity=activities.Ensuite.PRESENT, illuminance=30)

    await ensuite_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.SCENE_BATHROOM_CONCENTRATE).was.turned_on()

def ensuite_scene_is(self, activity, illuminance):
    self.state_of(entities.SENSOR_DESK_MS_ILLUMINANCE).is_set_to(utils.awaitable(illuminance))
    self.state_of(helpers.ENSUITE_ACTIVITY).is_set_to(utils.awaitable(activity))


given.GivenThatWrapper.ensuite_scene_is = ensuite_scene_is
