import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import entities
import helpers
import matchers
import utils
from scenes_controller.living_room_scene import LivingRoomScene


@automation_fixture(LivingRoomScene)
def living_room_scene():
    matchers.init()
    pass


def test_set_scene_triggers_when_activity_changes(given_that, living_room_scene, assert_that):
    assert_that(living_room_scene) \
        .listens_to.state(helpers.LIVING_ROOM_ACTIVITY) \
        .with_callback(living_room_scene.set_living_room_scene)


def test_set_scene_triggers_when_illuminance_changes(given_that, living_room_scene, assert_that):
    assert_that(living_room_scene) \
        .listens_to.state(entities.SENSOR_DESK_MS_ILLUMINANCE) \
        .with_callback(living_room_scene.set_living_room_scene)


@pytest.mark.asyncio
async def test_when_empty(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.EMPTY, illuminance=100)

    await living_room_scene.set_living_room_scene(None, None, None, None, None)

    assert_that(entities.LIGHT_LIVING_ROOM).was.turned_off()


@pytest.mark.asyncio
async def test_when_bright(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.PRESENT, illuminance=100)

    await living_room_scene.set_living_room_scene(None, None, None, None, None)

    assert_that(entities.LIGHT_LIVING_ROOM).was.turned_off()

@pytest.mark.asyncio
async def test_when_present(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.PRESENT, illuminance=30)

    await living_room_scene.set_living_room_scene(None, None, None, None, None)

    assert_that(entities.SCENE_LIVING_ROOM_WELCOME).was.turned_on()


@pytest.mark.asyncio
async def test_when_reading(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.READING, illuminance=30)

    await living_room_scene.set_living_room_scene(None, None, None, None, None)

    assert_that(entities.SCENE_LIVING_ROOM_READING).was.turned_on()


@pytest.mark.asyncio
async def test_when_watching_tv(given_that, living_room_scene, assert_that):
    given_that.living_room_scene_is(activity=activities.LivingRoom.WATCHING_TV, illuminance=30)

    await living_room_scene.set_living_room_scene(None, None, None, None, None)

    assert_that(entities.SCENE_LIVING_ROOM_MOVIE).was.turned_on()


def living_room_scene_is(self, activity, illuminance):
    self.state_of(entities.SENSOR_DESK_MS_ILLUMINANCE).is_set_to(utils.awaitable(illuminance))
    self.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(utils.awaitable(activity.value))


given.GivenThatWrapper.living_room_scene_is = living_room_scene_is
