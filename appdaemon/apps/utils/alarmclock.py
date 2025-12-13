from __future__ import annotations

from datetime import timedelta
from enum import StrEnum
from typing import Any, Callable

from appdaemon.plugins.hass import hassapi as hass

import entities
from state_handler import StateHandler

# MQTT event encapsulating all Sleep as Android events
SLEEP_AS_ANDROID_EVENT = "SleepAsAndroid_phone"


# Enabled Sleep As Android events (they can be enabled in the app)
class Event(StrEnum):
    ONE_HOUR_BEFORE_ALARM = 'before_alarm'


class AlarmClock:

    def __init__(self, app: hass.Hass):
        self._app = app
        self.state = StateHandler(app)

    def listen(self, callback: Callable, event: Event) -> None:
        self._app.listen_event(self._on_event(event, callback), SLEEP_AS_ANDROID_EVENT)
        self._app.listen_state(self._on_alarm_time_change(callback), entities.INPUT_DATETIME_NEXT_IOS_ALARM)


    def _on_event(self, event: Event, callback: Callable) -> Callable[[Any, str, Any, Any], None]:
        def on_specified_event(event_name: str, data: Any, kwargs: Any) -> None:
            self._app.log(f'received alarm clock event {data["event"]} ',
                level="INFO")
            if data['event'] == event: callback()

        return on_specified_event

    def _on_alarm_time_change(self, callback: Callable) -> Callable[[Any, str, Any, Any], None]:
        app = self._app
        state = self.state

        def cb(entity, attribute, old, new, kwargs) -> None:
            app.log(f'alarm time changed, scheduling callback {entity} ')
            nextalarm = state.get_as_datetime(entities.INPUT_DATETIME_NEXT_IOS_ALARM) - timedelta(hours=1)
            def one_hour_before(event_name: str, data: Any, kwargs: Any) -> None:
                app.log(f'triggering callback 1 hour before alarm {entity} ')
                callback()

            app.run_at(one_hour_before, nextalarm)

        return cb