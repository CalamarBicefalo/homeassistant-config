from typing import Any

import activities
import entities
from app import App
from select_handler import SelectHandler


class StudioController(App):
    motion_sensor = entities.BINARY_SENSOR_STUDIO_MOTION
    cooldown = None

    @property
    def activity(self) -> SelectHandler:
        return self.activities.studio

    def initialize(self) -> None:
        self.log(f'Initializing studio activity controller.', level="DEBUG")

        self.listen_state(
            self.controller_handler,
            [self.motion_sensor, entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER, entities.SENSOR_DRUMS_PLUG_POWER]
        )

    def controller_handler(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(
            f'Triggering studio activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        if entity == entities.SENSOR_DRUMS_PLUG_POWER and abs(float(old) - float(new)) < 3:
            return

        self.handle_cooldown()

        # Work handling
        if self.is_on(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER):
            self.activity.set(activities.Studio.WORKING)

        # Drum handling
        elif self.is_consuming_at_least(entities.SENSOR_DRUMS_PLUG_POWER, watts=4):
            self.activity.set(activities.Studio.DRUMMING)

        # Presence
        elif self.is_on(self.motion_sensor):
            self.activity.set(activities.Common.PRESENT)

        else:
            self.activity.set(activities.Common.EMPTY)

    def handle_cooldown(self) -> None:
        if self.cooldown:
            self.cancel_timer(self.cooldown)
        self.cooldown = self.run_in(lambda *_: self.activities.studio.set(activities.Studio.EMPTY), 5 * 60 * 60)
