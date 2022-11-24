import activities
import entities
import scenes
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp


class StorageRoomScene(SceneApp):
    activity = activities.StorageRoom
    illuminance_sensor = None
    room_lights = entities.LIGHT_STORAGE

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.StorageRoom.PRESENT:
            return scenes.STORAGE_BRIGHT
        return scene.off()
