from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Any, Callable, Optional

from appdaemon.plugins.hass import hassapi as hass

import entities
from state_handler import StateHandler


class AlarmClock:

    def __init__(self, app: hass.Hass):
        self._app = app
        self.state = StateHandler(app)
        self._scheduled_one_hour_timer = None
        self._callback_offset_seconds = 0  # Default to right on time

    def run_before_alarm(self, callback: Callable, hours: int = 0, minutes: int = 0, seconds: int = 0) -> None:
        self._callback_offset_seconds = hours * 3600 + minutes * 60 + seconds
        self._app.listen_state(self._on_ios_alarm_change(callback), entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED)
        self._app.listen_state(self._on_ios_alarm_change(callback), entities.INPUT_DATETIME_IOS_ALARM_TIME)
        
        # Schedule daily 3AM check to ensure callback is set when alarm time doesn't change
        self._app.run_daily(self._on_daily_ios_alarm_check(callback), time(3, 0, 0))

    # iOS Alarm state change handlers
    def _on_ios_alarm_change(self, callback: Callable) -> Callable[..., None]:
        def cb(entity, attribute, old, new, **kwargs) -> None:
            self._schedule_ios_alarm_callback(callback)
        return cb

    def _on_daily_ios_alarm_check(self, callback: Callable) -> Callable[..., None]:
        def cb(kwargs: Any) -> None:
            self._app.log('daily 3AM iOS alarm check triggered', level="INFO")
            self._schedule_ios_alarm_callback(callback)
        return cb

    def _schedule_ios_alarm_callback(self, callback: Callable) -> None:
        app = self._app
        state = self.state
        
        self._cancel_scheduled_one_hour_timer()
        
        if not state.is_home(entities.DEVICE_TRACKER_JC_IPHONE):
            app.log('device is not home, not scheduling callback', level="INFO")
            return
        
        is_enabled = state.is_on(entities.INPUT_BOOLEAN_IOS_ALARM_ENABLED)
        if not is_enabled:
            app.log('alarm is disabled, not scheduling callback', level="INFO")
            return
        
        alarm_time = state.get_as_time(entities.INPUT_DATETIME_IOS_ALARM_TIME)
        if not alarm_time:
            app.log('alarm time not set, not scheduling callback', level="WARNING")
            return
        
        alarm_datetime = self._calculate_next_alarm_datetime(alarm_time)
        if not alarm_datetime:
            app.log(f'failed to calculate alarm datetime from {alarm_time}', level="ERROR")
            return
        
        next_alarm_callback_time = alarm_datetime - timedelta(seconds=self._callback_offset_seconds)
        now = app.datetime()
        
        # Edge case: callback time can be in the past if we're within the offset window of the alarm
        if next_alarm_callback_time <= now:
            app.log(f'alarm callback time {next_alarm_callback_time} is in the past (now: {now}), not scheduling callback', level="WARNING")
            return
        
        delay_seconds = (next_alarm_callback_time - now).total_seconds()
        app.log(f'scheduling alarm callback for {next_alarm_callback_time} (in {_format_duration(delay_seconds)}, offset={_format_duration(self._callback_offset_seconds)})', level="INFO")

        def one_hour_before(kwargs: Any) -> None:
            app.log(f'triggering callback scheduled at={next_alarm_callback_time}')
            self._scheduled_one_hour_timer = None
            callback()

        self._scheduled_one_hour_timer = app.run_in(one_hour_before, delay_seconds)

    def _cancel_scheduled_one_hour_timer(self):
        if self._scheduled_one_hour_timer:
            self._app.cancel_timer(self._scheduled_one_hour_timer, True)
        self._scheduled_one_hour_timer = None

    def _calculate_next_alarm_datetime(self, alarm_time: time) -> Optional[datetime]:
        try:
            now = self._app.datetime()
            alarm_today = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)
            
            if alarm_today > now:
                return alarm_today
            else:
                return alarm_today + timedelta(days=1)
        except (ValueError, AttributeError) as e:
            self._app.log(f'Error calculating alarm datetime from {alarm_time}: {e}', level="ERROR")
            return None

def _format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable format like '2h 15m' or '45m' or '30s'."""
    if seconds < 60:
        return f"{int(seconds)}s"

    minutes = int(seconds // 60)
    if minutes < 60:
        return f"{minutes}m"

    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes > 0:
        return f"{hours}h {remaining_minutes}m"
    return f"{hours}h"

