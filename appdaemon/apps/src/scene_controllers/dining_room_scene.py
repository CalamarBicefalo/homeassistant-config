import entities
import scenes
from modes import Mode
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneByModeSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class DiningRoomScene(SceneApp):

    def initialize(self) -> None:
        super().initialize()

    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.dining_room.activity

    illuminance_sensor = entities.SENSOR_STUDIO_MS_ILLUMINANCE
    room_lights = entities.LIGHT_DINING_ROOM
    speakers = entities.MEDIA_PLAYER_COOKING_AREA_2
    blinds = entities.COVER_BLINDS_CURTAIN

    def get_light_scene(self, activity: DiningRoom.Activity) -> Scene | SceneByModeSelector:
        match activity:
            case DiningRoom.Activity.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scene.with_actions(
                        scenes.LIVING_ROOM_WELCOME,
                        lambda: self.handlers.blinds.best_for_temperature(),
                    ),
                    Mode.NIGHT: scene.with_actions(
                        scenes.LIVING_ROOM_WELCOME,
                        lambda: self.handlers.blinds.close(),
                    )
                })

            case DiningRoom.Activity.DINING:
                return scene.with_actions(
                    scenes.DINING_ROOM_DINNER_TIME,
                    lambda: self.handlers.music.play(Playlist.COOL_JAZZ),
                    lambda: self.handlers.blinds.best_for_temperature(),
                )

        return scene.with_actions(
            scene.off(),
            lambda: self.run_if_activity_stays_in(self.handlers.blinds.best_for_temperature, minutes=10),
        )

    def play_music_if_appropriate(self) -> None:
        if not self.handlers.music.is_playing() and not self.handlers.rooms.studio.activity.is_value(
                Studio.Activity.WORKING):
            self.handlers.music.play(Playlist.random())
