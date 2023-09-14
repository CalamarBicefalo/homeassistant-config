from __future__ import annotations

from typing import Optional

from appdaemon.plugins.hass import hassapi as hass

import entities
import helpers
from modes import Mode
from select_handler import SelectHandler
from state_handler import StateHandler
from entities import Entity

COMFORT_TEMPERATURE = 22

class BlindsHandler:
    def __init__(self, app: hass.Hass, blinds: Optional[Entity], room_with_plants: bool = False) -> None:
        self.app = app
        self._blinds = blinds
        self.state = StateHandler(app)
        self.mode = SelectHandler[Mode](app, helpers.HOMEASSISTANT_MODE)
        self.room_with_plants = room_with_plants

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
        temperature = self.state.get_as_number(entities.SENSOR_AIR_QUALITY_TEMPERATURE)
        if self.mode.is_value(Mode.DAY) and temperature > COMFORT_TEMPERATURE:
            if self.room_with_plants:
                self.set_position(30)
            else:
                self.close()
        elif self.mode.is_value(Mode.DAY) and temperature < COMFORT_TEMPERATURE:
            self.open()
        elif temperature > COMFORT_TEMPERATURE:
            self.open()
        else:
            self.close()

    def set_position(self, open_percentage: int) -> None:
        self.app.call_service("cover/set_cover_position",
                              entity_id=self._blinds, position=open_percentage)

    def get_position(self) -> float:
        position: float = self.state.get_attr_as_number(self._blinds, "current_position")
        return position

    def is_closed(self) -> bool:
        return self.get_position() <= 0

    def is_open(self) -> bool:
        return self.get_position() >= 100
