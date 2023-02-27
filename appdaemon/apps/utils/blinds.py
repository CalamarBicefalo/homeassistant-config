from __future__ import annotations

from appdaemon.plugins.hass import hassapi as hass

import states
from entities import Entity


class BlindsHandler:
    def __init__(self, app: hass.Hass) -> None:
        self.app = app

    def open_all(self) -> None:
        self.app.call_service("cover/open_cover",
                              entity_id="all")

    def close_all(self) -> None:
        self.app.call_service("cover/close_cover",
                              entity_id="all")

    def close(self, entity: Entity) -> None:
        if self.app.get_state(entity) == states.OPEN:
            self.app.call_service("cover/close_cover",
                                  entity_id=entity)

    def open(self, entity: Entity) -> None:
        if self.app.get_state(entity) == states.CLOSED:
            self.app.call_service("cover/open_cover",
                                  entity_id=entity)
