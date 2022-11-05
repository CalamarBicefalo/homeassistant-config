import activities
import entities
import helpers
from scenes_controller.scene_app import SceneApp


class LivingRoomScene(SceneApp):

    def set_light_scene(self, activity: activities.LivingRoom):
        if activity == activities.LivingRoom.READING:
            self.turn_on(entities.SCENE_LIVING_ROOM_READING)
        if activity == activities.LivingRoom.WATCHING_TV:
            self.turn_on(entities.SCENE_LIVING_ROOM_MOVIE)
        if activity == activities.LivingRoom.PRESENT:
            self.turn_on(entities.SCENE_LIVING_ROOM_WELCOME)

    def turn_off_lights(self):
        self.turn_off(entities.LIGHT_LIVING_ROOM)

    @property
    def activity_helper(self):
        return helpers.LIVING_ROOM_ACTIVITY

    @property
    def illuminance_sensor(self) -> entities.Entity:
        return entities.SENSOR_DESK_MS_ILLUMINANCE

