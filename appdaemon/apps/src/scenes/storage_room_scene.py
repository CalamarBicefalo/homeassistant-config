import activities
import entities
from scenes import scene
from scenes.scene import Scene
from scenes.scene_app import SceneApp


class StorageRoomScene(SceneApp):
    activity = activities.StorageRoom
    illuminance_sensor = None
    room_lights = entities.LIGHT_STORAGE

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.StorageRoom.PRESENT:
            return scene.of(entities.SCENE_STORAGE_BRIGHT)
        return scene.none()
