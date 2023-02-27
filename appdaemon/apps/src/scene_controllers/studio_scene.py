import activities
import entities
import scenes
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp
from utils.select_handler import SelectHandler


class StudioScene(SceneApp):
    @property
    def activity(self) -> SelectHandler:
        return self.activities.studio

    illuminance_sensor = entities.SENSOR_DESK_MS_ILLUMINANCE
    room_lights = entities.LIGHT_STUDIO

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        match activity:
            case activities.Studio.WORKING:
                return scenes.STUDIO_WORKING
            case activities.Studio.DRUMMING:
                return scenes.STUDIO_DRUMMING
            case activities.Studio.PRESENT:
                return scenes.STUDIO_CONCENTRATE
        return scene.off()

    def on_activity_change(self, activity: activities.Activity) -> None:
        match activity:
            case activities.Studio.WORKING:
                self.turn_on(entities.SWITCH_MONITOR_PLUG)
            case activities.Studio.DRUMMING:
                self.turn_off_media()
            case _:
                self.turn_off(entities.SWITCH_MONITOR_PLUG)
