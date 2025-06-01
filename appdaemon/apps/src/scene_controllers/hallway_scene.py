from typing import Optional

import entities
import scenes
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneByModeSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler
from selects import Mode


class HallwayScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.hallway.activity
    illuminance_sensor = entities.SENSOR_MS_HALLWAY_EP1_ILLUMINANCE
    room_lights = entities.LIGHT_HALLWAY

    def get_light_scene(self, activity: StrEnum, previous_activity: Optional[StrEnum]) -> Scene | SceneByModeSelector:
        if activity == Hallway.Activity.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.HALLWAY_BRIGHT,
                Mode.NIGHT: scenes.HALLWAY_NATURAL_LIGHT,
                Mode.SLEEPING: scenes.HALLWAY_NIGHTLIGHT,
            })
        return scene.off()
