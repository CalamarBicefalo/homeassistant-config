from controllers.controller_app import ControllerApp

import activities
import entities


class EnsuiteController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_ENSUITE_MOTION
    activity = activities.Ensuite
