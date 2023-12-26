
from enum import StrEnum
from typing import TypeVar

import appdaemon.plugins.hass.hassapi as hass

from helpers import Helper
from select_handler import SelectHandler

T = TypeVar("T", bound=StrEnum)
ACTIVITY_CHANGED_EVENT = "activity_changed"


class ActivityHandler(SelectHandler[T]):

    def __init__(self, app: hass.Hass, helper: Helper | str):
        super().__init__(app, helper)
        self._helper = helper
        self._app = app

    def set(self, value: T | str) -> None:
        self._app.fire_event(ACTIVITY_CHANGED_EVENT, helper=self._helper, activity=value, manual=False)
        super().set(value)


