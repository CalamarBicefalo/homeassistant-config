import activities
import devices
import helpers
import scenes
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
            devices.STUDIO_ILLUMINANCE
        )

    async def set_living_room_scene(self, entity, attribute, old, new, kwargs):
        if await self.is_activity(helpers.LIVING_ROOM_ACTIVITY, activities.LivingRoom.EMPTY):
            self.turn_off(devices.LIVING_ROOM_LIGHTS)

        if await self.get_state(devices.STUDIO_ILLUMINANCE) < 40:
            if await self.is_activity(helpers.LIVING_ROOM_ACTIVITY, activities.LivingRoom.READING):
                self.turn_on(scenes.LIVING_ROOM_READING)
            if await self.is_activity(helpers.LIVING_ROOM_ACTIVITY, activities.LivingRoom.WATCHING_TV):
                self.turn_on(scenes.LIVING_ROOM_MOVIE)
            if await self.is_activity(helpers.LIVING_ROOM_ACTIVITY, activities.LivingRoom.PRESENT):
                self.turn_on(scenes.LIVING_ROOM_WELCOME)
