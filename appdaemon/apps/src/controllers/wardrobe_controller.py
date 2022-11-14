import entities
import helpers
from controllers.controller_app import ControllerApp


class WardrobeController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_DOOR_MS_MOTION
    activity_helper = helpers.WARDROBE_ACTIVITY
