from typing import Any

import entities
from activity_controllers.generic_controller import ActivityController
from rooms import *
from select_handler import SelectHandler


class StudioController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_STUDIO_MOTION

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.studio.activity

    def initialize(self) -> None:
        self.log(f'Initializing studio activity controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [self.motion_sensor, entities.BINARY_SENSOR_DESK_CHAIR_PS, entities.SENSOR_DRUMKIT_ACTIVE_POWER]
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(
            f'Triggering studio activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if entity == entities.SENSOR_DRUMKIT_ACTIVE_POWER and abs(float(old) - float(new)) < 3:
            return

        self.cancel_empty_timer()

        # Work handling
        if self.is_on(entities.BINARY_SENSOR_DESK_CHAIR_PS):
            self.activity.set(Studio.Activity.WORKING)

        # Drum handling
        elif self.is_consuming_at_least(entities.SENSOR_DRUMKIT_ACTIVE_POWER, watts=4):
            self.activity.set(Studio.Activity.DRUMMING)

        # Presence
        elif self.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(seconds=10)
