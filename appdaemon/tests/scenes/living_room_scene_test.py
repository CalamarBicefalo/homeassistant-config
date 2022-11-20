import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import helpers
import matchers
import states
import utils
from scenes.living_room_scene import LivingRoomScene


@automation_fixture(LivingRoomScene)
def living_room_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
async def test_when_reading(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.READING, illuminance=30, are_lights_on=False)

    await living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.SCENE_LIVING_ROOM_READING).was.turned_on()


@pytest.mark.asyncio
async def test_when_watching_tv(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.WATCHING_TV, illuminance=30, are_lights_on=False)

    await living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.SCENE_LIVING_ROOM_MOVIE).was.turned_on()


def living_room_scene_is(self, activity, illuminance, are_lights_on):
    self.state_of(entities.SENSOR_DESK_MS_ILLUMINANCE).is_set_to(utils.awaitable(illuminance))
    self.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(utils.awaitable(activity))
    if are_lights_on:
        self.state_of(entities.LIGHT_LIVING_ROOM).is_set_to(utils.awaitable(states.ON))
    else:
        self.state_of(entities.LIGHT_LIVING_ROOM).is_set_to(utils.awaitable(states.OFF))


given.GivenThatWrapper.living_room_scene_is = living_room_scene_is
