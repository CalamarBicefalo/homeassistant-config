from datetime import datetime, time

import pytest
from appdaemontestframework import automation_fixture

import apps.helpers
import utils
from apps import devices, services, helpers, activities
from apps.vacuum_controller import VacuumController


@automation_fixture(VacuumController)
def vacuum_controller():
    pass


def test_clean_mop_maintenance_triggers_while_in_kitchen(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .listens_to.state(helpers.KITCHEN_ACTIVITY, old=activities.AWAY, new=activities.PRESENT) \
        .with_callback(vacuum_controller.clean_kitchen)


@pytest.mark.asyncio
async def test_clean_kitchen_when_clean_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.state_of(apps.helpers.LAST_CLEANED_KITCHEN).is_set_to("2000-01-01 00:00:00")

    await vacuum_controller.start_mop_maintenance(None)

    assert_that(services.VACUUM_GO_TO).was_not.called_with(
        entity_id=devices.VACUUM_CLEANER,
        segments="?????"
    )


@pytest.mark.asyncio
async def test_clean_kitchen_when_dirty_goes_to_maintenance_spot(given_that, vacuum_controller, assert_that):
    given_that.state_of(apps.helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_now())

    await vacuum_controller.start_mop_maintenance(None)

    assert_that(services.VACUUM_GO_TO).was.called_with(
        entity_id=devices.VACUUM_CLEANER,
        segments="?????"
    )
