import activities
import entities
import scenes
from scene_controllers import scene
from scene_controllers.scene import Scene
from scene_controllers.scene_app import SceneApp


class LivingRoomScene(SceneApp):
    activity = activities.LivingRoom
    illuminance_sensor = entities.SENSOR_DESK_MS_ILLUMINANCE
    room_lights = entities.LIGHT_LIVING_ROOM

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.LivingRoom.READING:
            return scenes.LIVING_ROOM_READING
        if activity == activities.LivingRoom.WATCHING_TV:
            return scenes.LIVING_ROOM_MOVIE
        if activity == activities.LivingRoom.PRESENT:
            return scenes.LIVING_ROOM_WELCOME

        return scene.off()



