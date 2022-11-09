import activities
import entities
import helpers
from scenes.scene_app import SceneApp


class EnsuiteScene(SceneApp):
    activity_helper = helpers.ENSUITE_ACTIVITY
    illuminance_sensor = None
    room_lights = entities.LIGHT_BATHROOM

    def get_light_scene(self, activity: activities.Activity):
        if activity == activities.Ensuite.PRESENT:
            return entities.SCENE_BATHROOM_CONCENTRATE

