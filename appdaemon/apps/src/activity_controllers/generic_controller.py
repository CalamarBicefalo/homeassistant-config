from abc import abstractmethod
from typing import Optional

import entities
import states
from activity_handler import ActivityHandler, ACTIVITY_CHANGED_EVENT
from app import App
from rooms import *
from select_handler import SelectHandler

# The maximum amount of time that a room can stay in a given activity without changes before setting as EMPTY (regardless of sensor)
MAX_SECONDS_UNTIL_EMPTY = 3 * 60 * 60
# The maximum amount of time motion sensor can report empty room before setting EMPTY as an activity
MAX_SECONDS_WITHOUT_PRESENCE_UNTIL_EMPTY = 10 * 60


class ActivityController(App):
    _empty_timer = None

    @property
    def controller(self) -> str:
        return self.__class__.__name__

    @property
    @abstractmethod
    def motion_sensor(self) -> entities.Entity:
        pass

    def initialize_lock(self) -> None:
        self.log(f'Initializing {self.controller} activity controller.', level="DEBUG")

        if self.motion_sensor:
            self.listen_event(
                self.activity.on_activity_changed_event,
                ACTIVITY_CHANGED_EVENT
            )

    def set_as_empty_in(self, seconds: int = 0, minutes: int = 0) -> None:
        self._cancel_empty_timer()
        self._run_empty_timer_in(seconds=seconds + (minutes * 60))

    def cancel_empty_timer(self) -> None:
        """
        Cancels any running timer and ensures room gets to EMPTY state after the cooldown period
        """
        self._cancel_empty_timer()
        # Ensures every room eventually converges to the EMPTY state
        if not self.motion_sensor:
            self._run_empty_timer_in(self.max_seconds_without_presence_until_empty, warn_log=f'Setting {self.controller} to empty after {self.max_seconds_without_presence_until_empty} seconds because there is no motion sensor configured')

        elif self.state.is_off(self.motion_sensor):
            self._run_empty_timer_in(self.max_seconds_without_presence_until_empty, warn_log=f'Setting {self.controller} to empty because the motion sensor {self.motion_sensor} has been off for {self.max_seconds_without_presence_until_empty} seconds')

        else:
            self._run_empty_timer_in(self.max_seconds_until_empty, warn_log=f'Setting {self.controller} to empty because there has been no activity for {self.max_seconds_until_empty} seconds')

    def _cancel_empty_timer(self) -> None:
        if self._empty_timer and hasattr(self, 'AD') and self.timer_running(self._empty_timer):
            self.cancel_timer(self._empty_timer)

    def _run_empty_timer_in(self, seconds: int, warn_log: Optional[str] = None) -> None:
        def callback() -> None:
            if warn_log:
                self.log(warn_log, level="WARNING")
            self.activity.set(CommonActivities.EMPTY)
            self._empty_timer = None

        self._empty_timer = self.run_in(lambda *_: callback(), seconds)

    @property
    @abstractmethod
    def activity(self) -> ActivityHandler:
        pass

    @property
    def max_seconds_until_empty(self) -> int:
        return MAX_SECONDS_UNTIL_EMPTY

    @property
    def max_seconds_without_presence_until_empty(self) -> int:
        return MAX_SECONDS_WITHOUT_PRESENCE_UNTIL_EMPTY


class MotionController(ActivityController):

    def initialize(self) -> None:
        super().initialize_lock()
        self.log(f'Initializing {self.controller} motion based activity controller.', level="DEBUG")

        if self.motion_sensor:
            self.listen_state(
                self.controller_handler,
                [self.motion_sensor]
            )

    def controller_handler(self, entity, attribute, old, new, kwargs):  # type: ignore
        self.log(
            f'Triggering {self.controller} motion based activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        if self.ignore_motion_trigger():
            return

        if new == states.DETECTED:
            self.activity.set(CommonActivities.PRESENT)
        else:
            self.set_as_empty_in(self.cooldown_seconds)

    @property
    def cooldown_seconds(self) -> int:
        return 1

    @property
    @abstractmethod
    def activity(self) -> SelectHandler:
        pass

    def ignore_motion_trigger(self) -> bool:
        return False
