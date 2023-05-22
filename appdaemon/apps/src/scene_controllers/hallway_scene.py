import entities
import scenes
from modes import Mode
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class HallwayScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.hallway.activity
    illuminance_sensor = entities.SENSOR_HALLWAY_MS_ILLUMINANCE
    room_lights = entities.LIGHT_HALLWAY

    def get_light_scene(self, activity: StrEnum) -> Scene | SceneSelector:
        if activity == Hallway.Activity.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.HALLWAY_BRIGHT,
                Mode.NIGHT: scenes.HALLWAY_TYRELL,
                Mode.SLEEPING: scenes.HALLWAY_NIGHTLIGHT,
            })
        return scene.off()
