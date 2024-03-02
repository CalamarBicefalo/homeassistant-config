import pytest
from appdaemontestframework import automation_fixture, given_that as given, assert_that as assertt

import entities
import helpers
import matchers
import selects
import services
from test_utils import formatted_days_ago as days_ago
from appliances.flat_cleaner import FlatCleaner


@automation_fixture(FlatCleaner)
def vacuum_controller():
    matchers.init()
    pass


def test_triggers_when_away(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .listens_to.state(helpers.MODE, new=selects.Mode.AWAY) \
        .with_callback(vacuum_controller.clean_flat)


@pytest.mark.asyncio
def test_when_more_than_3_days_since_last_clean_does_not_clean(given_that, vacuum_controller, assert_that):
    given_that.flat_cleaning_state_is(
        last_cleaned=days_ago(4),
    )

    vacuum_controller.clean_flat(None, None, None, None, None)

    assert_that(services.VACUUM_START).was.sent_to_clean_flat()


@pytest.mark.asyncio
def test_when_less_than_3_days_since_last_clean_does_not_clean(given_that, vacuum_controller, assert_that):
    given_that.flat_cleaning_state_is(
        last_cleaned=days_ago(2),
    )

    vacuum_controller.clean_flat(None, None, None, None, None)

    assert_that(services.VACUUM_START).was_not.sent_to_clean_flat()


@pytest.mark.asyncio
def test_when_vacuumed_updates_last_cleaned(given_that, vacuum_controller, assert_that):
    given_that.flat_cleaning_state_is(
        last_cleaned=days_ago(7),
    )

    vacuum_controller.clean_flat(None, None, None, None, None)

    assert_that(services.INPUT_DATETIME_SET_DATETIME).was.set_to_now(helpers.LAST_CLEANED_FLAT)



def flat_cleaning_state_is(self, last_cleaned):
    self.state_of(helpers.LAST_CLEANED_FLAT).is_set_to(last_cleaned)


given.GivenThatWrapper.flat_cleaning_state_is = flat_cleaning_state_is
del flat_cleaning_state_is  # clean up namespace


def sent_to_clean_flat(self):
    self.called_with(
        entity_id=entities.VACUUM_FLICK,
    )


assertt.Was.sent_to_clean_flat = sent_to_clean_flat
del sent_to_clean_flat  # clean up namespace
