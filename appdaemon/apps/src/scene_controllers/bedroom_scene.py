import activities
import entities
import scenes
from modes import Mode
from scene_controllers import scene
from scene_controllers.scene import SceneSelector, Scene
from scene_controllers.scene_app import SceneApp


class BedroomScene(SceneApp):
    activity = activities.Bedroom
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM

    def get_light_scene(self, activity: activities.Activity) -> SceneSelector | Scene:
        if activity == activities.Bedroom.PRESENT:
            return scene.by_mode({
                Mode.DAY: scenes.BEDROOM_BRIGHT,
                Mode.NIGHT: scenes.BEDROOM_NIGHTLIGHT,
                Mode.BEDTIME: scenes.BEDROOM_GENTLE_READING,
                Mode.AWAY: scene.off(),
                Mode.SLEEPING: scene.off()
            })
        return scene.off()
