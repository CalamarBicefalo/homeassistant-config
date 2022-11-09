import entities
import helpers
from controllers.controller_app import ControllerApp


class EnsuiteController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    activity_helper = helpers.ENSUITE_ACTIVITY
