import activities
import entities
import helpers
from app import App


class StorageRoomController(App):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION
    activity = activities.Bedroom
