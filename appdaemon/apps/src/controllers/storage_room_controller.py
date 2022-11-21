import activities
import entities
from app import App


class StorageRoomController(App):
    motion_sensor = entities.BINARY_SENSOR_BEDROOM_MS_MOTION
    activity = activities.Bedroom
