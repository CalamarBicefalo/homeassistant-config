import entities
import helpers
from activity_controllers.generic_controller import MotionController
from rooms import *


class KitchenController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_KITCHEN_MOTION
    cooldown_seconds = 30

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.kitchen.activity

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering kitchen activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        # TV Break Handling
        if self.activity.get() == LivingRoom.Activity.WATCHING_TV and self.state.is_on(self.motion_sensor):
            self.activity.set(Kitchen.Activity.TV_BREAK)

        # Presence Handling
        elif self.state.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)
            self.set_helper_to_now(helpers.LAST_COOKED)

        else:
            self.set_as_empty_in(self.cooldown_seconds)
