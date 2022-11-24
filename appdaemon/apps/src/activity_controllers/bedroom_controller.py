from controllers.controller_app import ControllerApp

import activities
import entities


class BedroomController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION
    activity = activities.Bedroom
