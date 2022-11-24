import activities
import entities
import scenes
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp


class HallwayScene(SceneApp):
    activity = activities.Hallway
    illuminance_sensor = entities.SENSOR_HALLWAY_MS_ILLUMINANCE
    room_lights = entities.LIGHT_HALLWAY

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.Hallway.PRESENT:
            return scenes.HALLWAY_BRIGHT
        return scene.off()
