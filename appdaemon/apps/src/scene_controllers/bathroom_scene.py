import entities
import scenes
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneByModeSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler
from selects import Mode


class BathroomScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.bathroom.activity
    illuminance_sensor = None
    room_lights = entities.LIGHT_BATHROOM

    def get_light_scene(self, activity: StrEnum) -> Scene | SceneByModeSelector:
        if activity in [Bathroom.Activity.PRESENT, Bathroom.Activity.SHOWERING]:
            return scene.by_mode({
                Mode.DAY: scenes.BATHROOM_CONCENTRATE,
                Mode.NIGHT: scenes.BATHROOM_CONCENTRATE,
                Mode.SLEEPING: scenes.BATHROOM_NIGHTLIGHT,
            })
        return scene.off()
