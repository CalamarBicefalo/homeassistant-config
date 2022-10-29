from datetime import datetime, timedelta

import pytest
from appdaemontestframework import automation_fixture, given_that as given

import activities
import helpers
import matchers
import services
from utils import formatted_yesterday as yesterday, formatted_now as now, formatted_days_ago as days_ago, format_date, \
    awaitable
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
        .listens_to.state(helpers.KITCHEN_ACTIVITY, new=activities.Kitchen.EMPTY) \
        .with_callback(vacuum_controller.clean_kitchen)


@pytest.mark.asyncio
async def test_when_didnt_cook_does_not_vacuum(given_that, vacuum_controller, assert_that):
    given_that.state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=days_ago(3)
    )

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_cooked_vacuums(given_that, vacuum_controller, assert_that):
    given_that.state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_vacuumed_updates_last_cleaned(given_that, vacuum_controller, assert_that):
    given_that.state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.HELPER_DATETIME_SET).was.set_to_now(helpers.LAST_CLEANED_KITCHEN)


@pytest.mark.asyncio
async def test_when_around_does_not_clean(given_that, vacuum_controller, assert_that, time_travel):
    given_that.state_is(
        activity=activities.LivingRoom.WATCHING_TV,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_less_than_20_hours_since_last_clean_does_not_clean(given_that, vacuum_controller, assert_that,
                                                                       time_travel):
    given_that.state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=format_date((datetime.now() - timedelta(hours=19))),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
async def test_when_more_than_20_hours_since_last_clean_cleans(given_that, vacuum_controller, assert_that, time_travel):
    given_that.state_is(
        activity=activities.LivingRoom.EMPTY,
        last_cleaned=format_date((datetime.now() - timedelta(hours=21))),
        last_cooked=now()
    )

    await vacuum_controller.clean_kitchen(None)

    assert_that(services.VACUUM_CLEAN_SEGMENT).was.sent_to_clean_kitchen()


def state_is(self, activity, last_cleaned, last_cooked):
    self.state_of(helpers.LAST_COOKED).is_set_to(awaitable(last_cooked))
    self.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(awaitable(last_cleaned))
    self.state_of(helpers.LIVING_ROOM_ACTIVITY).is_set_to(awaitable(activity.value))


given.GivenThatWrapper.state_is = state_is
