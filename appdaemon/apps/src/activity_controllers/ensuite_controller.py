import entities
import helpers
from activity_controllers.controller_app import ControllerApp


class EnsuiteActivity(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    activity_helper = helpers.ENSUITE_ACTIVITY
