import pytest, matchers
from appdaemontestframework import automation_fixture

import activities
import entities
import services
from activity_controllers.generic_controller import MotionController
from utils.select_handler import SelectHandler
from utils import states


class GenericMotionController(MotionController):
    motion_sensor = entities.Entity("motion-sensor")
    cooldown_seconds = 2

    @property
    def activity(self) -> SelectHandler:
        return self.activities.kitchen


@automation_fixture(GenericMotionController)
def subject():
    matchers.init()
    pass


def test_triggers_when_motion(given_that, subject, assert_that):
    assert_that(subject) \
        .listens_to.state(["motion-sensor"]) \
        .with_callback(subject.controller_handler)


@pytest.mark.asyncio
def test_when_present(given_that, subject, assert_that):
    subject.controller_handler("motion-sensor", None, None, states.DETECTED, None)

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.kitchen_helper,
                                                                         activities.Kitchen.PRESENT)


@pytest.mark.asyncio
def test_when_away(given_that, subject, assert_that, time_travel):
    subject.controller_handler("motion-sensor", None, None, states.NOT_DETECTED, None)

    time_travel.fast_forward(2).minutes()

    assert_that(services.INPUT_SELECT_SELECT_OPTION).was.set_to_activity(activities.kitchen_helper,
                                                                         activities.Kitchen.EMPTY)

@pytest.mark.asyncio
def test_when_retriggering(given_that, subject, assert_that, time_travel):
    subject.controller_handler("motion-sensor", None, None, states.DETECTED, None)
    time_travel.fast_forward(1).minutes()
    subject.controller_handler("motion-sensor", None, None, states.DETECTED, None)
    time_travel.fast_forward(1).minutes()
    subject.controller_handler("motion-sensor", None, None, states.DETECTED, None)
    time_travel.fast_forward(1).minutes()
    subject.controller_handler("motion-sensor", None, None, states.DETECTED, None)
    time_travel.fast_forward(1).minutes()


    assert_that(services.INPUT_SELECT_SELECT_OPTION).was_not.set_to_activity(activities.kitchen_helper,
                                                                         activities.Kitchen.EMPTY)
