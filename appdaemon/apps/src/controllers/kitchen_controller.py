import entities
import helpers
from controllers.controller_app import ControllerApp


class KitchenController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_KITCHEN_MOTION
    activity_helper = helpers.KITCHEN_ACTIVITY