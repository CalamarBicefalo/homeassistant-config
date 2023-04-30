from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Optional

import appdaemon.plugins.hass.hassapi as hass

import flick
import helpers
import services


class Room:

    def __init__(self, app: hass.Hass) -> None:
        self.app = app
        self.flick = flick.FlickHandler(app)

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def _last_cleaned_helper(self) -> helpers.Helper:
        pass

    @property
    @abstractmethod
    def _activity_helper(self) -> helpers.Helper:
        pass

    @property
    def _room_cleaner_segment(self) -> Optional[int]:
        return None

    @property
    def _days_between_cleaning(self) -> int:
        return 4

    def last_cleaned(self) -> datetime:
        return helpers.helper_to_datetime(self.app.get_state(self._last_cleaned_helper))

    def clean(self) -> None:
        if self._room_cleaner_segment is None:
            self.app.log(f'Room cleaner segment not set for {self.name}, skipping cleaning', level="WARNING")
            return
        self.flick.clean_room(self._room_cleaner_segment)
        self._set_helper_to_now(self._last_cleaned_helper)

    def needs_cleaning(self) -> bool:
        return self.last_cleaned() < datetime.now() - timedelta(days=self._days_between_cleaning)

    def _set_helper_to_now(self, helper: helpers.Helper) -> None:
        self.app.call_service(
            services.INPUT_DATETIME_SET_DATETIME,
            entity_id=helper,
            datetime=helpers.datetime_to_helper(datetime.now())
        )

