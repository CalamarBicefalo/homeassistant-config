from datetime import datetime

import pytest
from appdaemontestframework import automation_fixture

import activities
import helpers
import matchers
import services
import utils
from vacuum.kitchen_cleaner import KitchenCleaner


@automation_fixture(KitchenCleaner)
def vacuum_controller():
    matchers.init()
    pass


def test_triggers_every_night(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .registered.run_daily("22:30:00") \
        .with_callback(vacuum_controller.clean_kitchen)


def test_triggers_when_away(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .listens_to.state(helpers.KITCHEN_ACTIVITY, new=activities.EMPTY) \
        .with_callback(vacuum_controller.clean_kitchen_if_scheduled)

@pytest.mark.asyncio
async def test_when_didnt_cook_does_not_vacuum(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_COOKED).is_set_to(utils.formatted_yesterday())
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_now())
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.EMPTY)

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_cooked_vacuums(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_COOKED).is_set_to(utils.formatted_now())
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_yesterday())
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.EMPTY)

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_vacuumed_sets_last_cleaned(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_COOKED).is_set_to(utils.formatted_now())
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_yesterday())
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.EMPTY)

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.HELPER_DATETIME_SET).was.set_to_now(helpers.LAST_CLEANED_KITCHEN)


@pytest.mark.asyncio
async def test_when_around_does_not_clean(given_that, vacuum_controller, assert_that, time_travel):
    given_that.state_of(helpers.LAST_COOKED).is_set_to(utils.formatted_now())
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_yesterday())
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.WATCHING_TV)

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_not_scheduled(given_that, vacuum_controller, assert_that, time_travel):
    given_that.state_of(helpers.LAST_COOKED).is_set_to(utils.formatted_now())
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_yesterday())
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.EMPTY)

    await vacuum_controller.clean_kitchen_if_scheduled(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_not_scheduled(given_that, vacuum_controller, assert_that, time_travel):
    given_that.state_of(helpers.LAST_COOKED).is_set_to(utils.formatted_now())
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(utils.formatted_yesterday())
    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.WATCHING_TV)

    await vacuum_controller.clean_kitchen_if_scheduled(None)
    await vacuum_controller.clean_kitchen(None)
    await vacuum_controller.clean_kitchen_if_scheduled(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()

    given_that.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(activities.EMPTY)
    await vacuum_controller.clean_kitchen_if_scheduled(None)
    assert_that(services.VACUUM_CLEAN_SEGMENT).was.sent_to_clean_kitchen()
