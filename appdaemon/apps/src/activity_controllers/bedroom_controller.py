import activities
import entities
from activity_controllers.controller_app import MotionController
from select_handler import SelectHandler


class BedroomController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION

    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom
