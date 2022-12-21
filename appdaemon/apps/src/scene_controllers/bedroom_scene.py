from typing import Optional

import activities
import entities
import scenes
from modes import Mode
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class BedroomScene(SceneApp):
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM
    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom

    def get_light_scene(self, activity: activities.Activity) -> SceneSelector | Optional[Scene]:
        if activity == activities.Bedroom.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.BEDROOM_BRIGHT,
                Mode.NIGHT: scenes.BEDROOM_NIGHTLIGHT,
            })
        return scene.off()
