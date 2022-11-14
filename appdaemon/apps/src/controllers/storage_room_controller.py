import entities
import helpers
from app import App


class StorageRoomController(App):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION
    activity_helper = helpers.BEDROOM_ACTIVITY
