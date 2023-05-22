from __future__ import annotations

from typing import Optional

from appdaemon.plugins.hass import hassapi as hass

import states
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
        if self.app.get_state(self._blinds) != states.CLOSED:
            self.app.call_service("cover/close_cover",
                                  entity_id=self._blinds)

    def open(self) -> None:
        if self.app.get_state(self._blinds) == states.CLOSED:
            self.app.call_service("cover/open_cover",
                                  entity_id=self._blinds)

    def set_position(self, open_percentage: int) -> None:
        if self.app.get_state(self._blinds) == states.CLOSED:
            self.app.call_service("cover/set_cover_position",
                                  entity_id=self._blinds, position=open_percentage)

    def get_position(self) -> int:
        position: int = self.app.get_state(self._blinds, attribute="current_position")
        return position

