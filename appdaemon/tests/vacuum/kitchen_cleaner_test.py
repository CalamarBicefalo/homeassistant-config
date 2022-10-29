from datetime import datetime, timedelta

import pytest
from appdaemontestframework import automation_fixture, given_that as given,assert_that as assertt

import activities
import entities
import helpers
import matchers
import services
from utils import formatted_yesterday as yesterday, formatted_now as now, formatted_days_ago as days_ago, format_date, \
    awaitable
from vacuum.kitchen_cleaner import KitchenCleaner, kitchen_segment


@automation_fixture(KitchenCleaner)
def vacuum_controller():
    matchers.init()
    pass


def test_triggers_every_night(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .registered.run_daily("22:30:00") \
        .with_callback(vacuum_controller.clean_kitchen_daily)


def test_triggers_when_away(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .listens_to.state(helpers.LIVING_ROOM_ACTIVITY, new=activities.LivingRoom.EMPTY.value) \
        .with_callback(vacuum_controller.clean_kitchen)


@pytest.mark.asyncio
async def test_when_didnt_cook_does_not_vacuum(given_that, vacuum_controller, assert_that):
    given_that.kitchen_cleaning_state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=days_ago(3)
    )

    await vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.XIAOMI_MIIO_VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_cooked_vacuums(given_that, vacuum_controller, assert_that):
    given_that.kitchen_cleaning_state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.XIAOMI_MIIO_VACUUM_CLEAN_SEGMENT).was.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_vacuumed_updates_last_cleaned(given_that, vacuum_controller, assert_that):
    given_that.kitchen_cleaning_state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.INPUT_DATETIME_SET_DATETIME).was.set_to_now(helpers.LAST_CLEANED_KITCHEN)


@pytest.mark.asyncio
async def test_when_around_does_not_clean(given_that, vacuum_controller, assert_that, time_travel):
    given_that.kitchen_cleaning_state_is(
        activity=activities.LivingRoom.WATCHING_TV,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.XIAOMI_MIIO_VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_less_than_20_hours_since_last_clean_does_not_clean(given_that, vacuum_controller, assert_that,
                                                                       time_travel):
    given_that.kitchen_cleaning_state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=format_date((datetime.now() - timedelta(hours=19))),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.XIAOMI_MIIO_VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_more_than_20_hours_since_last_clean_cleans(given_that, vacuum_controller, assert_that, time_travel):
    given_that.kitchen_cleaning_state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=format_date((datetime.now() - timedelta(hours=21))),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.XIAOMI_MIIO_VACUUM_CLEAN_SEGMENT).was.sent_to_clean_kitchen()


def kitchen_cleaning_state_is(self, activity, last_cleaned, last_cooked):
    self.state_of(helpers.LAST_COOKED).is_set_to(awaitable(last_cooked))
    self.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(awaitable(last_cleaned))
    self.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(awaitable(activity.value))


given.GivenThatWrapper.kitchen_cleaning_state_is = kitchen_cleaning_state_is

def sent_to_clean_kitchen(self):
    self.called_with(
        entity_id=entities.VACUUM_ROBOROCK_VACUUM_A15,
        segments=kitchen_segment
    )

assertt.Was.sent_to_clean_kitchen = sent_to_clean_kitchen
del sent_to_clean_kitchen  # clean up namespace
