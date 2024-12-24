from typing import Any

import entities
from activity_controllers.generic_controller import ActivityController
from rooms import *


class OfficeController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_OFFICE_MOTION

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.office.activity

    def initialize(self) -> None:
        super().initialize_lock()
        self.log(f'Initializing office activity controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [
                self.motion_sensor
            ]
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(
            f'Triggering office activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        # Presence
        if self.state.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(seconds=10)

