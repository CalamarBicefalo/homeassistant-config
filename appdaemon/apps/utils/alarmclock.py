from __future__ import annotations

from datetime import timedelta
from typing import Any, Callable

from appdaemon.plugins.hass import hassapi as hass

import entities
from state_handler import StateHandler

# MQTT event encapsulating all Sleep as Android events
SLEEP_AS_ANDROID_EVENT = "SleepAsAndroid_phone"
# Sleep As Android known events
SLEEP_AS_ANDROID_ONE_HOUR_BEFORE_ALARM = 'before_alarm'


class AlarmClock:

    def __init__(self, app: hass.Hass):
        self._app = app
        self.state = StateHandler(app)
        self._scheduled_one_hour_timer = None

    def listen_one_hour_before_alarm(self, callback: Callable) -> None:
        self._app.listen_event(self._on_event(callback), SLEEP_AS_ANDROID_EVENT)
        self._app.listen_state(self._on_ios_alarm_time_change(callback), entities.INPUT_DATETIME_NEXT_IOS_ALARM)

    def listen_on_ios_alarm_dismissed(self, callback: Callable) -> None:
        self._app.listen_state(self._on_alarm_dismissed(callback), entities.INPUT_DATETIME_SKIPPED_IOS_ALARM)


    # MQTT events sent by Sleep As Android
    def _on_event(self, callback: Callable) -> Callable[[Any, str, Any, Any], None]:
        def on_specified_event(event_name: str, data: Any, kwargs: Any) -> None:
            self._app.log(f'received alarm clock event {data["event"]} ',
                level="INFO")
            if data['event'] == SLEEP_AS_ANDROID_ONE_HOUR_BEFORE_ALARM: callback()

        return on_specified_event

    # Updates on known datetime helpers for iOS Alarms
    def _on_ios_alarm_time_change(self, callback: Callable) -> Callable[..., None]:
        app = self._app
        state = self.state

        def cb(entity, attribute, old, new, **kwargs) -> None:
            nextalarm = state.get_as_datetime(entities.INPUT_DATETIME_NEXT_IOS_ALARM) - timedelta(hours=1)
            app.log(f'alarm time changed in entity={entity}, scheduling callback for next alarm={nextalarm}')

            def one_hour_before(**kwargs: Any) -> None:
                app.log(f'triggering callback scheduled by entity={entity} at={nextalarm} ')
                self._scheduled_one_hour_timer = None
                callback()

            self._cancel_scheduled_one_hour_timer()
            self._scheduled_one_hour_timer = app.run_at(one_hour_before, nextalarm)

        return cb

    def _on_alarm_dismissed(self, callback: Callable) -> Callable[..., None]:
        app = self._app
        def cb(entity, attribute, old, new, **kwargs) -> None:
            app.log(f'alarm dismissed, executing callback {entity} ')
            callback()
        return cb

    def _cancel_scheduled_one_hour_timer(self):
        if self._scheduled_one_hour_timer:
            self._app.cancel_timer(self._scheduled_one_hour_timer, True)
        self._scheduled_one_hour_timer = None