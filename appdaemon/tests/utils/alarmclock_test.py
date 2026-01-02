from datetime import datetime

import pytest
from appdaemontestframework import automation_fixture, given_that as given

import entities
import matchers
from alarmclock import AlarmClock
from app import App


class AlarmClockApp(App):
    def initialize(self) -> None:
        self.alarm_clock = AlarmClock(self)
        self.callback_count = 0

    def test_callback(self) -> None:
        self.callback_count += 1


@automation_fixture(AlarmClockApp)
def app() -> None:
    matchers.init()
    pass


def test_listens_to_ios_alarm_time_changes(given_that, app, assert_that):
    app.alarm_clock.run_before_alarm(app.test_callback)
    
    assert_that(app).listens_to.state(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED)
    assert_that(app).listens_to.state(entities.INPUT_DATETIME_IOS_ALARM_TIME)


def test_ios_alarm_triggers_callback_one_hour_before_alarm(given_that, app, time_travel):
    given_that.alarm_state_is(alarm_time="09:00", current_time="2024-01-15 06:00:00")
    app.alarm_clock.run_before_alarm(app.test_callback, hours=1)
    
    state_callback = app.alarm_clock._on_ios_alarm_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_IOS_ALARM_TIME, 'state', '08:00', '09:00')
    
    assert app.callback_count == 0
    time_travel.fast_forward(119).minutes()
    assert app.callback_count == 0
    time_travel.fast_forward(1).minutes()
    assert app.callback_count == 1


def test_ios_alarm_change_cancels_previous_callback(given_that, app, time_travel):
    given_that.alarm_state_is(alarm_time="09:00", current_time="2024-01-15 06:00:00")
    app.alarm_clock.run_before_alarm(app.test_callback, hours=1)
    state_callback = app.alarm_clock._on_ios_alarm_change(app.test_callback)
    
    given_that.state_of(entities.INPUT_DATETIME_IOS_ALARM_TIME).is_set_to("09:00")
    state_callback(entities.INPUT_DATETIME_IOS_ALARM_TIME, 'state', '', '09:00')
    
    app.set_state(entities.INPUT_DATETIME_IOS_ALARM_TIME, state="13:00")
    state_callback(entities.INPUT_DATETIME_IOS_ALARM_TIME, 'state', '09:00', '13:00')
    
    time_travel.fast_forward(360).minutes()
    assert app.callback_count == 1


def test_ios_alarm_handles_next_day_alarm(given_that, app, time_travel):
    given_that.alarm_state_is(alarm_time="07:00", current_time="2024-01-15 22:00:00")
    app.alarm_clock.run_before_alarm(app.test_callback, hours=1)
    
    state_callback = app.alarm_clock._on_ios_alarm_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_IOS_ALARM_TIME, 'state', '08:00', '07:00')
    
    assert app.callback_count == 0
    time_travel.fast_forward(480).minutes()
    assert app.callback_count == 1


def test_ios_alarm_in_past_schedules_for_next_day(given_that, app, time_travel):
    given_that.alarm_state_is(alarm_time="08:00", current_time="2024-01-15 12:00:00")
    app.alarm_clock.run_before_alarm(app.test_callback, hours=1)
    
    state_callback = app.alarm_clock._on_ios_alarm_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_IOS_ALARM_TIME, 'state', '09:00', '08:00')
    
    assert app.alarm_clock._scheduled_one_hour_timer is not None
    assert app.callback_count == 0
    time_travel.fast_forward(1140).minutes()
    assert app.callback_count == 1


def test_ios_alarm_not_home_does_not_schedule(given_that, app):
    given_that.alarm_state_is(alarm_time="09:00", current_time="2024-01-15 06:00:00", device_tracker="away")
    app.alarm_clock.run_before_alarm(app.test_callback)
    
    state_callback = app.alarm_clock._on_ios_alarm_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_IOS_ALARM_TIME, 'state', '08:00', '09:00')
    
    assert app.alarm_clock._scheduled_one_hour_timer is None
    assert app.callback_count == 0


def test_ios_alarm_disabled_does_not_schedule(given_that, app):
    given_that.alarm_state_is(alarm_time="09:00", current_time="2024-01-15 06:00:00", alarm_enabled="off")
    app.alarm_clock.run_before_alarm(app.test_callback)
    
    state_callback = app.alarm_clock._on_ios_alarm_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_IOS_ALARM_TIME, 'state', '08:00', '09:00')
    
    assert app.alarm_clock._scheduled_one_hour_timer is None
    assert app.callback_count == 0


def test_daily_3am_scheduler_sets_alarm_callback(given_that, app, time_travel):
    given_that.alarm_state_is(alarm_time="08:00", current_time="2024-01-15 03:00:00")
    app.alarm_clock.run_before_alarm(app.test_callback, hours=1)
    
    daily_callback = app.alarm_clock._on_daily_ios_alarm_check(app.test_callback)
    daily_callback({})
    
    assert app.alarm_clock._scheduled_one_hour_timer is not None
    time_travel.fast_forward(300).minutes()
    assert app.callback_count == 1


def test_configurable_offset_30_minutes(given_that, app, time_travel):
    given_that.alarm_state_is(alarm_time="10:00", current_time="2024-01-15 08:00:00")
    app.alarm_clock.run_before_alarm(app.test_callback, minutes=30)
    
    state_callback = app.alarm_clock._on_ios_alarm_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_IOS_ALARM_TIME, 'state', '09:00', '10:00')
    
    assert app.callback_count == 0
    time_travel.fast_forward(90).minutes()
    assert app.callback_count == 1


def dt(datetime_string: str) -> datetime:
    """Helper to parse datetime strings in tests for consistency."""
    return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")


def alarm_state_is(self,
                   device_tracker="home",
                   alarm_enabled="on",
                   alarm_time="09:00",
                   current_time="2024-01-15 06:00:00"):
    self.state_of(entities.DEVICE_TRACKER_JC_IPHONE).is_set_to(device_tracker)
    self.state_of(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED).is_set_to(alarm_enabled)
    self.state_of(entities.INPUT_DATETIME_IOS_ALARM_TIME).is_set_to(alarm_time)
    self.time_is(dt(current_time))


given.GivenThatWrapper.alarm_state_is = alarm_state_is
del alarm_state_is
