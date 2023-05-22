import entities
import states
from activity_controllers.generic_controller import ActivityController
from rooms import *
from select_handler import SelectHandler


class WardrobeController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_WARDROBE_MOTION

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.wardrobe.activity

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
                self.set_as_empty_in(minutes=5)
            else:
                self.activity.set(Wardrobe.Activity.PRESENT)

        # Presence Handling
        elif self.is_on(self.motion_sensor):
            self.activity.set(CommonActivities.PRESENT)

        else:
            self.set_as_empty_in(minutes=1)

    def is_wardrobe_sensor(self, entity: entities.Entity) -> bool:
        return entity in [
            entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR,
            entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE,
            entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE,
        ]

    def wardrobe_is_open(self) -> bool:
        return (
                self.is_on(entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR)
                or self.has_state(entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE, states.OPEN)
                or self.has_state(entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE, states.OPEN)
        )
