import activities
import entities
from scenes.scene_app import SceneApp


class StorageRoomScene(SceneApp):
    activity = activities.StorageRoom
    illuminance_sensor = None
    room_lights = entities.LIGHT_STORAGE

    def get_light_scene(self, activity: activities.Activity):
        if activity == activities.StorageRoom.PRESENT:
            return entities.SCENE_STORAGE_BRIGHT

