from typing import Optional

import entities
import scenes
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneByModeSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler
from selects import Mode


class StudioScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.studio.activity

    illuminance_sensor = entities.SENSOR_MS_STUDIO_EP1_ILLUMINANCE
    room_lights = entities.LIGHT_STUDIO
    speakers = entities.MEDIA_PLAYER_LIVING_ROOM_STEREO
    blinds = entities.COVER_CURTAINS_STUDIO
    room_has_plants = False

    def get_light_scene(self, activity: Studio.Activity, previous_activity: Optional[StrEnum]) -> Scene | SceneByModeSelector:
        match activity:
            case Studio.Activity.WORKING:
                return scene.with_actions(
                    scenes.STUDIO_WORKING,
                    lambda: self.turn_on(entities.SWITCH_MONITOR),
                    lambda: self.play_music_if_appropriate(),
                )

            case Studio.Activity.MEETING:
                return scene.with_actions(
                    scenes.STUDIO_WORKING,
                    lambda: self.turn_on(entities.SWITCH_MONITOR),
                    lambda: self.handlers.music.pause(),
                )

            case Studio.Activity.PRESENT:
                return scene.with_actions(
                    scenes.STUDIO_NATURAL_LIGHT,
                    lambda: self.handlers.blinds.best_for_temperature(),
                )

        return scene.with_actions(
            scene.off(),
            lambda: self.turn_off(entities.SWITCH_MONITOR),
            lambda: self.handlers.blinds.best_for_temperature(),
        )

    def on_mode_change(self, new: Mode, old: Mode) -> None:
        self.handlers.blinds.best_for_temperature()

    def play_music_if_appropriate(self) -> None:
        if not self.handlers.music.is_playing():
            self.handlers.music.play(Playlist.DISCOVER_WEEKLY_AMANDA, volume_level=0.3)
