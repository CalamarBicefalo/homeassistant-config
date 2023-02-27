import activities
import entities
import scenes
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp
from handlers.select_handler import SelectHandler


class StorageRoomScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.activities.storageroom
    illuminance_sensor = None
    room_lights = entities.LIGHT_STORAGE

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.StorageRoom.PRESENT:
            return scenes.STORAGE_BRIGHT
        return scene.off()
