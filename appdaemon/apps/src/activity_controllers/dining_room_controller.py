import entities
from activity_controllers.generic_controller import ActivityController
from rooms import *


class LivingRoomController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_LIVING_ROOM_DINING_TABLE_MS

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.dining_room.activity

    def initialize(self) -> None:
        super().initialize_lock()
        self.listen_state(
            self.controller_handler,
            [
                self.motion_sensor,
            ]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering dining room activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        if self.activity.is_value(DiningRoom.Activity.DINING):
            return

        elif self.state.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.activity.set(CommonActivities.EMPTY)
