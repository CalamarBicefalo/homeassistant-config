from abc import abstractmethod

import activities
import entities
import states
from app import App
from handlers.select_handler import SelectHandler


class ActivityController(App):
    _empty_timer = None

    def set_as_empty_in(self, seconds: int = 0, minutes: int = 0) -> None:
        countdown = seconds + (minutes * 60)
        if self._empty_timer:
            self.cancel_timer(self._empty_timer)
        self._empty_timer = self.run_in(lambda *_: self.activity.set(activities.Common.EMPTY), countdown)

    def cancel_empty_timer(self) -> None:
        if self._empty_timer:
            self.cancel_timer(self._empty_timer)
        self._empty_timer = self.run_in(lambda *_: self.activity.set(activities.Common.EMPTY), 3 * 60 * 60)

    @property
    @abstractmethod
    def activity(self) -> SelectHandler:
        pass


class MotionController(ActivityController):

    def initialize(self) -> None:
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
            self.activity.set(activities.Common.PRESENT)
        else:
            self.set_as_empty_in(self.cooldown_seconds)

    @property
    def controller(self) -> str:
        return self.__class__.__name__

    @property
    @abstractmethod
    def motion_sensor(self) -> entities.Entity:
        pass

    @property
    def cooldown_seconds(self) -> int:
        return 1

    @property
    @abstractmethod
    def activity(self) -> SelectHandler:
        pass

    def ignore_motion_trigger(self) -> bool:
        return False
