from abc import abstractmethod
from typing import Optional, List

import activities
import entities
from app import App
from select_handler import SelectHandler


class MotionController(App):

    def initialize(self) -> None:
        self.log(f'Initializing {self.controller} motion based activity controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [self.motion_sensor]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs):
        self.log(f'Triggering {self.controller} motion based activity controller {entity} -> {attribute} old={old} new={new}',
                 level="DEBUG")

        self.handle_presence()

    def handle_presence(self) -> None:
        if self.is_on(self.motion_sensor):
            self.activity.set(activities.Common.PRESENT)
        else:
            self.activity.set(activities.Common.EMPTY)

    @property
    def controller(self) -> str:
        return self.__class__.__name__

    @property
    @abstractmethod
    def motion_sensor(self) ->entities.Entity:
        pass


    @property
    @abstractmethod
    def activity(self) -> SelectHandler:
        pass
