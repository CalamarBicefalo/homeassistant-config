import activities
import entities
import helpers
from scenes_controller.scene_app import SceneApp


class EnsuiteScene(SceneApp):
    activity_helper = helpers.ENSUITE_ACTIVITY
    illuminance_sensor = None
    room_lights = entities.LIGHT_BATHROOM

    def set_light_scene(self, activity: activities.Activity):
        if activity == activities.Ensuite.PRESENT:
            self.turn_on(entities.SCENE_BATHROOM_CONCENTRATE)

