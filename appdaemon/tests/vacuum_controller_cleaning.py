from datetime import datetime

import pytest
from appdaemontestframework import automation_fixture

import apps.helpers
from apps import devices, services, helpers, activities
from apps.vacuum_controller import VacuumController
from utils import formatted_now


@automation_fixture(VacuumController)
def vacuum_controller():
    pass


def test_clean_kitchen_triggers_every_night(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .registered.run_daily("22:30:00") \
        .with_callback(vacuum_controller.clean_kitchen)


@pytest.mark.asyncio
async def test_clean_kitchen_when_didnt_cook_does_not_vacuum(given_that, vacuum_controller, assert_that):
    given_that.state_of(apps.helpers.LAST_COOKED).is_set_to("2000-01-01 00:00:00")
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.AWAY)

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.called_with(
        entity_id=devices.VACUUM_CLEANER,
        segments=16
    )


@pytest.mark.asyncio
async def test_clean_kitchen_when_cooked_vacuums(given_that, vacuum_controller, assert_that):
    given_that.state_of(apps.helpers.LAST_COOKED).is_set_to(formatted_now())
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.AWAY)

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was.called_with(
        entity_id=devices.VACUUM_CLEANER,
        segments=16
    )


@pytest.mark.asyncio
@pytest.mark.skip(reason="not quite getting time_travel to work here")
async def test_clean_kitchen_when_TV_on_waits(given_that, vacuum_controller, assert_that, time_travel):
    given_that.state_of(apps.helpers.LAST_COOKED).is_set_to(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.WATCHING_TV)

    time_travel.fast_forward(140).minutes()
    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.called_with(
        entity_id=devices.VACUUM_CLEANER,
        segments=16
    )


