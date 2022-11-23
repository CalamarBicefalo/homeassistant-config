import activities
import entities
from scenes import scene
from scenes.scene import Scene
from scenes.scene_app import SceneApp


class LivingRoomScene(SceneApp):
    activity = activities.LivingRoom
    illuminance_sensor = entities.SENSOR_DESK_MS_ILLUMINANCE
    room_lights = entities.LIGHT_LIVING_ROOM

    def get_light_scene(self, activity: activities.Activity) -> Scene:
        if activity == activities.LivingRoom.READING:
            return scene.of(entities.SCENE_LIVING_ROOM_READING)
        if activity == activities.LivingRoom.WATCHING_TV:
            return scene.of(entities.SCENE_LIVING_ROOM_MOVIE)
        if activity == activities.LivingRoom.PRESENT:
            return scene.of(entities.SCENE_LIVING_ROOM_WELCOME)

        return scene.none()



