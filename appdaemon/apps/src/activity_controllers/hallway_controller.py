import entities
from activity_controllers.generic_controller import MotionController
from utils.select_handler import SelectHandler


class HallwayController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_HALLWAY_MS_MOTION
    cooldown_seconds = 30
    @property
    def activity(self) -> SelectHandler:
        return self.activities.hallway
