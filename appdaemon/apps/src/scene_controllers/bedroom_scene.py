from typing import Optional

import activities
import entities
import scenes
from modes import Mode
from music import Playlist
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class BedroomScene(SceneApp):
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM
    speakers = entities.MEDIA_PLAYER_MASS_BEDROOM_SPEAKERS

    @property
    def activity(self) -> SelectHandler:
        return self.activities.bedroom

    def get_light_scene(self, activity: activities.Activity) -> SceneSelector | Optional[Scene]:
        mode = self.mode.get()
        if mode == Mode.SLEEPING or mode == Mode.BEDTIME:
            return None
        if activity == activities.Bedroom.RELAXING:
            return scenes.BEDROOM_RELAXING
        if activity == activities.Bedroom.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.BEDROOM_BRIGHT,
                Mode.NIGHT: scenes.BEDROOM_NIGHTLIGHT,
            })
        return scene.off()

    def on_activity_change(self, activity: activities.Activity) -> None:
        if activity == activities.Bedroom.RELAXING:
            self.music.play(Playlist.random(), volume_level=0.3)

