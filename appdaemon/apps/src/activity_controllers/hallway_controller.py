import entities
from activity_controllers.motion_controller import MotionController
from select_handler import SelectHandler


class HallwayController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_HALLWAY_MS_MOTION
    cooldown_seconds = 30
    @property
    def activity(self) -> SelectHandler:
        return self.activities.hallway
