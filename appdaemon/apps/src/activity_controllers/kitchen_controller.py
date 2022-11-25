import entities
from activity_controllers.controller_app import MotionController
from select_handler import SelectHandler


class KitchenController(MotionController):
    motion_sensor = entities.BINARY_SENSOR_KITCHEN_MOTION
    @property
    def activity(self) -> SelectHandler:
        return self.activities.kitchen
