import activities
import entities
import helpers
from scenes_controller.scene_app import SceneApp


class StudioScene(SceneApp):
    activity_helper = helpers.STUDIO_ACTIVITY
    illuminance_sensor = entities.SENSOR_DESK_MS_ILLUMINANCE

    def set_light_scene(self, activity: activities.Activity):
        if activity == activities.Studio.WORKING:
            self.turn_on(entities.SCENE_STUDIO_WORKING)
        if activity == activities.Studio.DRUMMING:
            self.turn_on(entities.SCENE_STUDIO_DRUMMING)
        if activity == activities.Studio.PRESENT:
            self.turn_on(entities.SCENE_STUDIO_CONCENTRATE)

    def on_activity_change(self, activity: activities.Activity):
        if activity == activities.Studio.WORKING:
            self.turn_on(entities.SWITCH_MONITOR_PLUG)
        else:
            self.turn_off(entities.SWITCH_MONITOR_PLUG)

    def turn_off_lights(self):
        self.turn_off(entities.LIGHT_STUDIO)
