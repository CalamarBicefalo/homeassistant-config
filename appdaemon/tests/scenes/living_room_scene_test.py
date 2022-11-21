import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import matchers
import states
from scenes.living_room_scene import LivingRoomScene


@automation_fixture(LivingRoomScene)
def living_room_scene():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_reading(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.READING, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.SCENE_LIVING_ROOM_READING).was.turned_on()


@pytest.mark.asyncio
def test_when_watching_tv(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.WATCHING_TV, illuminance=30, are_lights_on=False)

    living_room_scene.handle_scene(None, None, None, None, None)

    assert_that(entities.SCENE_LIVING_ROOM_MOVIE).was.turned_on()


def living_room_scene_is(self, activity, illuminance, are_lights_on):
    self.state_of(entities.SENSOR_DESK_MS_ILLUMINANCE).is_set_to((illuminance))
    self.state_of(activities.LivingRoom.helper).is_set_to((activity))
    if are_lights_on:
        self.state_of(entities.LIGHT_LIVING_ROOM).is_set_to((states.ON))
    else:
        self.state_of(entities.LIGHT_LIVING_ROOM).is_set_to((states.OFF))


given.GivenThatWrapper.living_room_scene_is = living_room_scene_is
