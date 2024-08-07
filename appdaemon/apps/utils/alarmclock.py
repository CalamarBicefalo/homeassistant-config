from __future__ import annotations

from enum import StrEnum
from typing import Any, Callable

from appdaemon.plugins.hass import hassapi as hass

# MQTT event encapsulating all Sleep as Android events
SLEEP_AS_ANDROID_EVENT = "SleepAsAndroid_phone"


# Enabled Sleep As Android events (they can be enabled in the app)
class Event(StrEnum):
    ALARM_DISMISSED = 'alarm_alert_dismiss'
    ONE_HOUR_BEFORE_ALARM = 'before_alarm'


class AlarmClock:

    def __init__(self, app: hass.Hass):
        self._app = app

    def listen(self, callback: Callable, event: Event) -> None:
        self._app.listen_event(self._on_event(event, callback), SLEEP_AS_ANDROID_EVENT)


    def _on_event(self, event: Event, callback: Callable) -> Callable[[Any, str, Any, Any], None]:
        def on_specified_event(event_name: str, data: Any, kwargs: Any) -> None:
            self._app.log(f'received alarm clock event {data["event"]} ',
                level="INFO")
            if data['event'] == event: callback()

        return on_specified_event
