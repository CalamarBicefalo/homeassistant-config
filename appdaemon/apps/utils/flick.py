from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Set

import entities
import helpers
import services
from app import App
from entities import Entity


class FlickHandler:
    def __init__(self, app: App) -> None:
        self.app = app
        self._opening: Set[Entity] = set()

    def clean_flat(self) -> None:
        self.app.call_service(
            services.VACUUM_START,
            entity_id=entities.VACUUM_FLICK,
        )
        self.app.set_helper_to_now(helpers.LAST_CLEANED_FLAT)

    def clean_room(self, room: Room) -> None:
        self.app.call_service(
            services.VACUUM_SEND_COMMAND,
            entity_id=entities.VACUUM_FLICK,
            command="app_segment_clean",
            params=room.value,
        )
        match room:
            case Room.kitchen:
                self.app.set_helper_to_now(helpers.LAST_CLEANED_KITCHEN)

    def go_to_maintenance_spot(self) -> None:
        self.app.call_service(
            services.VACUUM_SEND_COMMAND,
            entity_id=entities.VACUUM_FLICK,
            command="app_goto_target",
            params=[mop_maintenance.x, mop_maintenance.y]
        )
        self.app.set_helper_to_now(helpers.LAST_CLEANED_VACUUM_MOP)

    def last_cleaned_flat(self) -> datetime:
        return self.app.helper_to_datetime(helpers.LAST_CLEANED_FLAT)

    def last_cleaned_kitchen(self) -> datetime:
        return self.app.helper_to_datetime(helpers.LAST_CLEANED_KITCHEN)

    def last_maintenance(self) -> datetime:
        return self.app.helper_to_datetime(helpers.LAST_CLEANED_VACUUM_MOP)


class Room(Enum):
    kitchen = 16
    living_room = 24
    dining_room = 17
    hallway = 20
    bedroom = 21
    ensuite = 22
    storage_room = 19
    bathroom = 18
    office = 23


class Point:
    def __init__(self, x_init: int, y_init: int) -> None:
        self.x = x_init
        self.y = y_init

    def __repr__(self) -> str:
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


mop_maintenance = Point(24900, 22200)
