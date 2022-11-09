import activities
import entities
import helpers
from scenes_controller.scene_app import SceneApp


class LivingRoomScene(SceneApp):
    activity_helper = helpers.LIVING_ROOM_ACTIVITY
    illuminance_sensor = entities.SENSOR_DESK_MS_ILLUMINANCE
    room_lights = entities.LIGHT_LIVING_ROOM

    def get_light_scene(self, activity: activities.LivingRoom):
        if activity == activities.LivingRoom.READING:
            return entities.SCENE_LIVING_ROOM_READING
        if activity == activities.LivingRoom.WATCHING_TV:
            return entities.SCENE_LIVING_ROOM_MOVIE
        if activity == activities.LivingRoom.PRESENT:
            return entities.SCENE_LIVING_ROOM_WELCOME



