import entities
import scenes
from activity_controllers.living_room_controller import COFFEE_TABLE_BUTTON_IEEE_ADDRESS
from selects import Mode
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneByModeSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class LivingRoomScene(SceneApp):

    def initialize(self) -> None:
        super().initialize()
        self.handlers.buttons.on_click(COFFEE_TABLE_BUTTON_IEEE_ADDRESS, self.music_manual_override_toggle)
        self.handlers.buttons.on_long_press(COFFEE_TABLE_BUTTON_IEEE_ADDRESS, self.disable_music_manual_override)

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.living_room.activity

    illuminance_sensor = entities.SENSOR_STUDIO_MS_ILLUMINANCE
    room_lights = entities.LIGHT_LIVING_ROOM
    speakers = entities.MEDIA_PLAYER_LIVING_ROOM_STEREO
    blinds = entities.COVER_BLINDS_CURTAIN
    music_manual_override = False

    def get_light_scene(self, activity: LivingRoom.Activity) -> Scene | SceneByModeSelector:
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
                        scenes.LIVING_ROOM_WELCOME,
                        lambda: self.handlers.blinds.best_for_temperature(),
                    ),
                    Mode.NIGHT: scene.with_actions(
                        scenes.LIVING_ROOM_WELCOME,
                        lambda: self.handlers.blinds.close(),
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
            lambda: self.disable_music_manual_override(),
        )

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
