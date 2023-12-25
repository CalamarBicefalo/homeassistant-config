from abc import abstractmethod
from datetime import datetime, timedelta, time
from typing import Optional, Any

import helpers
import services
from flick import FlickHandler
from modes import Mode
from select_handler import SelectHandler
from state_handler import StateHandler

EMPTY = "Empty"


class Room():
    adjacent_rooms: list['Room'] = []
    open_floor_rooms: list['Room'] = []

    def __init__(self, app) -> None:  # type: ignore
        self.app = app
        self.flick = FlickHandler(app)
        self.state = StateHandler(app)

    def initialize(self) -> None:
        if self.days_between_cleaning <= 0:
            self.app.log(f'Cleaning disabled for {self.name}.', level="INFO")
            return

        self.app.log(f'Initializing {self.name} clean check hourly.', level="INFO")
        self.app.run_hourly(
            lambda *_: self.clean_if_needed(),
            time(0, 0, 0)
        )
        rooms_ = [self._activity_helper, *map(lambda room: room._activity_helper, self.open_floor_rooms)]
        self.app.listen_state(
            lambda *_: self.clean_if_needed(),
            rooms_,
            new="Empty"
        )

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def days_between_cleaning(self) -> int:
        pass

    @property
    @abstractmethod
    def _last_cleaned_helper(self) -> helpers.Helper:
        pass

    @property
    @abstractmethod
    def _activity_helper(self) -> helpers.Helper:
        pass

    @abstractmethod
    def get_activity(self) -> SelectHandler:
        pass

    @property
    def _room_cleaner_segment(self) -> Optional[int]:
        return None

    def clean_if_needed(self) -> None:
        if self._needs_cleaning() and self._cleaning_is_allowed():
            self.clean()

    def is_empty(self) -> bool:
        empty: bool = self.get_activity().is_value(EMPTY)
        return empty

    def are_all_open_floor_rooms_empty(self) -> bool:
        return all(map(lambda room: room.is_empty(), self.open_floor_rooms))

    def last_cleaned(self) -> datetime:
        last_cleaned: datetime | None = self.state.get_as_datetime(self._last_cleaned_helper)
        if not last_cleaned:
            self.app.log(f'Last cleaned not set for {self._last_cleaned_helper}, returning default value',
                         level="WARNING")
            return datetime.fromisoformat('1970-01-01')
        return last_cleaned

    def clean(self) -> None:
        if self._room_cleaner_segment is None:
            self.app.log(f'Room cleaner segment not set for {self.name}, skipping cleaning', level="WARNING")
            return
        self.app.log(f'Cleaning {self.name}', level="INFO")
        self.flick.clean_room(self._room_cleaner_segment)
        self._set_helper_to_now(self._last_cleaned_helper)

    def _needs_cleaning(self) -> bool:
        needs_cleaning = self.last_cleaned() < datetime.now() - timedelta(days=self.days_between_cleaning)
        if not needs_cleaning:
            self.app.log(
                f'{self.name} does not need cleaning. last_cleaned={self.last_cleaned()} days_between_cleaning={self.days_between_cleaning}',
                level="INFO")
        return needs_cleaning

    def _cleaning_is_allowed(self) -> bool:
        return self.is_empty() and self.are_all_open_floor_rooms_empty() and not self.app.handlers.mode.is_value(Mode.SLEEPING)

    def _set_helper_to_now(self, helper: helpers.Helper) -> None:
        self.app.call_service(
            services.INPUT_DATETIME_SET_DATETIME,
            entity_id=helper,
            datetime=helpers.datetime_to_helper(datetime.now())
        )
