from datetime import datetime
from unittest.mock import patch

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from appdaemontestframework import automation_fixture

import matchers
from error_reporter import ErrorReporter, LAST_ERROR_SENSOR, ERROR_EVENT

TS = datetime(2026, 5, 31, 12, 0, 0)


@pytest.fixture(autouse=True)
def stub_listen_log():
    # listen_log is not mocked by the test framework; stub it so initialize()
    # (run when the automation fixture is built) doesn't reach real AppDaemon.
    with patch.object(Hass, "listen_log"):
        yield


@automation_fixture(ErrorReporter)
def reporter() -> None:
    matchers.init()


@pytest.mark.asyncio
def test_warning_is_mirrored_to_sensor_and_event(reporter, hass_mocks):
    reporter.on_log("Some app", TS, "WARNING", "error_log", "boom happened", {})

    set_state = hass_mocks.hass_functions["set_state"]
    set_state.assert_called_once()
    args, kwargs = set_state.call_args
    assert args[0] == LAST_ERROR_SENSOR
    assert kwargs["state"] == "WARNING [Some app] boom happened"
    assert kwargs["attributes"]["app"] == "Some app"
    assert kwargs["attributes"]["level"] == "WARNING"
    assert kwargs["attributes"]["type"] == "error_log"
    assert kwargs["attributes"]["message"] == "boom happened"

    hass_mocks.hass_functions["fire_event"].assert_called_once_with(
        ERROR_EVENT, app="Some app", level="WARNING", message="boom happened")


@pytest.mark.asyncio
def test_own_log_records_are_ignored(reporter, hass_mocks):
    reporter.on_log(reporter.name, TS, "WARNING", "main_log", "noise", {})

    hass_mocks.hass_functions["set_state"].assert_not_called()
    hass_mocks.hass_functions["fire_event"].assert_not_called()


@pytest.mark.asyncio
def test_headline_is_truncated_to_single_line_but_message_is_kept(reporter, hass_mocks):
    long_message = "first line " + "x" * 400 + "\nsecond line"

    reporter.on_log("App", TS, "ERROR", "error_log", long_message, {})

    kwargs = hass_mocks.hass_functions["set_state"].call_args.kwargs
    assert len(kwargs["state"]) <= 255
    assert "\n" not in kwargs["state"]
    assert kwargs["attributes"]["message"] == long_message
