from unittest import mock

import entities
import matchers
import pytest
from appdaemontestframework import automation_fixture, given_that as given, assert_that as assertt

import activities
import helpers
import services
import states
import test_utils
from flick import FlickHandler
from vacuum.mop_maintenance import MopMaintenance


@automation_fixture(MopMaintenance)
def vacuum_controller():
    matchers.init()
    pass


def test_clean_mop_maintenance_triggers_while_in_kitchen(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .listens_to.state(vacuum_controller.activities.kitchen._helper,
                          old=activities.Kitchen.EMPTY,
                          new=activities.Kitchen.PRESENT) \
        .with_callback(vacuum_controller.start_mop_maintenance)


@pytest.mark.asyncio
def test_mop_when_flick_cleaning_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.mop_maintenance_state_is(
        last_cleaned=test_utils.formatted_minutes_ago(60),
        last_maintenance=test_utils.formatted_yesterday(),
        flick=states.CLEANING
    )

    with mock.patch.object(FlickHandler, 'go_to_maintenance_spot') as flick:
        vacuum_controller.flick = flick
        vacuum_controller.start_mop_maintenance(None, None, None, None, None)

        flick.go_to_maintenance_spot.assert_not_called()



@pytest.mark.asyncio
def test_mop_when_clean_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.mop_maintenance_state_is(
        last_cleaned=test_utils.formatted_yesterday(),
        last_maintenance=test_utils.formatted_now(),
    )

    with mock.patch.object(FlickHandler, 'go_to_maintenance_spot') as flick:
        vacuum_controller.flick = flick
        vacuum_controller.start_mop_maintenance(None, None, None, None, None)

        flick.go_to_maintenance_spot.assert_not_called()

@pytest.mark.asyncio
def test_mop_when_just_cleaned_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.mop_maintenance_state_is(
        last_cleaned=test_utils.formatted_minutes_ago(15),
        last_maintenance=test_utils.formatted_yesterday(),
    )

    with mock.patch.object(FlickHandler, 'go_to_maintenance_spot') as flick:
        vacuum_controller.flick = flick
        vacuum_controller.start_mop_maintenance(None, None, None, None, None)

        flick.go_to_maintenance_spot.assert_not_called()


@pytest.mark.asyncio
def test_mop_when_dirty_goes_to_maintenance_spot(given_that, vacuum_controller, assert_that):
    given_that.mop_maintenance_state_is(
        last_cleaned=test_utils.formatted_minutes_ago(60),
        last_maintenance=test_utils.formatted_yesterday(),
    )

    with mock.patch.object(FlickHandler, 'go_to_maintenance_spot') as flick:
        vacuum_controller.flick = flick
        vacuum_controller.start_mop_maintenance(None, None, None, None, None)

        flick.go_to_maintenance_spot.assert_called_once()


@pytest.mark.asyncio
def test_mop_when_cleaned_updates_helper(given_that, vacuum_controller, assert_that):
    given_that.mop_maintenance_state_is(
        last_cleaned=test_utils.formatted_minutes_ago(60),
        last_maintenance=test_utils.formatted_yesterday(),
    )

    vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.INPUT_DATETIME_SET_DATETIME).was.set_to_now(helpers.LAST_CLEANED_VACUUM_MOP)


def mop_maintenance_state_is(self, last_cleaned, last_maintenance, flick=states.DOCKED):
    self.state_of(helpers.LAST_CLEANED_FLAT).is_set_to(last_cleaned)
    self.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to(last_maintenance)
    self.state_of(entities.VACUUM_FLICK).is_set_to(flick)


given.GivenThatWrapper.mop_maintenance_state_is = mop_maintenance_state_is
del mop_maintenance_state_is  # clean up namespace
