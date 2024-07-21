import entities
import states
from activity_controllers.generic_controller import MotionController
from activity_handler import ActivityHandler
from rooms import Hallway


class HallwayController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_HALLWAY_MOTION
    contact_sensor = entities.BINARY_SENSOR_FLAT_DOOR_CS
    max_seconds_without_presence_until_empty = 10
    max_seconds_until_empty = 60 * 10

    @property
    def activity(self) -> ActivityHandler:
        return self.handlers.rooms.hallway.activity

    def initialize(self) -> None:
        super().initialize_lock()
        self.listen_state(
            self.on_motion,
            self.motion_sensor
        )

        self.listen_state(
            self.on_door,
            self.contact_sensor
        )

    def on_motion(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.cancel_empty_timer()
        if new == states.DETECTED:
            self.activity.set(Hallway.Activity.PRESENT)
        else:
            self.set_as_empty_in(seconds=self.max_seconds_without_presence_until_empty)

    def on_door(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.cancel_empty_timer()
        self.activity.set(Hallway.Activity.PRESENT)
        if self.state.is_off(self.motion_sensor):
            self.set_as_empty_in(seconds=self.max_seconds_without_presence_until_empty)
