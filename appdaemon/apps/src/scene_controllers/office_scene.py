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


class OfficeScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.office.activity

    illuminance_sensor = entities.SENSOR_MS_STUDIO_EP1_ILLUMINANCE
    room_lights = entities.LIGHT_OFFICE
    speakers = entities.MEDIA_PLAYER_OFFICE_SPEAKER_2
    # blinds = entities.COVER_OFFICE_BLINDS
    # room_has_plants = False

    def get_light_scene(self, activity: Office.Activity, previous_activity: Optional[StrEnum]) -> Scene | SceneByModeSelector:
        match activity:
            case Office.Activity.WORKING:
                return scene.with_actions(
                    scenes.OFFICE_NATURAL_LIGHT_3,
                    lambda: self.play_music_if_appropriate(),
                    # lambda: self.handlers.blinds.best_for_temperature(),
                )

            case Office.Activity.MEETING:
                return scene.with_actions(
                    scenes.OFFICE_NATURAL_LIGHT_3,
                    lambda: self.handlers.music.pause(),
                    # lambda: self.handlers.blinds.best_for_temperature(),
                )

            case Office.Activity.PRESENT:
                return scene.with_actions(
                    scenes.OFFICE_NATURAL_LIGHT_3,
                    lambda: self.pause_music_if_working_before(previous_activity),
                    # lambda: self.handlers.blinds.best_for_temperature(),
                )

        return scene.with_actions(
            scene.off(),
            lambda: self.pause_music_if_working_before(previous_activity),
            # lambda: self.handlers.blinds.best_for_temperature(),
        )

    # def on_mode_change(self, new: Mode, old: Mode) -> None:
    #     if new == Mode.AWAY:
    #         self.handlers.blinds.best_for_temperature()

    def play_music_if_appropriate(self) -> None:
        if not self.handlers.music.is_playing():
            self.handlers.music.play(Playlist.DISCOVER_WEEKLY_AMANDA, volume_level=0.3)

    def pause_music_if_working_before(self, previous_activity) -> None:
        if previous_activity == Office.Activity.WORKING:
            self.handlers.music.pause()
