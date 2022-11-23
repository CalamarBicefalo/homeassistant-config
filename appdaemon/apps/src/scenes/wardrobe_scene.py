import activities
import entities
from scenes import scene
from scenes.scene import Scene
from scenes.scene_app import SceneApp


class WardrobeScene(SceneApp):
    activity = activities.Wardrobe
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_ILLUMINANCE
    room_lights = entities.LIGHT_WARDROBE

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.Wardrobe.PRESENT:
            return scene.of(entities.SCENE_WARDROBE_BRIGHT)
        return scene.none()
