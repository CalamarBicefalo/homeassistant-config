import activities
import entities
from activity_controllers.motion_controller import MotionController
from select_handler import SelectHandler


class BedroomController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION
    cooldown_seconds = 60

    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom

    def ignore_motion_trigger(self) -> bool:
        return self.activity.is_value(activities.Bedroom.RELAXING) or self.activity.is_value(activities.Bedroom.BEDTIME)

