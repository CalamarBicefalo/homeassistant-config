import activities
import entities
from scenes import scene
from scenes.scene import Scene
from scenes.scene_app import SceneApp


class EnsuiteScene(SceneApp):
    activity = activities.Ensuite
    illuminance_sensor = None
    room_lights = entities.LIGHT_BATHROOM

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.Ensuite.PRESENT:
            return scene.of(entities.SCENE_BATHROOM_CONCENTRATE)
        return scene.none()
