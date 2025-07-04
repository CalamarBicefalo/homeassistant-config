from __future__ import annotations

from typing import Optional

from appdaemon.plugins.hass import hassapi as hass

import helpers
import states
from entities import Entity
from select_handler import SelectHandler
from selects import Mode
from state_handler import StateHandler
from temperature_handler import TemperatureHandler


class BlindsHandler:
    def __init__(self, app: hass.Hass, blinds: Optional[Entity], main_source_of_light: bool = False, window: Optional[Entity] = None) -> None:
        self.app = app
        self._blinds = blinds
        self._window = window
        self.state = StateHandler(app)
        self.temperature = TemperatureHandler(app)
        self.mode = SelectHandler[Mode](app, helpers.MODE)
        self.main_source_of_light = main_source_of_light

    def open_all(self) -> None:
        self.app.call_service("cover/open_cover",
                              entity_id="all")

    def close_all(self) -> None:
        self.app.call_service("cover/close_cover",
                              entity_id="all")

    def close(self) -> None:
        if self.is_open():
            self.app.call_service("cover/close_cover",
                                  entity_id=self._blinds)

    def open(self) -> None:
        if self.is_closed():
            self.app.call_service("cover/open_cover",
                                  entity_id=self._blinds)

    def best_for_temperature(self) -> None:
        if self.is_day():
            if self.temperature.should_cooldown():
                if self.main_source_of_light:
                    self.set_position(30)
                else:
                    self.close()
            else:
                self.open()
        else:
            if self.window_is_open() and self.temperature.should_cooldown():
                self.open()
            self.close()

    def is_day(self):
        return self.app.sunset() < self.app.sunrise()

    def set_position(self, open_percentage: int | float) -> None:
        self.app.call_service("cover/set_cover_position",
                              entity_id=self._blinds, position=open_percentage)

    def get_position(self) -> float:
        position: float = self.state.get_attr_as_number(self._blinds, "current_position")
        return position

    def is_closed(self) -> bool:
        return self.get_position() <= 0

    def is_open(self) -> bool:
        return self.get_position() >= 1

    def window_is_open(self):
        return self._window and self.state.is_value(self._window, states.OPEN)
