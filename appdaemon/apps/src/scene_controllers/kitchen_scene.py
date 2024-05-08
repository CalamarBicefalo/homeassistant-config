import entities
import scenes
from selects import Mode
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneByModeSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class KitchenScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.handlers.rooms.kitchen.activity

    illuminance_sensor = entities.SENSOR_KITCHEN_MS_ILLUMINANCE
    room_lights = entities.LIGHT_KITCHEN
    speakers = entities.MEDIA_PLAYER_LIVING_ROOM_STEREO

    def get_light_scene(self, activity: StrEnum) -> Scene | SceneByModeSelector:
        match activity:
            case Kitchen.Activity.TV_BREAK:
                return scenes.KITCHEN_TV

            case Kitchen.Activity.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scenes.KITCHEN_CONCENTRATE,
                    Mode.NIGHT: scenes.KITCHEN_COOK,
                    Mode.SLEEPING: scenes.KITCHEN_NIGHTLIGHT,
                })

            case Kitchen.Activity.COOKING:
                return scene.with_actions(
                    scenes.KITCHEN_COOK,
                    self.play_music_if_appropriate,
                )

        return scene.off()

    def play_music_if_appropriate(self) -> None:
        if not self.handlers.music.is_playing():
            self.handlers.music.play(Playlist.random())
