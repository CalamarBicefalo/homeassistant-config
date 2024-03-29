import pytest, matchers
from appdaemontestframework import automation_fixture

from rooms import *
import entities
import services
from activity_controllers.generic_controller import MotionController
from select_handler import SelectHandler
import states


class GenericMotionController(MotionController):
    motion_sensor = entities.Entity("motion-sensor")
    cooldown_seconds = 2

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.bedroom.activity

    def ignore_motion_trigger(self) -> bool:
        return True


@automation_fixture(GenericMotionController)
def subject():
    matchers.init()
    pass


@pytest.mark.asyncio
def test_triggers_when_ignoring_motion_does_nothing(given_that, subject, assert_that):
    given_that.state_of("motion-sensor").is_set_to(states.ON)

    subject.controller_handler("motion-sensor", None, None, states.DETECTED, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(Bedroom._activity_helper,
                                                                         Bedroom.Activity.PRESENT)
