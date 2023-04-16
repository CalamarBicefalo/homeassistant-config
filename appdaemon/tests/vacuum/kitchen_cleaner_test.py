from datetime import datetime, timedelta

import pytest
from appdaemontestframework import automation_fixture, given_that as given, assert_that as assertt
from freezegun import freeze_time

import activities
import entities
import flick
import helpers
import matchers
import services
from test_utils import formatted_yesterday as yesterday, formatted_now as now, formatted_days_ago as days_ago, \
    format_date
from vacuum.kitchen_cleaner import KitchenCleaner


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
        .listens_to.state(vacuum_controller.activities.livingroom._helper, new=activities.LivingRoom.EMPTY) \
        .with_callback(vacuum_controller.clean_kitchen)


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_didnt_cook_does_not_vacuum(given_that, vacuum_controller, assert_that):
    given_that.kitchen_cleaning_state_is(
        livingroom_activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=days_ago(3)
    )

    vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_cooked_vacuums(given_that, vacuum_controller, assert_that):
    given_that.kitchen_cleaning_state_is(
        livingroom_activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was.sent_to_clean_kitchen()

@pytest.mark.asyncio
@freeze_time("2012-01-14 10:00:01")
def test_when_morning_waits(given_that, vacuum_controller, assert_that):
    given_that.kitchen_cleaning_state_is(
        livingroom_activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_vacuumed_updates_last_cleaned(given_that, vacuum_controller, assert_that):
    given_that.kitchen_cleaning_state_is(
        livingroom_activity=activities.LivingRoom.EMPTY,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.INPUT_DATETIME_SET_DATETIME).was.set_to_now(helpers.LAST_CLEANED_KITCHEN)


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_in_the_living_room_does_not_clean(given_that, vacuum_controller, assert_that, time_travel):
    given_that.kitchen_cleaning_state_is(
        livingroom_activity=activities.LivingRoom.WATCHING_TV,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_kitchen()

@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_in_the_kitchen_does_not_clean(given_that, vacuum_controller, assert_that, time_travel):
    given_that.kitchen_cleaning_state_is(
        livingroom_activity=activities.Kitchen.COOKING,
        last_cleaned=yesterday(),
        last_cooked=now()
    )

    vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_less_than_20_hours_since_last_clean_does_not_clean(given_that, vacuum_controller, assert_that,
                                                                 time_travel):
    given_that.kitchen_cleaning_state_is(
        livingroom_activity=activities.LivingRoom.EMPTY,
        last_cleaned=format_date((datetime.now() - timedelta(hours=19))),
        last_cooked=now()
    )

    vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_kitchen()


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_more_than_20_hours_since_last_clean_cleans(given_that, vacuum_controller, assert_that, time_travel):
    given_that.kitchen_cleaning_state_is(
        livingroom_activity=activities.LivingRoom.EMPTY,
        last_cleaned=format_date((datetime.now() - timedelta(hours=21))),
        last_cooked=now()
    )

    vacuum_controller.clean_kitchen(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was.sent_to_clean_kitchen()


def kitchen_cleaning_state_is(self, last_cleaned, last_cooked, livingroom_activity=activities.LivingRoom.EMPTY,
                              kitchen_activity=activities.Kitchen.EMPTY, studio_activity=activities.Studio.EMPTY):
    activity_handlers = activities.ActivityHandlers(None)
    self.state_of(helpers.LAST_COOKED).is_set_to(last_cooked)
    self.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to(last_cleaned)
    self.state_of(activity_handlers.livingroom._helper).is_set_to(livingroom_activity)
    self.state_of(activity_handlers.kitchen._helper).is_set_to(kitchen_activity)
    self.state_of(activity_handlers.studio._helper).is_set_to(studio_activity)


given.GivenThatWrapper.kitchen_cleaning_state_is = kitchen_cleaning_state_is
del kitchen_cleaning_state_is  # clean up namespace


def sent_to_clean_kitchen(self):
    self.called_with(
        entity_id=entities.VACUUM_FLICK,
        command="app_segment_clean",
        params=flick.Room.kitchen.value
    )


assertt.Was.sent_to_clean_kitchen = sent_to_clean_kitchen
del sent_to_clean_kitchen  # clean up namespace
