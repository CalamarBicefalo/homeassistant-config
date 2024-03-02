import entities
import scenes
from selects import Mode
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneByModeSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class EnsuiteScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.ensuite.activity
    illuminance_sensor = None
    room_lights = entities.LIGHT_ENSUITE

    def get_light_scene(self, activity: StrEnum) -> Scene | SceneByModeSelector:
        if activity in [Ensuite.Activity.PRESENT, Ensuite.Activity.SHOWERING]:
            return scene.by_mode({
                Mode.DAY: scenes.ENSUITE_CONCENTRATE,
                Mode.NIGHT: scenes.ENSUITE_CONCENTRATE,
                Mode.SLEEPING: scenes.ENSUITE_NIGHTLIGHT,
            })
        return scene.off()
