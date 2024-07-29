
from enum import StrEnum
from typing import TypeVar, Generic

import appdaemon.plugins.hass.hassapi as hass

import services
from helpers import Helper
from state_handler import StateHandler

T = TypeVar("T", bound=StrEnum)


class SelectHandler(Generic[T]):

    def __init__(self, app: hass.Hass, helper: Helper | str):
        self._helper = helper
        self._app = app
        self.state = StateHandler(app)

    def set(self, value: T | str) -> None:
        self._app.log("Setting select " + value, level="DEBUG")
        self._app.call_service(
            services.INPUT_SELECT_SELECT_OPTION,
            entity_id=self._helper,
            option=value
        )

    def is_value(self, value: T | str) -> bool:
        return self.state.is_value(self._helper, value)

    def get(self) -> T:
        return self.state.get_as_str(self._helper)  # type: ignore
