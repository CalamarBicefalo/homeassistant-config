import activities
import entities
from controllers.controller_app import ControllerApp


class HallwayController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_HALLWAY_MS_MOTION
    activity = activities.Hallway
