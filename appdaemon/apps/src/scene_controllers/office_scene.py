from typing import Optional

import entities
import scenes
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneByModeSelector, Facet
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler
from selects import Mode


class OfficeScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.office.activity

    brightness_sensor = entities.SENSOR_OFFICE_BRIGHTNESS
    room_lights = entities.LIGHT_OFFICE
    speakers = entities.MEDIA_PLAYER_OFFICE_SPEAKER_2
    blinds = entities.COVER_OFFICE_BLINDS
    window = entities.BINARY_SENSOR_OFFICE_OFFICE_WINDOW_CS_WINDOW
    room_has_plants = True

    def get_light_scene(self, activity: Office.Activity, previous_activity: Optional[StrEnum]) -> Scene | SceneByModeSelector:
        match activity:
            case Office.Activity.WORKING:
                return scene.with_actions(
                    scenes.OFFICE_WORKING,
                    (Facet.MEDIA, lambda: self.play_music_if_appropriate()),
                    (Facet.BLINDS, lambda: self.handlers.blinds.best_for_temperature()),
                    (Facet.POWER, lambda: self.turn_on(entities.SWITCH_MONITOR)),
                )

            case Office.Activity.MEETING:
                return scene.with_actions(
                    scenes.OFFICE_WORKING,
                    (Facet.MEDIA, lambda: self.handlers.music.pause()),
                    (Facet.BLINDS, lambda: self.handlers.blinds.best_for_temperature()),
                    (Facet.POWER, lambda: self.turn_on(entities.SWITCH_MONITOR)),
                )

            case Office.Activity.DRUMMING:
                return scene.with_actions(
                    scenes.OFFICE_DRUMMING,
                    (Facet.POWER, lambda: self.turn_on(entities.SWITCH_DRUM_POWER_STRIP_SPEAKERS)),
                    (Facet.POWER, lambda: self.turn_on(entities.SWITCH_DRUM_POWER_STRIP_SWITCH)),
                    (Facet.POWER, lambda: self.turn_on(entities.SWITCH_DRUM_POWER_STRIP_TABLET)),
                    (Facet.POWER, lambda: self.turn_on(entities.SWITCH_DRUM_POWER_STRIP_FOCUSRITE)),
                    (Facet.POWER, lambda: self.turn_on(entities.SWITCH_DRUM_POWER_STRIP_ROLAND)),
                    (Facet.MEDIA, lambda: self.handlers.music.pause()),
                    (Facet.BLINDS, lambda: self.handlers.blinds.close()),
                    (Facet.POWER, lambda: self.turn_off(entities.SWITCH_MONITOR)),
                )

            case Office.Activity.SNARING:
                return scene.with_actions(
                    scenes.OFFICE_SNARING,
                    (Facet.MEDIA, lambda: self.handlers.music.pause()),
                    (Facet.BLINDS, lambda: self.handlers.blinds.close()),
                    (Facet.POWER, lambda: self.turn_off(entities.SWITCH_MONITOR)),
                )

            case Office.Activity.PRESENT:
                return scene.with_actions(
                    scenes.OFFICE_NATURAL_LIGHT_3,
                    (Facet.MEDIA, lambda: self.pause_music_if_working_before(previous_activity)),
                    (Facet.BLINDS, lambda: self.handlers.blinds.best_for_temperature()),
                )

        return scene.with_actions(
            scene.off(),
            (Facet.MEDIA, lambda: self.pause_music_if_working_before(previous_activity)),
            (Facet.POWER, lambda: self.turn_off(entities.FAN_OFFICE_FAN)),
            (Facet.POWER, lambda: self.turn_off(entities.SWITCH_DRUM_POWER_STRIP_SPEAKERS)),
            (Facet.POWER, lambda: self.turn_off(entities.SWITCH_DRUM_POWER_STRIP_SWITCH)),
            (Facet.POWER, lambda: self.turn_off(entities.SWITCH_DRUM_POWER_STRIP_TABLET)),
            (Facet.POWER, lambda: self.turn_off(entities.SWITCH_DRUM_POWER_STRIP_FOCUSRITE)),
            (Facet.POWER, lambda: self.turn_off(entities.SWITCH_DRUM_POWER_STRIP_ROLAND)),
            (Facet.POWER, lambda: self.turn_off(entities.SWITCH_MONITOR)),
            (Facet.BLINDS, lambda: self.handlers.blinds.best_for_temperature()),
        )

    def play_music_if_appropriate(self) -> None:
        if not self.handlers.music.is_playing():
            self.handlers.music.play(Playlist.random(), volume_level=0.3)

    def pause_music_if_working_before(self, previous_activity) -> None:
        if previous_activity == Office.Activity.WORKING:
            self.handlers.music.pause()
