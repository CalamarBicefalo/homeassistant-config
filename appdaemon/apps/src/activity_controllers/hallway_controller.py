from controllers.controller_app import ControllerApp

import activities
import entities


class HallwayController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_HALLWAY_MS_MOTION
    activity = activities.Hallway
