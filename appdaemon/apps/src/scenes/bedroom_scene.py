import activities
import entities
from scenes.scene_app import SceneApp


class BedroomScene(SceneApp):
    activity = activities.Bedroom
    illuminance_sensor = entities.SENSOR_BEDROOM_MS_ILLUMINANCE
    room_lights = entities.LIGHT_BEDROOM

    def get_light_scene(self, activity: activities.Activity):
        if activity == activities.Bedroom.PRESENT:
            return entities.SCENE_BEDROOM_BRIGHT

