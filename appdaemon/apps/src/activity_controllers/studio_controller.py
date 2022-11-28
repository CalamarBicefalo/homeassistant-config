from typing import Any

import activities
import entities
from activity_controllers.controller_app import MotionController
from select_handler import SelectHandler


class StudioController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_STUDIO_MOTION

    @property
    def activity(self) -> SelectHandler:
        return self.activities.studio

    def initialize(self) -> None:
        self.log(f'Initializing {self.controller} motion based activity controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [self.motion_sensor, entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER, entities.SENSOR_DRUMS_PLUG_POWER]
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(
            f'Triggering {self.controller} motion based activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if entity == entities.SENSOR_DRUMS_PLUG_POWER and abs(float(old) - float(new)) < 3:
            return

        # Work handling
        if self.is_on(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER):
            self.activity.set(activities.Studio.WORKING)
            return

        # Drum handling
        if self.is_consuming_at_least(entities.SENSOR_DRUMS_PLUG_POWER, watts=4):
            self.activity.set(activities.Studio.DRUMMING)
            return

        self.handle_presence()
