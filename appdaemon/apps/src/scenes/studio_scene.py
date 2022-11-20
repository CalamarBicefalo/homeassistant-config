import activities
import entities
from scenes.scene_app import SceneApp


class StudioScene(SceneApp):
    activity = activities.Studio
    illuminance_sensor = entities.SENSOR_DESK_MS_ILLUMINANCE
    room_lights = entities.LIGHT_STUDIO

    def get_light_scene(self, activity: activities.Activity):
        if activity == activities.Studio.WORKING:
            return entities.SCENE_STUDIO_WORKING
        if activity == activities.Studio.DRUMMING:
            return entities.SCENE_STUDIO_DRUMMING
        if activity == activities.Studio.PRESENT:
            return entities.SCENE_STUDIO_CONCENTRATE

    def on_activity_change(self, activity: activities.Activity):
        if activity == activities.Studio.WORKING:
            self.turn_on(entities.SWITCH_MONITOR_PLUG)
        else:
            self.turn_off(entities.SWITCH_MONITOR_PLUG)
