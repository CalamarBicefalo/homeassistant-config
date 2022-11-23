import activities
import entities
from scenes import scene
from scenes.scene import Scene
from scenes.scene_app import SceneApp


class HallwayScene(SceneApp):
    activity = activities.Hallway
    illuminance_sensor = entities.SENSOR_HALLWAY_MS_ILLUMINANCE
    room_lights = entities.LIGHT_HALLWAY

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.Hallway.PRESENT:
            return scene.of(entities.SCENE_HALLWAY_BRIGHT)
        return scene.none()
