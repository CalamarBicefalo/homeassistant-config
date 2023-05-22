import entities
import scenes
from modes import Mode
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class WardrobeScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.wardrobe.activity
    illuminance_sensor = entities.SENSOR_HALLWAY_MS_ILLUMINANCE
    room_lights = entities.LIGHT_WARDROBE

    def get_light_scene(self, activity: StrEnum) -> Scene | SceneSelector:
        match activity:
            case Wardrobe.Activity.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scenes.WARDROBE_BRIGHT,
                    Mode.NIGHT: scenes.WARDROBE_NIGHTLIGHT,
                    Mode.SLEEPING: scene.off(),
                })
            case Wardrobe.Activity.DRESSING:
                return scenes.WARDROBE_DRESSING

        return scene.off()
