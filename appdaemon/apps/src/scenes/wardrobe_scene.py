import activities
import entities
import helpers
from scenes.scene_app import SceneApp


class WardrobeScene(SceneApp):
    activity_helper = helpers.WARDROBE_ACTIVITY
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_ILLUMINANCE
    room_lights = entities.LIGHT_WARDROBE

    def get_light_scene(self, activity: activities.Activity):
        if activity == activities.Wardrobe.PRESENT:
            return entities.SCENE_WARDROBE_BRIGHT
