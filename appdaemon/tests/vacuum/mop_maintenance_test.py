import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import helpers
import services
import utils
from vacuum.mop_maintenance import MopMaintenance


@automation_fixture(MopMaintenance)
def vacuum_controller():
    matchers.init()
    pass


def test_clean_mop_maintenance_triggers_while_in_kitchen(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .listens_to.state(helpers.KITCHEN_ACTIVITY, old=activities.EMPTY, new=activities.PRESENT) \
        .with_callback(vacuum_controller.start_mop_maintenance)


@pytest.mark.asyncio
async def test_mop_when_clean_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.awaitable(utils.formatted_yesterday()))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.awaitable(utils.formatted_now()))

    await vacuum_controller.start_mop_maintenance()

    assert_that(services.VACUUM_GO_TO).was_not.sent_for_maintenance_to_kitchen()


@pytest.mark.asyncio
async def test_mop_when_dirty_goes_to_maintenance_spot(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.awaitable(utils.formatted_now()))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.awaitable(utils.formatted_yesterday()))

    await vacuum_controller.start_mop_maintenance()

    assert_that(services.VACUUM_GO_TO).was.sent_for_maintenance_to_kitchen()


@pytest.mark.asyncio
async def test_mop_when_cleaned_updates_helper(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.awaitable(utils.formatted_now()))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.awaitable(utils.formatted_yesterday()))

    await vacuum_controller.start_mop_maintenance()

    assert_that(services.HELPER_DATETIME_SET).was.set_to_now(helpers.LAST_CLEANED_VACUUM_MOP)
