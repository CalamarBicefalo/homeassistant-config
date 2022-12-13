import pytest
from appdaemontestframework import automation_fixture

import activities
import helpers
import matchers
import modes
import services
from away_monitor import AwayMonitor


@automation_fixture(AwayMonitor)
def monitor() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_away_notifies_of_suspicious_activity(given_that, monitor, assert_that):
    given_that.state_of(helpers.HOMEASSISTANT_MODE).is_set_to(modes.Mode.AWAY)

    monitor.on_activity_change("hallway", None, None, "present", None)

    assert_that(services.NOTIFY_NOTIFY).was.called_with(
        message='Activity present detected in hallway while away from home',
        title="🚨Activity detected")


@pytest.mark.asyncio
def test_when_present_does_not_notify(given_that, monitor, assert_that):
    given_that.state_of(helpers.HOMEASSISTANT_MODE).is_set_to(modes.Mode.DAY)

    monitor.on_activity_change(None, None, None, None, None)

    assert_that(services.NOTIFY_NOTIFY).was_not.called()
