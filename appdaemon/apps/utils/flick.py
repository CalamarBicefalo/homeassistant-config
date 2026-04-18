from __future__ import annotations

from collections import deque
from datetime import datetime
from threading import Lock
from typing import Any, ClassVar, Deque, Optional, Set

from appdaemon.plugins.hass import hassapi as hass

import entities
import helpers
import services
from entities import Entity
from state_handler import StateHandler

MAX_ROOMS_CLEANED_BEFORE_MAINTENANCE = 10

class FlickHandler:
    _room_queue: ClassVar[Deque[int]] = deque()
    _queue_lock: ClassVar[Lock] = Lock()
    _status_listener_apps: ClassVar[Set[int]] = set()
    _cleaning_in_progress: ClassVar[bool] = False

    _IN_PROGRESS_STATUSES: ClassVar[Set[str]] = {"segment_cleaning", "cleaning"}
    _READY_FOR_NEXT_ROOM_STATUSES: ClassVar[Set[str]] = {"returning_home", "charging"}

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
        current_count = self.state.get_as_number(entities.INPUT_NUMBER_ROOMS_CLEANED_SINCE_LAST_MAINTENANCE)
        self.app.call_service(
            services.INPUT_NUMBER_SET_VALUE,
            entity_id=entities.INPUT_NUMBER_ROOMS_CLEANED_SINCE_LAST_MAINTENANCE,
            value=current_count+10,
        )

    def clean_room(self, room: int) -> None:
        self._ensure_status_listener()
        with FlickHandler._queue_lock:
            FlickHandler._room_queue.append(room)
            self.app.log(f'Room {room} added to queue. Queue now: {list(FlickHandler._room_queue)}', level="INFO")
        self._try_clean_next_room()

    def _ensure_status_listener(self) -> None:
        app_id = id(self.app)
        with FlickHandler._queue_lock:
            if app_id in FlickHandler._status_listener_apps:
                return

            FlickHandler._status_listener_apps.add(app_id)
            status = self._get_flick_status()
            FlickHandler._cleaning_in_progress = status in FlickHandler._IN_PROGRESS_STATUSES

        self.app.listen_state(
            self._on_flick_status_change,
            entities.SENSOR_FLICK_STATUS,
        )

    def _on_flick_status_change(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if not new:
            return

        self.app.log(f'Flick status changed: {old} -> {new}. Queue: {list(FlickHandler._room_queue)}', level="INFO")

        if new in FlickHandler._IN_PROGRESS_STATUSES:
            with FlickHandler._queue_lock:
                FlickHandler._cleaning_in_progress = True
            return

        if new in FlickHandler._READY_FOR_NEXT_ROOM_STATUSES:
            with FlickHandler._queue_lock:
                FlickHandler._cleaning_in_progress = False
            self._try_clean_next_room()

    def _try_clean_next_room(self) -> None:
        next_room: int | None = None

        with FlickHandler._queue_lock:
            if FlickHandler._cleaning_in_progress:
                self.app.log(f'Cleaning already in progress, queued room will wait. Queue: {list(FlickHandler._room_queue)}', level="INFO")
                return

            status = self._get_flick_status()
            if status in FlickHandler._IN_PROGRESS_STATUSES:
                FlickHandler._cleaning_in_progress = True
                self.app.log(f'Vacuum busy (status={status}), not starting next room. Queue: {list(FlickHandler._room_queue)}', level="INFO")
                return

            if not FlickHandler._room_queue:
                self.app.log('Queue empty, nothing to clean', level="DEBUG")
                return

            next_room = FlickHandler._room_queue.popleft()
            FlickHandler._cleaning_in_progress = True
            self.app.log(f'Starting to clean room {next_room}. Remaining queue: {list(FlickHandler._room_queue)}', level="INFO")

        self.app.call_service(
            services.VACUUM_SEND_COMMAND,
            entity_id=entities.VACUUM_FLICK,
            command="app_segment_clean",
            params=[next_room],
        )
        self.app.call_service(
            services.INPUT_NUMBER_INCREMENT,
            entity_id=entities.INPUT_NUMBER_ROOMS_CLEANED_SINCE_LAST_MAINTENANCE
        )

    def _get_flick_status(self) -> Optional[str]:
        try:
            return self.state.get_as_str(entities.SENSOR_FLICK_STATUS)
        except Exception:
            return None

    def go_to_maintenance_spot(self) -> None:
        self.app.call_service(
            services.VACUUM_SEND_COMMAND,
            entity_id=entities.VACUUM_FLICK,
            command="app_goto_target",
            params=[mop_maintenance.x, mop_maintenance.y]
        )
        self._set_helper_to_now(helpers.LAST_CLEANED_VACUUM_MOP)
        self.app.call_service(
            services.INPUT_NUMBER_SET_VALUE,
            entity_id=entities.INPUT_NUMBER_ROOMS_CLEANED_SINCE_LAST_MAINTENANCE,
            value=0,
        )

    def last_cleaned_flat(self) -> datetime:
        return self.state.get_as_datetime(helpers.LAST_CLEANED_FLAT)

    def last_maintenance(self) -> datetime:
        return self.state.get_as_datetime(helpers.LAST_CLEANED_VACUUM_MOP)

    def needs_maintenance(self) -> bool:
        current_count = self.state.get_as_number(entities.INPUT_NUMBER_ROOMS_CLEANED_SINCE_LAST_MAINTENANCE)
        return current_count > MAX_ROOMS_CLEANED_BEFORE_MAINTENANCE

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


mop_maintenance = Point(22200, 26400)
