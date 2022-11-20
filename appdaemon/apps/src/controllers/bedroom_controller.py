import activities
import entities
import helpers
from controllers.controller_app import ControllerApp


class BedroomController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION
    activity = activities.Bedroom
