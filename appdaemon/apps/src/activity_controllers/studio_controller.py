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
            [
                self.motion_sensor,
                entities.BINARY_SENSOR_DESK_CHAIR_PS,
                entities.SENSOR_DRUMKIT_ACTIVE_POWER,
                entities.BINARY_SENSOR_SNYK_LAPTOP_AUDIO_INPUT_IN_USE
            ]
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(
            f'Triggering studio activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if entity == entities.SENSOR_DRUMKIT_ACTIVE_POWER:
            if abs(self.to_float(old, entity) - self.to_float(new, entity)) < 3:
                return

        self.cancel_empty_timer()

        # Work handling
        if self.laptop_at_home() and (self.sitting_at_desk() or self.standing_at_desk()):
            self.set_working_or_meeting()

        # Drum handling
        elif self.is_consuming_at_least(entities.SENSOR_DRUMKIT_ACTIVE_POWER, watts=4):
            self.activity.set(Studio.Activity.DRUMMING)

        # Presence
        elif self.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(seconds=10)

    def standing_at_desk(self) -> bool:
        return self.is_working_or_meeting() and self.is_on(entities.BINARY_SENSOR_SNYK_LAPTOP_ACTIVE)

    def sitting_at_desk(self) -> bool:
        return self.is_on(entities.BINARY_SENSOR_DESK_CHAIR_PS)

    def laptop_at_home(self) -> bool:
        return self.has_state(entities.DEVICE_TRACKER_SNYK_LAPTOP, 'home')

    def set_working_or_meeting(self) -> None:
        if self.is_on(entities.BINARY_SENSOR_SNYK_LAPTOP_AUDIO_INPUT_IN_USE):
            self.activity.set(Studio.Activity.MEETING)
        else:
            self.activity.set(Studio.Activity.WORKING)

    def is_working_or_meeting(self) -> bool:
        working: bool = self.activity.is_value(Studio.Activity.WORKING)
        meeting: bool = self.activity.is_value(Studio.Activity.MEETING)
        return working or meeting
