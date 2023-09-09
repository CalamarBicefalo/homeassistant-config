from __future__ import annotations

from typing import Optional

from appdaemon.plugins.hass import hassapi as hass

import entities
from entities import Entity


class BlindsHandler:
    def __init__(self, app: hass.Hass, blinds: Optional[Entity]) -> None:
        self.app = app
        self._blinds = blinds

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
        temperature: int = self.app.get_state(entities.SENSOR_AIR_QUALITY_TEMPERATURE)
        if temperature > 22:
            self.close()
        else:
            self.open()

    def set_position(self, open_percentage: int) -> None:
        self.app.call_service("cover/set_cover_position",
                              entity_id=self._blinds, position=open_percentage)

    def get_position(self) -> int:
        position: int = self.app.get_state(self._blinds, attribute="current_position")
        return position

    def is_closed(self) -> bool:
        return self.get_position() == 0

    def is_open(self) -> bool:
        return self.get_position() == 100

