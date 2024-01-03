from enum import StrEnum
from typing import TypeVar

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
        self._app.fire_event(ACTIVITY_CHANGED_EVENT, helper=self._helper, activity=value, manual=manual)
        super().set(value)

    def is_locked(self):
        return self.state.is_on(self._lock)

    def lock(self):
        return self._app.turn_on(self._lock)
