from __future__ import annotations

import math
from typing import Set

from appdaemon.plugins.hass import hassapi as hass

import states
from entities import Entity


class BlindsHandler:
    def __init__(self, app: hass.Hass) -> None:
        self.app = app
        self._opening: Set[Entity] = set()

    def open_all(self) -> None:
        self.app.call_service("cover/open_cover",
                              entity_id="all")

    def close_all(self) -> None:
        self.app.call_service("cover/close_cover",
                              entity_id="all")

    def close(self, entity: Entity) -> None:
        if self.app.get_state(entity) != states.CLOSED:
            self.app.call_service("cover/close_cover",
                                  entity_id=entity)

    def open(self, entity: Entity) -> None:
        if self.app.get_state(entity) == states.CLOSED:
            self.app.call_service("cover/open_cover",
                                  entity_id=entity)

    def set(self, entity: Entity, open_percentage: int) -> None:
        if self.app.get_state(entity) == states.CLOSED:
            self.app.call_service("cover/set_cover_position",
                                  entity_id=entity, position=open_percentage)

    def open_for(self, entity: Entity, minutes: int = 0) -> None:
        if minutes == 0:
            self.open(entity)
            return

        if entity in self._opening:
            return

        total_steps = 20

        duration_step = math.ceil(minutes * 60 / total_steps)
        position_step = math.ceil(100 / total_steps)

        def increment_cover_position() -> None:
            self._opening.add(entity)
            current_position = self.app.get_state(entity, attribute="position")
            if current_position >= 100:
                self._opening.remove(entity)
                return

            self.set(entity, min(current_position + position_step, 100))
            self.app.run_in(lambda *_: increment_cover_position(), duration_step)

        increment_cover_position()
