from datetime import datetime, time

from appdaemontestframework import automation_fixture

from apps.vacuum_controller import VacuumController


@automation_fixture(VacuumController)
def vacuum_controller():
    pass


def test_clean_kitchen_triggers_every_night(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .registered.run_daily(time(hour=22)) \
        .with_callback(vacuum_controller.clean_kitchen)


# def test_clean_kitchen(given_that, vacuum_controller, assert_that):
# given_that TV is off & kitchen presence has been active in the last 24 hours then go clean
# given_that.state_of(datetime(2020, 1, 1, 22, 0, 0))
# vacuum_controller.clean_kitchen(None, None, None)
# assert_that('light.living_room').was.turned_on()
