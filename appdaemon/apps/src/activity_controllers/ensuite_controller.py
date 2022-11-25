import entities
from activity_controllers.controller_app import MotionController
from select_handler import SelectHandler


class EnsuiteController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    @property
    def activity(self) -> SelectHandler:
        return self.activities.ensuite
