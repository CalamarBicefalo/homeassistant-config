from datetime import datetime, time

import pytest
from appdaemontestframework import automation_fixture, given_that as given, assert_that as assertt
from freezegun import freeze_time

import entities
import helpers
import matchers
import services
from modes import Mode
from rooms import *
from test_utils import formatted_yesterday as yesterday, formatted_now as now, formatted_days_ago as days_ago, \
    format_date
from vacuum.room_cleaner import RoomCleaner


@automation_fixture(RoomCleaner)
def app():
    matchers.init()
    pass

@pytest.fixture
def bedroom(app):
    return RoomHandlers(app).bedroom


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_vacuumed_updates_last_cleaned(given_that, bedroom, assert_that):
    given_that.bedroom_cleaning_state_is(
        wardrobe_activity=Wardrobe.Activity.EMPTY,
        last_cleaned=yesterday(),
    )

    bedroom.clean()

    assert_that(services.INPUT_DATETIME_SET_DATETIME).was.set_to_now(Bedroom._last_cleaned_helper)


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_dirty_and_appropriate_cleans(given_that, bedroom, assert_that, time_travel):
    given_that.bedroom_cleaning_state_is(
        wardrobe_activity=Wardrobe.Activity.EMPTY,
        bedroom_activity=Bedroom.Activity.EMPTY,
        last_cleaned=yesterday(),
    )

    bedroom.clean_if_needed()

    assert_that(services.VACUUM_SEND_COMMAND).was.sent_to_clean_bedroom()


@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_in_the_adjacent_open_room_does_not_clean(given_that, bedroom, assert_that, time_travel):
    given_that.bedroom_cleaning_state_is(
        wardrobe_activity=Wardrobe.Activity.DRESSING,
        bedroom_activity=Bedroom.Activity.EMPTY,
        last_cleaned=yesterday(),
    )

    bedroom.clean_if_needed()

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_bedroom()

@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_in_the_room_does_not_clean(given_that, bedroom, assert_that, time_travel):
    given_that.bedroom_cleaning_state_is(
        wardrobe_activity=Bedroom.Activity.EMPTY,
        bedroom_activity=Bedroom.Activity.BEDTIME,
        last_cleaned=yesterday(),
    )

    bedroom.clean_if_needed()

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_bedroom()

@pytest.mark.asyncio
@freeze_time("2012-01-14 23:00:01")
def test_when_sleeping_does_not_clean(given_that, bedroom, assert_that, time_travel):
    given_that.bedroom_cleaning_state_is(
        last_cleaned=yesterday(),
        mode=Mode.SLEEPING,
    )

    bedroom.clean_if_needed()

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_bedroom()


@pytest.mark.asyncio
@freeze_time("2012-01-14 15:59:00")
def test_when_before_allowed_clean_time_does_not_clean(given_that, bedroom, assert_that, time_travel):
    given_that.bedroom_cleaning_state_is(
        wardrobe_activity=Wardrobe.Activity.EMPTY,
        bedroom_activity=Bedroom.Activity.EMPTY,
        last_cleaned=yesterday(),
    )

    bedroom.clean_after = 16
    bedroom.clean_if_needed()
    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_to_clean_bedroom()

    bedroom.clean_after = 15
    bedroom.clean_if_needed()
    assert_that(services.VACUUM_SEND_COMMAND).was.sent_to_clean_bedroom()


def bedroom_cleaning_state_is(self, last_cleaned,
                              wardrobe_activity=Wardrobe.Activity.EMPTY,
                              bedroom_activity=Bedroom.Activity.EMPTY,
                              mode=Mode.NIGHT):
    self.state_of(helpers.HOMEASSISTANT_MODE).is_set_to(mode)
    self.state_of(Bedroom._last_cleaned_helper).is_set_to(last_cleaned)
    self.state_of(Wardrobe._activity_helper).is_set_to(wardrobe_activity)
    self.state_of(Bedroom._activity_helper).is_set_to(bedroom_activity)


given.GivenThatWrapper.bedroom_cleaning_state_is = bedroom_cleaning_state_is
del bedroom_cleaning_state_is  # clean up namespace


def sent_to_clean_bedroom(self):
    self.called_with(
        entity_id=entities.VACUUM_FLICK,
        command="app_segment_clean",
        params=Bedroom._room_cleaner_segment
    )


assertt.Was.sent_to_clean_bedroom = sent_to_clean_bedroom
del sent_to_clean_bedroom  # clean up namespace
