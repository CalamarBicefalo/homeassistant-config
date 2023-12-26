import entities
import states
from activity_controllers.generic_controller import ActivityController
from rooms import *
from select_handler import SelectHandler


class WardrobeController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_WARDROBE_MS_MOTION

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.wardrobe.activity

    @property
    def max_inactive_activity_seconds(self) -> int:
        return 10 * 60

    def initialize(self) -> None:
        self.listen_state(
            self.controller_handler,
            [
                self.motion_sensor,
                entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR,
                entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE,
                entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE,
            ]
        )

    def controller_handler(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.log(
            f'Triggering wardrobe activity controller {entity} -> {attribute} old={old} new={new}',
            level="DEBUG")

        self.cancel_empty_timer()

        # Dressing Handling
        if self.is_wardrobe_sensor(entity):
            if self.wardrobe_is_open():
                self.activity.set(Wardrobe.Activity.DRESSING)
            else:
                self.activity.set(Wardrobe.Activity.PRESENT)

        # Presence Handling
        elif self.state.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(seconds=10)

    def is_wardrobe_sensor(self, entity: entities.Entity) -> bool:
        return entity in [
            entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR,
            entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE,
            entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE,
        ]

    def wardrobe_is_open(self) -> bool:
        return (
                self.state.is_on(entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR)
                or self.state.is_value(entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE, states.OPEN)
                or self.state.is_value(entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE, states.OPEN)
        )
