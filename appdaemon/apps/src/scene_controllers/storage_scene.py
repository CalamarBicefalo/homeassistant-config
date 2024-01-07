import entities
import scenes
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class StorageScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.storage.activity
    illuminance_sensor = None
    room_lights = entities.LIGHT_STORAGE

    def get_light_scene(self, activity: StrEnum) -> Scene:
        if activity == Storage.Activity.PRESENT:
            return scenes.STORAGE_BRIGHT
        return scene.off()
