import math
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
    bedtime_duration_minutes = 30
    minutes_left = 0

    bedtime_loop = None

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
        if self.bedtime_loop:
            self.cancel_timer(self.bedtime_loop)
            self.bedtime_loop = None

        if activity == Bedroom.Activity.RELAXING:
            self.music.play(Playlist.NEO_CLASSICAL, volume_level=0.3)
            self.blinds.close(entities.COVER_BEDROOM_CURTAIN_COVER)

        elif activity == Bedroom.Activity.WAKING_UP:
            self.blinds.open_for(entities.COVER_BEDROOM_CURTAIN_COVER, 30)

        elif activity == Bedroom.Activity.BEDTIME:
            # Home cleanup
            self.turn_off_media()

            # Bedroom scene
            self.turn_on(entities.SCENE_BEDROOM_WARM_EMBRACE)
            self.blinds.close(entities.COVER_BEDROOM_CURTAIN_COVER)

            self.music.play(Playlist.DISCOVER_WEEKLY, volume_level=0.3)

            brightness_step = math.floor(
                self.get_entity(self.room_lights).get_state(attribute="brightness") / 30)

            self.minutes_left = self.bedtime_duration_minutes

            def every_minute_callback() -> None:
                if self.minutes_left <= 0:
                    self.mode.set(Mode.SLEEPING)
                    self.cancel_timer(self.bedtime_loop)
                    self.bedtime_loop = None
                    return

                self.minutes_left = self.minutes_left - 1

                # Dim lights
                current_brightness = self.get_entity(self.room_lights).get_state(attribute="brightness")
                new_brightness = current_brightness - brightness_step
                self.get_entity(self.room_lights).turn_on(brightness=new_brightness)

                # Dim music
                dim_volume_every = math.floor(self.bedtime_duration_minutes / 3)
                if self.minutes_left == dim_volume_every * 2:
                    self.music.volume(0.2)
                elif self.minutes_left == dim_volume_every:
                    self.music.volume(0.1)

            self.bedtime_loop = self.run_minutely(every_minute_callback, 'now')


        elif self.mode.get() == modes.Mode.DAY:
            self.blinds.open(entities.COVER_BEDROOM_CURTAIN_COVER)
