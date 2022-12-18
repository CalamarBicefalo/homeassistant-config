from abc import abstractmethod

import activities
import entities
import states
from app import App
from select_handler import SelectHandler


class MotionController(App):
    away_timer = None
    def initialize(self) -> None:
        self.log(f'Initializing {self.controller} motion based activity controller.', level="DEBUG")

        if self.motion_sensor:
            self.listen_state(
                self.controller_handler,
                [self.motion_sensor]
            )

    def controller_handler(self, entity, attribute, old, new, kwargs):  # type: ignore
        self.log(f'Triggering {self.controller} motion based activity controller {entity} -> {attribute} old={old} new={new}',
                 level="DEBUG")

        if self.away_timer:
            self.cancel_timer(self.away_timer)
        self.away_timer = self.run_in(lambda *_: self.activity.set(activities.Common.EMPTY), self.cooldown_minutes * 60)

        if new == states.DETECTED:
            self.activity.set(activities.Common.PRESENT)


    @property
    def controller(self) -> str:
        return self.__class__.__name__

    @property
    @abstractmethod
    def motion_sensor(self) -> entities.Entity:
        pass

    @property
    def cooldown_minutes(self) -> int:
        return 1


    @property
    @abstractmethod
    def activity(self) -> SelectHandler:
        pass
