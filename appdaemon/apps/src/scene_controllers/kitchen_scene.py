import activities
import entities
import scenes
from modes import Mode
from handlers.music import Playlist
from scene_controllers import scene
from scene_controllers.scene import Scene, SceneSelector
from scene_controllers.scene_app import SceneApp
from handlers.select_handler import SelectHandler


class KitchenScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.activities.kitchen

    illuminance_sensor = entities.SENSOR_KITCHEN_MS_ILLUMINANCE
    room_lights = entities.LIGHT_KITCHEN
    speakers = entities.MEDIA_PLAYER_MASS_COOKING_AREA

    def get_light_scene(self, activity: activities.Activity) -> Scene | SceneSelector:
        match activity:
            case activities.Kitchen.TV_BREAK:
                return scenes.KITCHEN_TV
            case activities.Kitchen.PRESENT:
                return scene.by_mode({
                    Mode.DAY: scenes.KITCHEN_CONCENTRATE,
                    Mode.NIGHT: scenes.KITCHEN_COOK,
                    Mode.SLEEPING: scenes.KITCHEN_NIGHTLIGHT,
                })
            case activities.Kitchen.COOKING:
                return scenes.KITCHEN_COOK

        return scene.off()

    def on_activity_change(self, activity: activities.Activity) -> None:
        match activity:
            case activities.Kitchen.COOKING:
                if not self.is_on(self.speakers):
                    self.music.play(Playlist.random())
