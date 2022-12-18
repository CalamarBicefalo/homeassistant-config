import entities
from activity_controllers.motion_controller import MotionController
from select_handler import SelectHandler


class BedroomController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION
    cooldown_minutes = 2

    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom
