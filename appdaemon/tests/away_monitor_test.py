import pytest
from appdaemontestframework import automation_fixture

import helpers
import matchers
import selects
import services
from away_monitor import AwayMonitor


@automation_fixture(AwayMonitor)
def monitor() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_when_away_notifies_of_suspicious_activity(given_that, monitor, assert_that):
    given_that.state_of(helpers.MODE).is_set_to(selects.Mode.AWAY)

    monitor.on_door_open(None, None, None, None, None)

    assert_that(services.NOTIFY_MOBILE_APP_JC_IPHONE).was.called_with(
        message=f'Front door opened while away',
        title="🚨Activity detected")


@pytest.mark.asyncio
def test_when_present_does_not_notify(given_that, monitor, assert_that):
    given_that.state_of(helpers.MODE).is_set_to(selects.Mode.DAY)

    monitor.on_door_open(None, None, None, None, None)

    assert_that(services.NOTIFY_MOBILE_APP_JC_IPHONE).was_not.called()
