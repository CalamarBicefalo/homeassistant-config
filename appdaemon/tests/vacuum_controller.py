from datetime import datetime, time

from appdaemontestframework import automation_fixture

from apps.vacuum_controller import VacuumController


@automation_fixture(VacuumController)
def vacuum_controller():
    pass


def test_clean_kitchen_triggers_every_night(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .registered.run_daily("22:30:00") \
        .with_callback(vacuum_controller.clean_kitchen)


def test_clean_kitchen(given_that, vacuum_controller, assert_that):
    vacuum_controller.clean_kitchen(None)
    assert_that('xiaomi_miio/vacuum_clean_segment').was.called_with(
        entity_id="vacuum.roborock_vacuum_a15",
        segments=16
    )
