import pytest
from appdaemontestframework import automation_fixture, given_that as given, assert_that as assertt

import entities
import flick
import matchers
import rooms
import services
from app import App


class FlickApp(App):
    def initialize(self) -> None:
        pass


@automation_fixture(FlickApp)
def app() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_clean_room(given_that, app: FlickApp, assert_that):
    app.handlers.rooms.kitchen.clean()

    assert_that(services.VACUUM_SEND_COMMAND).was.called_with(
        entity_id=entities.VACUUM_FLICK,
        command="app_segment_clean",
        params=rooms.Kitchen._room_cleaner_segment
    )



@pytest.mark.asyncio
def test_clean_flat_sends_flick_to_clean(given_that, app: FlickApp, assert_that):
    given_that.flick_state_is()

    app.handlers.flick.clean_flat()

    assert_that(services.VACUUM_START).was.called_with(
        entity_id=entities.VACUUM_FLICK,
    )

@pytest.mark.asyncio
def test_clean_flat_updates_room_cleaned_count(given_that, app: FlickApp, assert_that):
    given_that.flick_state_is(rooms_cleaned_since_maintenance=3)

    app.handlers.flick.clean_flat()

    assert_that(services.INPUT_NUMBER_SET_VALUE).was.called_with(
        entity_id=entities.INPUT_NUMBER_ROOMS_CLEANED_SINCE_LAST_MAINTENANCE,
        value=13
    )


@pytest.mark.asyncio
def test_clean_room_updates_room_cleaned_count(given_that, app: FlickApp, assert_that):
    given_that.flick_state_is()

    app.handlers.flick.clean_room(0)

    assert_that(services.INPUT_NUMBER_INCREMENT).was.called_with(
        entity_id=entities.INPUT_NUMBER_ROOMS_CLEANED_SINCE_LAST_MAINTENANCE
    )


@pytest.mark.asyncio
def test_go_to_maintenance(given_that, app: FlickApp, assert_that):
    given_that.flick_state_is()

    app.handlers.flick.go_to_maintenance_spot()

    assert_that(services.VACUUM_SEND_COMMAND).was.called_with(
        entity_id=entities.VACUUM_FLICK,
        command="app_goto_target",
        params=[flick.mop_maintenance.x, flick.mop_maintenance.y]
    )

def flick_state_is(self, rooms_cleaned_since_maintenance=0):
    self.state_of(entities.INPUT_NUMBER_ROOMS_CLEANED_SINCE_LAST_MAINTENANCE).is_set_to(rooms_cleaned_since_maintenance)


given.GivenThatWrapper.flick_state_is = flick_state_is
del flick_state_is  # clean up namespace