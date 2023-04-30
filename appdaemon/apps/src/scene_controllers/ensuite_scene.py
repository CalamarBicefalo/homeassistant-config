import entities
import scenes
from modes import Mode
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class EnsuiteScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.rooms.ensuite.activity
    illuminance_sensor = None
    room_lights = entities.LIGHT_BATHROOM

    def get_light_scene(self, activity: StrEnum) -> Scene | SceneSelector:
        if activity in [Ensuite.Activity.PRESENT, Ensuite.Activity.SHOWERING]:
            return scene.by_mode({
                Mode.DAY: scenes.BATHROOM_CONCENTRATE,
                Mode.NIGHT: scenes.BATHROOM_CONCENTRATE,
                Mode.SLEEPING: scenes.BATHROOM_NIGHTLIGHT,
            })
        return scene.off()
