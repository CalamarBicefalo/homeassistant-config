import math
from typing import Optional

import entities
import scenes
from modes import Mode
from music import Playlist, Tune
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneByModeSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class BedroomScene(SceneApp):
    illuminance_sensor = entities.SENSOR_STUDIO_MS_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM
    speakers = entities.MEDIA_PLAYER_BEDROOM_SPEAKERS_2
    blinds = entities.COVER_BEDROOM_CURTAIN_COVER
    bedtime_duration_minutes = 30
    bedtime_initial_brightness = 150
    bedtime_initial_volume = 0.3
    minutes_left = 0

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.bedroom.activity

    def get_light_scene(self, activity: StrEnum) -> SceneByModeSelector | Optional[Scene]:

        match activity:
            case Bedroom.Activity.WAKING_UP:
                return scene.with_actions(
                    None,
                    lambda: self.prepare_to_wake_up(),
                )

            case Bedroom.Activity.BEDTIME:
                return scene.with_actions(
                    None,
                    lambda: self.turn_off_media(),
                    lambda: self.turn_on(entities.SCENE_BEDROOM_WARM_EMBRACE,
                                         brightness=self.bedtime_initial_brightness),
                    lambda: self.handlers.blinds.close(),
                    lambda: self.handlers.music.play(Playlist.DISCOVER_WEEKLY,
                                                     volume_level=self.bedtime_initial_volume),
                    lambda: self.prepare_to_sleep()
                )

            case Bedroom.Activity.RELAXING:
                return scene.with_actions(
                    scenes.BEDROOM_RELAXING,
                    lambda: self.handlers.music.play(Playlist.NEO_CLASSICAL, volume_level=0.3),
                    lambda: self.handlers.blinds.close(),
                )

            case Bedroom.Activity.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scene.with_actions(scenes.BEDROOM_BRIGHT, lambda: self.handlers.blinds.open()),
                    Mode.NIGHT: scene.with_actions(scenes.BEDROOM_NIGHTLIGHT, lambda: self.handlers.blinds.close()),
                    Mode.SLEEPING: scene.with_actions(scene.off(), lambda: self.handlers.blinds.close()),
                })

        return scene.with_actions(
            scene.off(),
            lambda: self.handlers.blinds.best_for_temperature()
        )

    def prepare_to_wake_up(self) -> None:
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
            self.handlers.blinds.set_position(next_position)

        self.run_for(self.bedtime_duration_minutes, during_waking_up, None)

    def prepare_to_sleep(self) -> None:
        def after_bedtime() -> None:
            self.handlers.mode.set(Mode.SLEEPING)
            self.run_in(lambda *_: self.handlers.music.play(Tune.RAIN, volume_level=0.2), 2)

        def during_bedtime(minutes_left: int) -> None:
            self.log(f'Running bedtime loop, {self.minutes_left} minutes left.', level="DEBUG")
            if not self.activity.is_value(Bedroom.Activity.BEDTIME):
                raise Exception("bedtime loop can only run during bedtime activity")
            if self.handlers.mode.is_value(Mode.SLEEPING):
                raise Exception("aborting bedtime loop because mode is sleeping")

            # Dim lights
            new_brightness = round(self.bedtime_initial_brightness * minutes_left / self.bedtime_duration_minutes)
            self.get_entity(self.room_lights).turn_on(brightness=new_brightness)

            # Dim music
            new_volume = round(self.bedtime_initial_volume * minutes_left / self.bedtime_duration_minutes, 2)
            if new_volume >= 0.1:
                self.handlers.music.volume(new_volume)

        self.run_for(self.bedtime_duration_minutes, during_bedtime, after_bedtime)
