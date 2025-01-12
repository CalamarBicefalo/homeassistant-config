from datetime import datetime
from typing import Optional

import entities
import scenes
from activity_controllers.living_room_controller import COFFEE_TABLE_BUTTON_IEEE_ADDRESS
from blinds_handler import BlindsHandler
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneByModeSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler
from selects import Mode


class LivingRoomScene(SceneApp):
    balcony_blinds = None

    def initialize(self) -> None:
        super().initialize()
        # self.balcony_blinds = BlindsHandler(self, entities.COVER_BALCONY_BLINDS_LG_CURTAIN)
        self.handlers.buttons.on_click(COFFEE_TABLE_BUTTON_IEEE_ADDRESS, self.music_manual_override_toggle)
        self.handlers.buttons.on_long_press(COFFEE_TABLE_BUTTON_IEEE_ADDRESS, self.disable_music_manual_override)

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.living_room.activity

    illuminance_sensor = entities.SENSOR_MS_STUDIO_EP1_ILLUMINANCE
    room_lights = entities.LIGHT_LIVING_ROOM
    speakers = entities.MEDIA_PLAYER_LIVING_ROOM_STEREO
    blinds = entities.COVER_BLINDS_CURTAIN
    music_manual_override = False

    def get_light_scene(self, activity: LivingRoom.Activity, previous_activity: Optional[StrEnum]) -> Scene | SceneByModeSelector:
        match activity:
            case LivingRoom.Activity.RELAXING:
                return scene.with_actions(
                    scenes.LIVING_ROOM_COZY,
                    lambda: self.play_music_if_appropriate(),
                    lambda: self.handlers.blinds.close(),
                )

            case LivingRoom.Activity.WATCHING_TV:
                return scene.with_actions(
                    scenes.LIVING_ROOM_MOVIE,
                    lambda: self.handlers.music.pause(),
                    lambda: self.handlers.blinds.close(),
                )

            case LivingRoom.Activity.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scene.with_actions(
                        scenes.LIVING_ROOM_NATURAL_LIGHT_3,
                        lambda: self.handlers.blinds.best_for_temperature(),
                        # lambda: self.set_balcony_blinds_for_views(),
                    ),
                    Mode.NIGHT: scene.with_actions(
                        scenes.LIVING_ROOM_NATURAL_LIGHT_3,
                        lambda: self.handlers.blinds.close(),
                        # lambda: self.balcony_blinds.close(),
                    ),
                    Mode.SLEEPING: scenes.LIVING_ROOM_COZY,
                })

            case LivingRoom.Activity.DRUMMING:
                return scene.with_actions(
                    scenes.LIVING_ROOM_DRUMMING,
                    lambda: self.handlers.music.pause(),
                    lambda: self.handlers.blinds.close(),
                )

            case LivingRoom.Activity.GAMING:
                return scene.with_actions(
                    scenes.LIVING_ROOM_GAMING,
                    lambda: self.handlers.music.pause(),
                    lambda: self.handlers.blinds.close(),
                )

            case LivingRoom.Activity.DINING:
                return scene.with_actions(
                    scenes.LIVING_ROOM_DINING,
                    lambda: self.handlers.music.play(Playlist.COOL_JAZZ),
                    lambda: self.handlers.blinds.best_for_temperature(),
                )

        return scene.with_actions(
            scene.off(),
            lambda: self.run_if_activity_stays_in(self.handlers.blinds.best_for_temperature, minutes=10),
            # lambda: self.run_if_activity_stays_in(self.balcony_blinds.best_for_temperature, minutes=10),
            lambda: self.disable_music_manual_override(),
        )

    def set_balcony_blinds_for_views(self):
        hour = datetime.now().hour
        if hour > 12:
            self.balcony_blinds.open()
        elif hour > 10 and self.handlers.temperature.should_cooldown():
            self.balcony_blinds.set_position(50)
        else:
            self.balcony_blinds.best_for_temperature()

    def play_music_if_appropriate(self) -> None:
        if not self.handlers.music.is_playing() and not (
                self.handlers.rooms.studio.activity.is_value(Studio.Activity.WORKING)
                or self.handlers.rooms.studio.activity.is_value(Studio.Activity.MEETING)
        ):
            self.handlers.music.play(Playlist.random())

    def disable_music_manual_override(self) -> None:
        self.music_manual_override = False

    def music_manual_override_toggle(self) -> None:
        self.music_manual_override = True
        self.handlers.music.toggle_play_pause()
