import activities
import entities
import helpers
from controllers.controller_app import ControllerApp


class EnsuiteController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    activity = activities.Ensuite
