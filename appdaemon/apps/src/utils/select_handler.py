from enum import StrEnum
from typing import TypeVar, Generic

from utils.app import App

import services
from helpers import Helper

T = TypeVar("T", bound=StrEnum)


class SelectHandler(Generic[T]):

    def __init__(self, app: App, helper: Helper):
        self._helper = helper
        self._app = app

    def set(self, value: T) -> None:
        self._app.log("Setting select " + value, level="DEBUG")
        self._app.call_service(
            services.INPUT_SELECT_SELECT_OPTION,
            entity_id=self._helper,
            option=value
        )

    def is_value(self, value: T) -> bool:
        return self._app.has_state(self._helper, value)

    def get(self) -> T:
        return StrEnum(self._app.get_state(self._helper))  # type: ignore
