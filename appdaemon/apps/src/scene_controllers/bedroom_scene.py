from typing import Optional

import entities
import modes
import scenes
from modes import Mode
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class BedroomScene(SceneApp):
    illuminance_sensor = entities.SENSOR_BEDROOM_ENTRANCE_MS_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM
    speakers = entities.MEDIA_PLAYER_MASS_BEDROOM_SPEAKERS
    mode_change = None

    @property
    def activity(self) -> SelectHandler:
        return self.rooms.bedroom.activity

    def get_light_scene(self, activity: StrEnum) -> SceneSelector | Optional[Scene]:
        if activity == Bedroom.Activity.BEDTIME or activity == Bedroom.Activity.WAKING_UP:
            return None
        if activity == Bedroom.Activity.RELAXING:
            return scenes.BEDROOM_RELAXING
        if activity == Bedroom.Activity.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.BEDROOM_BRIGHT,
                Mode.NIGHT: scenes.BEDROOM_NIGHTLIGHT,
                Mode.SLEEPING: scene.off()
            })
        return scene.off()

    def on_activity_change(self, activity: StrEnum) -> None:
        if self.mode_change:
            self.cancel_timer(self.mode_change)
            self.mode_change = None

        if activity == Bedroom.Activity.RELAXING:
            self.music.play(Playlist.NEO_CLASSICAL, volume_level=0.3)
            self.blinds.close(entities.COVER_BEDROOM_CURTAIN_COVER)

        elif activity == Bedroom.Activity.WAKING_UP:
            self.blinds.open_for(entities.COVER_BEDROOM_CURTAIN_COVER, 30)

        elif activity == Bedroom.Activity.BEDTIME:
            # Home cleanup
            self.turn_off_media()

            # Bedroom scene
            self.turn_on(entities.SCENE_BEDROOM_BRIGHT)
            self.turn_on(entities.SCENE_BEDROOM_DIMMED)
            self.blinds.close(entities.COVER_BEDROOM_CURTAIN_COVER)
            self.music.play(Playlist.DISCOVER_WEEKLY, volume_level=0.3)
            self.run_in(lambda *_: self.music.volume(0.2), 10 * 60)
            self.run_in(lambda *_: self.music.volume(0.1), 20 * 60)
            self.run_in(lambda *_: self.turn_off(entities.LIGHT_FULL_LIVING_ROOM), 120)
            self.mode_change = self.run_in(lambda *_: self.mode.set(Mode.SLEEPING), 30 * 60)

        elif self.mode.get() == modes.Mode.DAY:
            self.blinds.open(entities.COVER_BEDROOM_CURTAIN_COVER)
