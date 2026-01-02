import math
import uuid
from typing import Optional
from uuid import UUID

import entities
import scenes
from music import Playlist, Radio, Tune
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import SceneByModeSelector, Scene
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler
from selects import Mode


class BedroomScene(SceneApp):
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_EPL_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM
    speakers = entities.MEDIA_PLAYER_BEDROOM_SPEAKERS
    blinds = entities.COVER_BEDROOM_CURTAIN_COVER
    room_has_plants = True
    wakeup_duration_minutes = 15
    bedtime_duration_minutes = 30
    bedtime_initial_brightness_pct = 60
    bedtime_initial_volume = 0.3
    minutes_left = 0
    running_group = uuid.uuid4()

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.bedroom.activity

    def get_light_scene(self, activity: StrEnum, previous_activity: Optional[StrEnum]) -> SceneByModeSelector | Optional[Scene]:

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
                    lambda: self.turn_on(entities.SCENE_BEDROOM_BEDTIME,
                                         brightness_pct=self.bedtime_initial_brightness_pct),
                    lambda: self.handlers.blinds.close(),
                    lambda: self.handlers.music.play(Playlist.NEO_CLASSICAL_LOUNGE,
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
                    Mode.DAY: scene.with_actions(scenes.BEDROOM_BRIGHT, lambda: self.handlers.blinds.best_for_temperature()),
                    Mode.NIGHT: scene.with_actions(scenes.BEDROOM_NIGHTLIGHT, lambda: self.handlers.blinds.close()),
                    Mode.SLEEPING: scene.with_actions(scene.off(), lambda: self.handlers.blinds.close()),
                })

            case Bedroom.Activity.EMPTY:
                actions = [lambda: self.handlers.blinds.best_for_temperature()]
                if self.just_woke_up:
                    actions.append(lambda: self.handlers.music.pause())
                return scene.with_actions(
                        scene.off(),
                        *actions,
        )

    def prepare_to_wake_up(self) -> None:
        is_dark = self.is_dark()
        self.log(f'Running wakeup loop, is_dark={is_dark}.', level="INFO")
        self.handlers.music.play(Tune.BIRDS, shuffle=False, volume_level=0.2)

        def during_waking_up(minutes_left: int) -> None:
            self.log(f'Running wakeup loop, {self.minutes_left} minutes left.', level="DEBUG")
            if not self.activity.is_value(Bedroom.Activity.WAKING_UP):
                raise Exception("waking up loop can only run during waking up activity")

            if is_dark:
                # Brighten lights slowly
                new_brightness_pct = round(6 * (self.wakeup_duration_minutes - minutes_left))
                self.get_entity(self.room_lights).turn_on(brightness_pct=new_brightness_pct)
            else:
                # Open blinds
                current_position = self.handlers.blinds.get_position()
                left_to_open = 100 - current_position

                if minutes_left <= 0 or left_to_open <= 0:
                    self.handlers.blinds.open()
                    raise Exception("blinds should be open by now, aborting countdown")

                next_increment = math.floor(left_to_open / minutes_left)
                next_position = current_position + next_increment
                self.log(f'current blind position = {current_position}. next position = {next_position}, increment = {next_increment}', level="DEBUG")
                
                if next_increment >= 25:
                    self.handlers.blinds.set_position(next_position)

        def after_wakeup() -> None:
            self.run_in(lambda *_: self.handlers.music.play(Radio.BBC_RADIO_4, shuffle=False, volume_level=0.3), 60)

        self.run_for(self.wakeup_duration_minutes, callback=during_waking_up, afterwards=after_wakeup, running_group=self.running_group, interval_minutes=3)

    def prepare_to_sleep(self) -> None:
        if self.handlers.mode.is_value(Mode.SLEEPING):
            self.log(f'aborting bedtime loop because mode is sleeping.')
            return

        def after_bedtime() -> None:
            self.handlers.mode.set(Mode.SLEEPING)
            self.go_to_sleep()

        def during_bedtime(minutes_left: int) -> None:
            self.log(f'Running bedtime loop, {self.minutes_left} minutes left.', level="DEBUG")
            if not self.activity.is_value(Bedroom.Activity.BEDTIME):
                raise Exception("bedtime loop can only run during bedtime activity")
            if self.handlers.mode.is_value(Mode.SLEEPING):
                raise Exception("aborting bedtime loop because mode is sleeping")

            # Dim lights
            new_brightness_pct = round(self.bedtime_initial_brightness_pct * minutes_left / self.bedtime_duration_minutes)
            self.get_entity(self.room_lights).turn_on(brightness_pct=new_brightness_pct)

            # Dim music
            new_volume = round(self.bedtime_initial_volume * minutes_left / self.bedtime_duration_minutes, 2)
            if new_volume >= 0.1:
                self.handlers.music.volume(new_volume)

        self.run_for(self.bedtime_duration_minutes, callback=during_bedtime, afterwards=after_bedtime, running_group=self.running_group, interval_minutes=1)

    def go_to_sleep(self) -> None:
        self.turn_off(self.room_lights)
        self.run_in(lambda *_: self.handlers.music.play(Tune.RAIN, volume_level=0.2), 2)

    def on_mode_change(self, new: Mode, old: Mode) -> None:
        if new == Mode.SLEEPING:
            self.go_to_sleep()
        elif new == Mode.AWAY or self.activity.is_value(Bedroom.Activity.EMPTY):
            self.handlers.blinds.best_for_temperature()
