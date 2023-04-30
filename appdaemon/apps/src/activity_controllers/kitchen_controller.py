import entities
from activity_controllers.generic_controller import MotionController
from rooms import *
from select_handler import SelectHandler


class KitchenController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_KITCHEN_MOTION
    cooldown_seconds = 30

    @property
    def activity(self) -> SelectHandler:
        return self.rooms.kitchen.activity

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering kitchen activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        # TV Break Handling
        if self.activity.get() == LivingRoom.Activity.WATCHING_TV and self.is_on(self.motion_sensor):
            self.activity.set(Kitchen.Activity.TV_BREAK)

        # Presence Handling
        elif self.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(self.cooldown_seconds)
