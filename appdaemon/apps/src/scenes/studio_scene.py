import activities
import entities
from scenes import scene
from scenes.scene import Scene
from scenes.scene_app import SceneApp


class StudioScene(SceneApp):
    activity = activities.Studio
    illuminance_sensor = entities.SENSOR_DESK_MS_ILLUMINANCE
    room_lights = entities.LIGHT_STUDIO

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.Studio.WORKING:
            return scene.of(entities.SCENE_STUDIO_WORKING)
        if activity == activities.Studio.DRUMMING:
            return scene.of(entities.SCENE_STUDIO_DRUMMING)
        if activity == activities.Studio.PRESENT:
            return scene.of(entities.SCENE_STUDIO_CONCENTRATE)
        return scene.none()

    def on_activity_change(self, activity: activities.Activity) -> None:
        if activity == activities.Studio.WORKING:
            self.turn_on(entities.SWITCH_MONITOR_PLUG)
        else:
            self.turn_off(entities.SWITCH_MONITOR_PLUG)
