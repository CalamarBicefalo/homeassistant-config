import entities
import scenes
from modes import Mode
from music import Playlist
from rooms import *
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneSelector
from scene_controllers.scene_app import SceneApp
from select_handler import SelectHandler


class KitchenScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.rooms.kitchen.activity

    illuminance_sensor = entities.SENSOR_KITCHEN_MS_ILLUMINANCE
    room_lights = entities.LIGHT_KITCHEN
    speakers = entities.MEDIA_PLAYER_MASS_COOKING_AREA

    def get_light_scene(self, activity: StrEnum) -> Scene | SceneSelector:
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
                return scenes.KITCHEN_COOK

        return scene.off()

    def on_activity_change(self, activity: StrEnum) -> None:
        match activity:
            case Kitchen.Activity.COOKING:
                if not self.music.is_playing():
                    self.music.play(Playlist.random())
