import entities
import states
from activity_controllers.generic_controller import ActivityController
from rooms import *


class WardrobeController(ActivityController):
    motion_sensor = entities.BINARY_SENSOR_WARDROBE_MS_MOTION
    max_seconds_until_empty = 15 * 60

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.wardrobe.activity

    def initialize(self) -> None:
        self._dressing_cooldown = None
        super().initialize_lock()
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
        if self._dressing_cooldown:
            self.cancel_timer(self._dressing_cooldown, True)
            self._dressing_cooldown = None
        self.cancel_empty_timer()

        if self.is_wardrobe_sensor(entity):
            self.handle_dressing()

        elif self.state.is_on(self.motion_sensor):
            self.handle_presence()

        else:
            self.set_as_empty_in(seconds=30)

    def handle_dressing(self) -> None:
        if self.wardrobe_is_open():
            self.activity.set(Wardrobe.Activity.DRESSING)
        else:
            if self.activity.is_value(Wardrobe.Activity.DRESSING):
                self._dressing_cooldown = self.run_in(lambda *_: self.dressing_cooldown(), 60)
            else:
                self.activity.set(Wardrobe.Activity.PRESENT)

    def handle_presence(self) -> None:
        if not self.activity.is_value(Wardrobe.Activity.DRESSING):
            self.activity.set(CommonActivities.PRESENT)

    def dressing_cooldown(self) -> None:
        self._dressing_cooldown = None
        if self.state.is_on(self.motion_sensor):
            self.handle_presence()
        else:
            self.activity.set(Wardrobe.Activity.EMPTY)

    def is_wardrobe_sensor(self, entity: entities.Entity) -> bool:
        return entity in [
            entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR,
            entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE,
            entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE,
        ]

    def wardrobe_is_open(self) -> bool:
        return (  # type: ignore
                self.state.is_on(entities.BINARY_SENSOR_WARDROBE_MIDDLE_DOOR)
                or self.state.is_value(entities.BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE, states.OPEN)
                or self.state.is_value(entities.BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE, states.OPEN)
        )
