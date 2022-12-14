import entities
import matchers
import pytest
from appdaemontestframework import automation_fixture, assert_that as assertt

import activities
import helpers
import services
import test_utils
from vacuum.mop_maintenance import MopMaintenance, mop_maintenance


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
def test_mop_when_clean_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to((test_utils.formatted_yesterday()))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to((test_utils.formatted_now()))

    vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_for_maintenance_to_kitchen()

@pytest.mark.asyncio
def test_mop_when_just_cleaned_does_nothing(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to((test_utils.formatted_minutes_ago(15)))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to((test_utils.formatted_yesterday()))

    vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was_not.sent_for_maintenance_to_kitchen()


@pytest.mark.asyncio
def test_mop_when_dirty_goes_to_maintenance_spot(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to((test_utils.formatted_minutes_ago(60)))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to((test_utils.formatted_yesterday()))

    vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.VACUUM_SEND_COMMAND).was.sent_for_maintenance_to_kitchen()


@pytest.mark.asyncio
def test_mop_when_cleaned_updates_helper(given_that, vacuum_controller, assert_that):
    given_that.state_of(helpers.LAST_CLEANED_KITCHEN).is_set_to((test_utils.formatted_minutes_ago(60)))
    given_that.state_of(helpers.LAST_CLEANED_VACUUM_MOP).is_set_to((test_utils.formatted_yesterday()))

    vacuum_controller.start_mop_maintenance(None, None, None, None, None)

    assert_that(services.INPUT_DATETIME_SET_DATETIME).was.set_to_now(helpers.LAST_CLEANED_VACUUM_MOP)


def sent_for_maintenance_to_kitchen(self):
    self.called_with(
        entity_id=entities.VACUUM_FLICK,
        command="app_goto_target",
        params=[mop_maintenance.x, mop_maintenance.y]
    )


assertt.Was.sent_for_maintenance_to_kitchen = sent_for_maintenance_to_kitchen
del sent_for_maintenance_to_kitchen
