from controllers.controller_app import ControllerApp

import activities
import entities


class KitchenController(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_KITCHEN_MOTION
    activity = activities.Kitchen
