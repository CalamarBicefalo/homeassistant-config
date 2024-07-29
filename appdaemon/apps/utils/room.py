from abc import abstractmethod
from datetime import datetime, timedelta, time
from typing import Optional, Any

import helpers
import services
from flick import FlickHandler
from select_handler import SelectHandler
from selects import Mode
from state_handler import StateHandler

EMPTY = "Empty"
CLEAN_ROOM_EVENT = "clean_room_requested"


class Room():
    adjacent_rooms: list['Room'] = []
    open_floor_rooms: list['Room'] = []

    def __init__(self, app) -> None:  # type: ignore
        self.app = app
        self.mode = SelectHandler[Mode](app, helpers.MODE)
        self.flick = FlickHandler(app)
        self.state = StateHandler(app)

    def initialize(self) -> None:
        self._initialize_presence_journal()
        self._initialize_cleaning()

    def _initialize_presence_journal(self) -> None:
        self.app.listen_state(
            lambda *_: self._update_last_present(),
            self._activity_helper,
        )

    def _initialize_cleaning(self) -> None:
        self.app.listen_event(
            self.on_room_clean_requested,
            CLEAN_ROOM_EVENT
        )

        if self.days_between_cleaning <= 0:
            self.app.log(f'Cleaning disabled for {self.name}.', level="INFO")
        else:
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
    def clean_after(self) -> int:
        pass

    @property
    @abstractmethod
    def _last_cleaned_helper(self) -> helpers.Helper:
        pass

    @property
    @abstractmethod
    def _last_present_helper(self) -> helpers.Helper:
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
        return self.state.get_as_datetime_or_default(self._last_cleaned_helper, '1970-01-01')

    def last_present(self) -> datetime:
        return self.state.get_as_datetime_or_default(self._last_present_helper, '1970-01-01')

    def clean(self) -> None:
        if self._room_cleaner_segment is None:
            self.app.log(f'Room cleaner segment not set for {self.name}, skipping cleaning', level="WARNING")
            return
        self.app.log(f'Cleaning {self.name}', level="INFO")
        self.flick.clean_room(self._room_cleaner_segment)
        self._set_helper_to_now(self._last_cleaned_helper)

    def _needs_cleaning(self) -> bool:
        days_between_clean_elapsed = self.last_cleaned() < datetime.now() - timedelta(days=self.days_between_cleaning)
        present_after_cleaned = self.last_present() > self.last_cleaned()
        if not days_between_clean_elapsed:
            self.app.log(
                f'{self.name} does not need cleaning. last_cleaned={self.last_cleaned()} days_between_cleaning={self.days_between_cleaning}',
                level="DEBUG")
        return days_between_clean_elapsed and present_after_cleaned

    def _cleaning_is_allowed(self) -> bool:
        return (self.is_empty()
                and self.are_all_open_floor_rooms_empty()
                and not self.mode.is_value(Mode.SLEEPING)
                and datetime.now().hour >= self.clean_after
                )

    def _update_last_present(self) -> None:
        self._set_helper_to_now(self._last_present_helper)

    def _set_helper_to_now(self, helper: helpers.Helper) -> None:
        self.app.call_service(
            services.INPUT_DATETIME_SET_DATETIME,
            entity_id=helper,
            datetime=helpers.datetime_to_helper(datetime.now())
        )

    def on_room_clean_requested(self, event_name: str, data: Any, kwargs: Any) -> None:
        self.app.log(f'Got event {event_name} with data {data}', level="DEBUG")
        if event_name != CLEAN_ROOM_EVENT:
            self.app.log(f'Got event of type {event_name} when expecting {CLEAN_ROOM_EVENT}', level="ERROR")
            return
        if not data or not data['helper']:
            self.app.log(f'Got event of type {event_name} missing mandatory attribute "helper" with the activity helper name', level="ERROR")
            return

        if data['helper'] == self._activity_helper:
            self.app.log(f'Cleaning {self.name} because of {event_name} event', level="INFO")
            self.clean()
