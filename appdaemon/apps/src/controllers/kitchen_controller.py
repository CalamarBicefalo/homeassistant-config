import activities
import entities
from controllers.controller_app import ControllerApp


class KitchenController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_KITCHEN_MOTION
    activity = activities.Kitchen
