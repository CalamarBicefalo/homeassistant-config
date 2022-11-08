import entities
import helpers
from activity_controllers.controller_app import ControllerApp


class KitchenActivity(ControllerApp):
    motion_sensor = entities.BINARY_SENSOR_KITCHEN_MOTION
    activity_helper = helpers.KITCHEN_ACTIVITY
