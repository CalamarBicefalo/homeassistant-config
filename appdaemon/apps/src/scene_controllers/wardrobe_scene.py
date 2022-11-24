import activities
import entities
import scenes
from modes import Mode
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene
from scene_controllers.scene_app import SceneApp


class WardrobeScene(SceneApp):
    activity = activities.Wardrobe
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_ILLUMINANCE
    room_lights = entities.LIGHT_WARDROBE

    def get_light_scene(self, activity: activities.Activity) -> Scene | SceneSelector:
        if activity == activities.Wardrobe.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.WARDROBE_BRIGHT,
                Mode.NIGHT: scenes.WARDROBE_NIGHTLIGHT,
                Mode.BEDTIME: scenes.WARDROBE_NIGHTLIGHT,
                Mode.AWAY: scene.off(),
                Mode.SLEEPING: scene.off(),
            })
        return scene.off()
