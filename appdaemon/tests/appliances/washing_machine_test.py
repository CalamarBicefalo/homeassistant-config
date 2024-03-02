import pytest
from appdaemontestframework import automation_fixture, given_that as given, assert_that as assertt

import entities
import helpers
import matchers
import selects
import services
import states
from test_utils import formatted_days_ago as days_ago, formatted_now as now
from appliances.washing_machine import WashingMachine


@automation_fixture(WashingMachine)
def washing_machine():
    matchers.init()
    pass


def test_triggers_when_door_changes(given_that, washing_machine, assert_that):
    assert_that(washing_machine) \
        .listens_to.state(entities.BINARY_SENSOR_WASHING_MACHINE_CS) \
        .with_callback(washing_machine.update_state)

def test_triggers_when_power_changes(given_that, washing_machine, assert_that):
    assert_that(washing_machine) \
        .listens_to.state(entities.SENSOR_WASHING_MACHINE_SWITCH_INSTANTANEOUS_DEMAND) \
        .with_callback(washing_machine.update_state)


@pytest.mark.asyncio
def test_when_door_open_sets_drying(given_that, washing_machine, assert_that):
    given_that.washing_machine_state_is(
        last_washed=days_ago(4),
        door=states.OPEN
    )

    washing_machine.update_state(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_option(entities.INPUT_SELECT_WASHING_MACHINE,
                                                                         selects.WashingMachine.DRYING)

@pytest.mark.asyncio
def test_when_using_power_sets_washing(given_that, washing_machine, assert_that):
    given_that.washing_machine_state_is(
        power=20,
    )

    washing_machine.update_state(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_option(entities.INPUT_SELECT_WASHING_MACHINE,
                                                                         selects.WashingMachine.WASHING)

@pytest.mark.asyncio
def test_eventually_marks_washing_as_finished(given_that, washing_machine, assert_that, time_travel):
    given_that.washing_machine_state_is(
        power=1,
        previous_state=selects.WashingMachine.WASHING,
    )
    washing_machine.update_state(None, None, None, None, None)
    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.called()

    time_travel.fast_forward(300).seconds()
    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_option(entities.INPUT_SELECT_WASHING_MACHINE,
                                                                       selects.WashingMachine.WET_CLOTHES_INSIDE)

@pytest.mark.asyncio
def test_when_door_closed_after_washing(given_that, washing_machine, assert_that):
    given_that.washing_machine_state_is(
        power=1,
        last_washed=now(),
        door=states.CLOSED,
        previous_state=selects.WashingMachine.DRYING
    )

    washing_machine.update_state(None, None, None, None, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_option(entities.INPUT_SELECT_WASHING_MACHINE,
                                                                         selects.WashingMachine.MOLD_ALERT)


def washing_machine_state_is(self, last_washed=days_ago(1), door=states.CLOSED, power=0, previous_state=selects.WashingMachine.OFF):
    self.state_of(helpers.LAST_WASHED_CLOTHES).is_set_to(last_washed)
    self.state_of(entities.BINARY_SENSOR_WASHING_MACHINE_CS).is_set_to(door)
    self.state_of(entities.SENSOR_WASHING_MACHINE_SWITCH_INSTANTANEOUS_DEMAND).is_set_to(power)
    self.state_of(entities.INPUT_SELECT_WASHING_MACHINE).is_set_to(previous_state)


given.GivenThatWrapper.washing_machine_state_is = washing_machine_state_is
del washing_machine_state_is  # clean up namespace
