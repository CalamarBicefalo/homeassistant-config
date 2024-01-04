from enum import StrEnum
from typing import TypeVar, Any

import appdaemon.plugins.hass.hassapi as hass

from helpers import Helper
from select_handler import SelectHandler
from state_handler import StateHandler

T = TypeVar("T", bound=StrEnum)
ACTIVITY_CHANGED_EVENT = "activity_changed"


class ActivityHandler(SelectHandler[T]):

    def __init__(self, app: hass.Hass, activity_helper: Helper | str, activity_lock: Helper | str):
        super().__init__(app, activity_helper)
        self._helper = activity_helper
        self._lock = activity_lock
        self._app = app
        self._state = StateHandler(app)

    def set(self, value: T | str, manual: bool = False) -> None:
        if not self.is_locked() or manual:
            super().set(value)

    def is_locked(self):
        return self.state.is_on(self._lock)

    def lock(self):
        return self._app.turn_on(self._lock)

    def on_activity_changed_event(self, event_name: str, data: Any, kwargs: Any) -> None:
        if event_name != ACTIVITY_CHANGED_EVENT:
            self._app.log(f'Got event of type {event_name} when expecting {ACTIVITY_CHANGED_EVENT}', level="ERROR")
            return
        if not data or not data['helper']:
            self._app.log(f'Got event of type {event_name} missing mandatory attribute "helper" with the activity helper name', level="ERROR")
            return
        if not data['activity']:
            self._app.log(f'Got event of type {event_name} missing mandatory attribute "activity" with the activity value', level="ERROR")
            return
        if not data['manual']:
            self._app.log(f'Got event of type {event_name} missing mandatory attribute "manual" indicating if it is a user generated action', level="ERROR")
            return

        if data['helper'] == self._helper:
            if data['manual']:
                self.lock()
            self.set(data['activity'], manual=data['manual'])
