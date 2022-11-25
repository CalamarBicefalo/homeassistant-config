import entities
from activity_controllers.controller_app import MotionController
from select_handler import SelectHandler


class HallwayController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_HALLWAY_MS_MOTION
    @property
    def activity(self) -> SelectHandler:
        return self.activities.hallway
