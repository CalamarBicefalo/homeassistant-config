from controllers.controller_app import ControllerApp

import activities
import entities


class WardrobeController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_DOOR_MS_MOTION
    activity = activities.Wardrobe
