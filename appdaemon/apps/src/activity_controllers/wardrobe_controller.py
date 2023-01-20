import entities
from activity_controllers.generic_controller import MotionController
from select_handler import SelectHandler


class WardrobeController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_DOOR_MS_MOTION
    cooldown_seconds = 10
    @property
    def activity(self) -> SelectHandler:
        return self.activities.wardrobe
