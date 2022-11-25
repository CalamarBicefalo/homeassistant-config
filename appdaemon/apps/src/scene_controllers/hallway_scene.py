import activities
import entities
import scenes
from modes import Mode
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class HallwayScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.activities.hallway
    illuminance_sensor = entities.SENSOR_HALLWAY_MS_ILLUMINANCE
    room_lights = entities.LIGHT_HALLWAY

    def get_light_scene(self, activity: activities.Activity) -> Scene | SceneSelector:
        if activity == activities.Hallway.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.HALLWAY_BRIGHT,
                Mode.NIGHT: scenes.HALLWAY_TYRELL,
                Mode.SLEEPING: scenes.HALLWAY_NIGHTLIGHT,
            })
        return scene.off()
