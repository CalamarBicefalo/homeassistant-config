import entities
import states
from activity_controllers.generic_controller import MotionController
from activity_handler import ActivityHandler
from rooms import CommonActivities, Hallway
from select_handler import SelectHandler


class HallwayController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_HALLWAY_MS_MOTION
    contact_sensor = entities.BINARY_SENSOR_FLAT_DOOR_CS
    cooldown_seconds = 30

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
            self.set_as_empty_in(seconds=10)

    def on_door(self, entity, attribute, old, new, kwargs) -> None:  # type: ignore
        self.cancel_empty_timer()
        self.activity.set(Hallway.Activity.PRESENT)
        self.set_as_empty_in(seconds=self.cooldown_seconds)
