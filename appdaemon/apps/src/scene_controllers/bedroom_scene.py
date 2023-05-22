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
    illuminance_sensor = entities.SENSOR_STUDIO_MS_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM
    speakers = entities.MEDIA_PLAYER_MASS_BEDROOM_SPEAKERS
    blinds = entities.COVER_BEDROOM_CURTAIN_COVER
    bedtime_duration_minutes = 30
    bedtime_initial_brightness = 255
    bedtime_initial_volume = 0.3
    minutes_left = 0

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.bedroom.activity

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
        if activity == Bedroom.Activity.RELAXING:
            self.handlers.music.play(Playlist.NEO_CLASSICAL, volume_level=0.3)
            self.handlers.blinds.close()

        elif activity == Bedroom.Activity.WAKING_UP:
            def during_waking_up(minutes_left: int) -> None:
                self.log(f'Running bedtime loop, {self.minutes_left} minutes left.', level="DEBUG")
                if not self.activity.is_value(Bedroom.Activity.WAKING_UP):
                    raise Exception("waking up loop can only run during waking up activity")

                # Open blinds
                current_position = self.handlers.blinds.get_position()
                left_to_open = 100 - current_position
                next_increment = math.floor(left_to_open / minutes_left)
                next_position = current_position + next_increment
                self.log(f'current blind position = {current_position}. next position = {next_position}', level="DEBUG")
                self.handlers.blinds.set_position()

            self.run_for(self.bedtime_duration_minutes, during_waking_up, None)

        elif activity == Bedroom.Activity.BEDTIME:
            # Home cleanup
            self.turn_off_media()

            # Bedroom scene
            self.turn_on(entities.SCENE_BEDROOM_WARM_EMBRACE)
            self.handlers.blinds.close()

            self.handlers.music.play(Playlist.DISCOVER_WEEKLY, volume_level=self.bedtime_initial_volume)

            def after_bedtime() -> None:
                self.handlers.mode.set(Mode.SLEEPING)

            def during_bedtime(minutes_left: int) -> None:
                self.log(f'Running bedtime loop, {self.minutes_left} minutes left.', level="DEBUG")
                if not self.activity.is_value(Bedroom.Activity.BEDTIME):
                    raise Exception("bedtime loop can only run during bedtime activity")

                # Dim lights
                new_brightness = round(self.bedtime_initial_brightness * minutes_left / self.bedtime_duration_minutes)
                self.log(f'new brightness = {new_brightness}', level="DEBUG")
                self.get_entity(self.room_lights).turn_on(brightness=new_brightness)

                # Dim music
                new_volume = round(self.bedtime_initial_volume * minutes_left / self.bedtime_duration_minutes, 2)
                self.log(f'new volume = {new_brightness}', level="DEBUG")
                self.handlers.music.volume(new_volume)

            self.run_for(self.bedtime_duration_minutes, during_bedtime, after_bedtime)


        elif self.handlers.mode.get() == modes.Mode.DAY:
            self.handlers.blinds.open()
