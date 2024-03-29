import pytest
from appdaemontestframework import automation_fixture

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
def test_clean_flat(given_that, app: FlickApp, assert_that):
    app.handlers.flick.clean_flat()

    assert_that(services.VACUUM_START).was.called_with(
        entity_id=entities.VACUUM_FLICK,
    )


@pytest.mark.asyncio
def test_go_to_maintenance(given_that, app: FlickApp, assert_that):
    app.handlers.flick.go_to_maintenance_spot()

    assert_that(services.VACUUM_SEND_COMMAND).was.called_with(
        entity_id=entities.VACUUM_FLICK,
        command="app_goto_target",
        params=[flick.mop_maintenance.x, flick.mop_maintenance.y]
    )
