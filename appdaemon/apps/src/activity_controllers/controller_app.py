from abc import abstractmethod
from typing import Optional, List

import activities
import entities
from app import App


class ControllerApp(App):

    def initialize(self):
        self.log(f'Initializing {self.controller} activity controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [self.motion_sensor, *self.additional_triggers]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs):
        if not self.should_trigger(entity, attribute, old, new):
            self.log(f'Skipping {self.controller} activity controller because precondition was not met '
                     f'{entity} -> {attribute} old={old} new={new}',
                     level="DEBUG")
            return

        self.log(f'Triggering {self.controller} activity controller {entity} -> {attribute} old={old} new={new}',
                 level="DEBUG")

        custom_activity = self.get_custom_activity(entity, attribute, old, new)
        if custom_activity:
            self.set_activity(self.activity.helper, custom_activity)
            return

        # Presence handling
        if self.is_on(self.motion_sensor):
            self.set_activity(self.activity.helper, activities.RoomActivity.PRESENT)
        else:
            self.set_activity(self.activity.helper, activities.RoomActivity.EMPTY)

    def get_custom_activity(self, entity, attribute, old, new) -> Optional[activities.Activity]:
        return None

    @property
    def controller(self):
        return self.__class__.__name__

    @property
    @abstractmethod
    def motion_sensor(self) -> entities.Entity:
        pass

    def should_trigger(self, entity, attribute, old, new) -> bool:
        return True

    @property
    def additional_triggers(self) -> List[entities.Entity]:
        return []

    @property
    @abstractmethod
    def activity(self) -> activities.RoomActivity:
        pass