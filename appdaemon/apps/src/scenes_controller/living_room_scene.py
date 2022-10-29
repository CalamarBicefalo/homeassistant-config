import activities
import entities
import helpers
from app import App


class LivingRoomScene(App):

    def initialize(self):
        self.log(f'Initializing living room scene.', level="DEBUG")
        self.listen_state(
            self.set_living_room_scene,
            helpers.LIVING_ROOM_ACTIVITY
        )
        self.listen_state(
            self.set_living_room_scene,
            entities.SENSOR_DESK_MS_ILLUMINANCE
        )

    async def set_living_room_scene(self, entity, attribute, old, new, kwargs):
        self.log(f'Changing living room scene {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        activity = await self.get_activity_value(helpers.LIVING_ROOM_ACTIVITY)
        if activity == activities.LivingRoom.EMPTY.value:
            self.turn_off(entities.LIGHT_LIVING_ROOM)

        if float(await self.get_state(entities.SENSOR_DESK_MS_ILLUMINANCE)) < 40:
            if activity == activities.LivingRoom.READING.value:
                self.turn_on(entities.SCENE_LIVING_ROOM_READING)
            if activity == activities.LivingRoom.WATCHING_TV.value:
                self.turn_on(entities.SCENE_LIVING_ROOM_MOVIE)
            if activity == activities.LivingRoom.PRESENT.value:
                self.turn_on(entities.SCENE_LIVING_ROOM_WELCOME)
        else:
            self.turn_off(entities.LIGHT_LIVING_ROOM)
