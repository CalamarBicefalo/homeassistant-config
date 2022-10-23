import pytest, matchers
from appdaemontestframework import automation_fixture

import apps.constants.helpers
import utils
from apps.constants import activities, helpers, services
from apps.vacuum.kitchen_cleaner import KitchenCleaner


@automation_fixture(KitchenCleaner)
def vacuum_controller():
    matchers.init()
    pass


def test_clean_mop_maintenance_triggers_while_in_kitchen(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .listens_to.state(helpers.KITCHEN_ACTIVITY, old=activities.AWAY, new=activities.PRESENT) \
        .with_callback(vacuum_controller.start_mop_maintenance)


@pytest.mark.asyncio
async def test_mop_when_clean_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.state_of(apps.constants.helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_yesterday())
    given_that.state_of(apps.constants.helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.formatted_now())

    await vacuum_controller.start_mop_maintenance()

    assert_that(services.VACUUM_GO_TO).was_not.sent_for_maintenance_to_kitchen()


@pytest.mark.asyncio
async def test_mop_when_dirty_goes_to_maintenance_spot(given_that, vacuum_controller, assert_that):
    given_that.state_of(apps.constants.helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_now())
    given_that.state_of(apps.constants.helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.formatted_yesterday())

    await vacuum_controller.start_mop_maintenance()

    assert_that(services.VACUUM_GO_TO).was.sent_for_maintenance_to_kitchen()


@pytest.mark.asyncio
async def test_mop_when_cleaned_updates_helper(given_that, vacuum_controller, assert_that):
    given_that.state_of(apps.constants.helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_now())
    given_that.state_of(apps.constants.helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(utils.formatted_yesterday())

    await vacuum_controller.start_mop_maintenance()

    assert_that(services.HELPER_DATETIME_SET).was.set_to_now(helpers.LAST_CLEANED_VACUUM_MOP)
