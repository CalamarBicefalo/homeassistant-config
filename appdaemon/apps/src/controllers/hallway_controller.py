import activities
import entities
import helpers
from controllers.controller_app import ControllerApp


class HallwayController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_HALLWAY_MS_MOTION
    activity = activities.Hallway
