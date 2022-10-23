from datetime import datetime, time

from appdaemontestframework import automation_fixture

from apps import entities, services
from apps.vacuum_controller import VacuumController


@automation_fixture(VacuumController)
def vacuum_controller():
    pass


def test_clean_kitchen_triggers_every_night(given_that, vacuum_controller, assert_that):
    assert_that(vacuum_controller) \
        .registered.run_daily("22:30:00") \
        .with_callback(vacuum_controller.clean_kitchen)


def test_clean_kitchen_when_didnt_cook(given_that, vacuum_controller, assert_that):
    given_that.state_of(entities.HELPER_LAST_COOKED).is_set_to("2000-01-01 00:00:00")
    vacuum_controller.clean_kitchen(None)
    assert_that(services.VACUUM_CLEAN_SEGMENT).was_not.called_with(
        entity_id=entities.DEVICE_VACUUM_CLEANER,
        segments=16
    )

def test_clean_kitchen_when_cooked(given_that, vacuum_controller, assert_that):
    given_that.state_of(entities.HELPER_LAST_COOKED).is_set_to("2022-10-05 19:00:00")
    vacuum_controller.clean_kitchen(None)
    assert_that(services.VACUUM_CLEAN_SEGMENT).was.called_with(
        entity_id=entities.DEVICE_VACUUM_CLEANER,
        segments=16
    )
