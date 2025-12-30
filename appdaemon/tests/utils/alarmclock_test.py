from datetime import datetime

import pytest
from appdaemontestframework import automation_fixture, given_that as given

import entities
import matchers
from alarmclock import AlarmClock, SLEEP_AS_ANDROID_EVENT, SLEEP_AS_ANDROID_ONE_HOUR_BEFORE_ALARM
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


def test_listens_to_android_event(given_that, app, assert_that):
    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    
    assert_that(app).listens_to.event(SLEEP_AS_ANDROID_EVENT)


def test_listens_to_ios_alarm_time_changes(given_that, app, assert_that):
    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    
    assert_that(app).listens_to.state(entities.INPUT_DATETIME_NEXT_IOS_ALARM)


def test_listens_to_ios_alarm_dismissed(given_that, app, assert_that):
    app.alarm_clock.listen_on_ios_alarm_dismissed(app.test_callback)
    
    assert_that(app).listens_to.state(entities.INPUT_DATETIME_SKIPPED_IOS_ALARM)


def test_android_event_triggers_callback_immediately(given_that, app):
    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    
    # Trigger the event callback manually (simulating the event firing)
    callback = app.alarm_clock._on_event(app.test_callback)
    callback(SLEEP_AS_ANDROID_EVENT, {'event': SLEEP_AS_ANDROID_ONE_HOUR_BEFORE_ALARM}, {})
    
    assert app.callback_count == 1


def test_android_event_with_different_event_type_does_not_trigger(given_that, app):
    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    
    # Trigger the event callback manually with different event type
    callback = app.alarm_clock._on_event(app.test_callback)
    callback(SLEEP_AS_ANDROID_EVENT, {'event': 'some_other_event'}, {})
    
    assert app.callback_count == 0


def test_ios_alarm_triggers_callback_one_hour_before_alarm(given_that, app, time_travel):
    given_that.state_of(entities.INPUT_DATETIME_NEXT_IOS_ALARM).is_set_to("2024-01-15 09:00:00")
    given_that.time_is(dt("2024-01-15 06:00:00"))

    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    
    # Manually trigger the state callback to simulate alarm change
    state_callback = app.alarm_clock._on_ios_alarm_time_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_NEXT_IOS_ALARM, 'state', '2024-01-15 08:00:00', '2024-01-15 09:00:00')
    
    # Callback should not be triggered yet
    assert app.callback_count == 0
    
    # Fast forward almost to callback time (1 hour 59 minutes)
    time_travel.fast_forward(119).minutes()
    assert app.callback_count == 0
    
    # Fast forward 1 more minute to reach exactly the callback time (2 hours = 8AM)
    time_travel.fast_forward(1).minutes()
    
    # Callback should now be triggered
    assert app.callback_count == 1


def test_ios_alarm_change_cancels_previous_callback(given_that, app, time_travel):
    given_that.time_is(dt("2024-01-15 06:00:00"))
    
    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    state_callback = app.alarm_clock._on_ios_alarm_time_change(app.test_callback)
    
    # Set up first timer (9AM alarm → 8AM callback in 120 min)
    given_that.state_of(entities.INPUT_DATETIME_NEXT_IOS_ALARM).is_set_to("2024-01-15 09:00:00")
    state_callback(entities.INPUT_DATETIME_NEXT_IOS_ALARM, 'state', '', '2024-01-15 09:00:00')
    
    # Immediately change alarm to 12PM (callback at 11AM = 300 min from start)
    app.set_state(entities.INPUT_DATETIME_NEXT_IOS_ALARM, state="2024-01-15 12:00:00")
    state_callback(entities.INPUT_DATETIME_NEXT_IOS_ALARM, 'state', '2024-01-15 09:00:00', '2024-01-15 12:00:00')
    
    # Fast forward directly to new callback time (11AM = 300 minutes)
    time_travel.fast_forward(300).minutes()
    
    # Callback should be triggered exactly once (from second timer only, first was cancelled)
    assert app.callback_count == 1


def test_ios_alarm_handles_next_day_alarm(given_that, app, time_travel):
    given_that.state_of(entities.INPUT_DATETIME_NEXT_IOS_ALARM).is_set_to("2024-01-16 08:00:00")
    given_that.time_is(dt("2024-01-15 23:00:00"))
    
    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    
    # Trigger alarm for 8AM tomorrow at 11:00 PM today
    state_callback = app.alarm_clock._on_ios_alarm_time_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_NEXT_IOS_ALARM, 'state', '2024-01-15 08:00:00', '2024-01-16 08:00:00')
    
    # Callback should not trigger immediately
    assert app.callback_count == 0
    
    # Fast forward to 7AM next day (8 hours)
    time_travel.fast_forward(480).minutes()
    
    # Callback should now be triggered
    assert app.callback_count == 1


def test_ios_alarm_in_past_does_not_schedule(given_that, app):
    # Alarm is set for 8AM but it's already 10AM
    given_that.state_of(entities.INPUT_DATETIME_NEXT_IOS_ALARM).is_set_to("2024-01-15 08:00:00")
    given_that.time_is(dt("2024-01-15 10:00:00"))
    
    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    
    # Set current time to 10AM (alarm callback time of 7AM is in the past)
    state_callback = app.alarm_clock._on_ios_alarm_time_change(app.test_callback)
    state_callback(entities.INPUT_DATETIME_NEXT_IOS_ALARM, 'state', '2024-01-15 07:00:00', '2024-01-15 08:00:00')
    
    # No timer should be scheduled
    assert app.alarm_clock._scheduled_one_hour_timer is None
    
    # Callback should never be triggered
    assert app.callback_count == 0


def test_ios_alarm_dismissed_triggers_callback_immediately(given_that, app):
    given_that.state_of(entities.INPUT_DATETIME_SKIPPED_IOS_ALARM).is_set_to("2024-01-15 06:00:00")
    
    app.alarm_clock.listen_on_ios_alarm_dismissed(app.test_callback)
    
    # Trigger the state callback manually
    callback = app.alarm_clock._on_alarm_dismissed(app.test_callback)
    callback(entities.INPUT_DATETIME_SKIPPED_IOS_ALARM, 'state', '2024-01-15 06:00:00', '2024-01-15 08:00:00')
    
    # Callback should be triggered immediately
    assert app.callback_count == 1


def test_both_android_and_ios_use_same_callback(given_that, app):
    app.alarm_clock.listen_one_hour_before_alarm(app.test_callback)
    
    # Trigger via Android event
    event_callback = app.alarm_clock._on_event(app.test_callback)
    event_callback(SLEEP_AS_ANDROID_EVENT, {'event': SLEEP_AS_ANDROID_ONE_HOUR_BEFORE_ALARM}, {})
    
    assert app.callback_count == 1
    
    # Trigger via iOS alarm dismissal
    dismissal_callback = app.alarm_clock._on_alarm_dismissed(app.test_callback)
    dismissal_callback(entities.INPUT_DATETIME_SKIPPED_IOS_ALARM, 'state', '2024-01-15 06:00:00', '2024-01-15 08:00:00')
    
    # Same callback should be triggered twice
    assert app.callback_count == 2

def dt(datetime_string: str) -> datetime:
    """Helper to parse datetime strings in tests for consistency."""
    return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
