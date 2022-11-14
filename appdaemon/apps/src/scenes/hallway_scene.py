import activities
import entities
import helpers
from scenes.scene_app import SceneApp


class HallwayScene(SceneApp):
    activity_helper = helpers.HALLWAY_ACTIVITY
    illuminance_sensor = entities.SENSOR_HALLWAY_MS_ILLUMINANCE
    room_lights = entities.LIGHT_HALLWAY

    def get_light_scene(self, activity: activities.Activity):
        if activity == activities.Hallway.PRESENT:
            return entities.SCENE_HALLWAY_BRIGHT

