import entities
import matchers
import pytest
from appdaemontestframework import automation_fixture, assert_that as assertt

import activities
import helpers
import services
import utils
from vacuum.mop_maintenance import MopMaintenance, mop_maintenance


@automation_fixture(MopMaintenance)
def vacuum_controller():
    matchers.init()
    pass


def test_clean_mop_maintenance_triggers_while_in_kitchen(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .listens_to.state(helpers.KITCHEN_ACTIVITY,
                          old=activities.Kitchen.EMPTY.value,
                          new=activities.Kitchen.PRESENT.value) \
        .with_callback(vacuum_controller.start_mop_maintenance)


@pytest.mark.asyncio
async def test_mop_when_clean_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.awaitable(utils.formatted_yesterday()))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.awaitable(utils.formatted_now()))

    await vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.XIAOMI_MIIO_VACUUM_GOTO).was_not.sent_for_maintenance_to_kitchen()

@pytest.mark.asyncio
async def test_mop_when_just_cleaned_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.awaitable(utils.formatted_minutes_ago(15)))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.awaitable(utils.formatted_yesterday()))

    await vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.XIAOMI_MIIO_VACUUM_GOTO).was_not.sent_for_maintenance_to_kitchen()


@pytest.mark.asyncio
async def test_mop_when_dirty_goes_to_maintenance_spot(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.awaitable(utils.formatted_minutes_ago(60)))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.awaitable(utils.formatted_yesterday()))

    await vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.XIAOMI_MIIO_VACUUM_GOTO).was.sent_for_maintenance_to_kitchen()


@pytest.mark.asyncio
async def test_mop_when_cleaned_updates_helper(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.awaitable(utils.formatted_minutes_ago(60)))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.awaitable(utils.formatted_yesterday()))

    await vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.INPUT_DATETIME_SET_DATETIME).was.set_to_now(helpers.LAST_CLEANED_VACUUM_MOP)


def sent_for_maintenance_to_kitchen(self):
    self.called_with(
        entity_id=entities.VACUUM_ROBOROCK_VACUUM_A15,
        x_coord=mop_maintenance.x,
        y_coord=mop_maintenance.y
    )


assertt.Was.sent_for_maintenance_to_kitchen = sent_for_maintenance_to_kitchen
del sent_for_maintenance_to_kitchen
