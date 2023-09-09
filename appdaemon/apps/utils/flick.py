from __future__ import annotations

from datetime import datetime
from typing import Set

from appdaemon.plugins.hass import hassapi as hass

import entities
import helpers
import services
from entities import Entity
from state_handler import StateHandler


class FlickHandler:
    def __init__(self, app: hass) -> None:
        self.app = app
        self._opening: Set[Entity] = set()
        self.state = StateHandler(app)

    def clean_flat(self) -> None:
        self.app.call_service(
            services.VACUUM_START,
            entity_id=entities.VACUUM_FLICK,
        )
        self._set_helper_to_now(helpers.LAST_CLEANED_FLAT)

    def clean_room(self, room: int) -> None:
        self.app.call_service(
            services.VACUUM_SEND_COMMAND,
            entity_id=entities.VACUUM_FLICK,
            command="app_segment_clean",
            params=room,
        )

    def go_to_maintenance_spot(self) -> None:
        self.app.call_service(
            services.VACUUM_SEND_COMMAND,
            entity_id=entities.VACUUM_FLICK,
            command="app_goto_target",
            params=[mop_maintenance.x, mop_maintenance.y]
        )
        self._set_helper_to_now(helpers.LAST_CLEANED_VACUUM_MOP)

    def last_cleaned_flat(self) -> datetime:
        return self.state.get_as_datetime(helpers.LAST_CLEANED_FLAT)

    def last_maintenance(self) -> datetime:
        return self.state.get_as_datetime(helpers.LAST_CLEANED_VACUUM_MOP)

    def _set_helper_to_now(self, helper: helpers.Helper) -> None:
        self.app.call_service(
            services.INPUT_DATETIME_SET_DATETIME,
            entity_id=helper,
            datetime=helpers.datetime_to_helper(datetime.now())
        )


class Point:
    def __init__(self, x_init: int, y_init: int) -> None:
        self.x = x_init
        self.y = y_init

    def __repr__(self) -> str:
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


mop_maintenance = Point(24900, 22200)
