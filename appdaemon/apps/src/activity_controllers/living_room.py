import activities
import entities
import helpers
from app import App


class LivingRoomActivity(App):

    def initialize(self):
        self.log(f'Initializing living room activity controller.', level="DEBUG")

        self.listen_state(
            self.living_room_activity_controller,
            [
                entities.BINARY_SENSOR_LIVING_ROOM_MOTION,
                entities.MEDIA_PLAYER_TV
            ]
        )

    async def living_room_activity_controller(self, entity, attribute, old, new, kwargs):
        self.log(f'Triggering living room activity controller {entity} -> {attribute} old={old} new={new}', level="DEBUG")

        # TV handling
        if await self.is_on(entities.MEDIA_PLAYER_TV):
            self.set_activity(helpers.LIVING_ROOM_ACTIVITY, activities.LivingRoom.WATCHING_TV)
            return

        # Presence handling
        if await self.is_on(entities.BINARY_SENSOR_LIVING_ROOM_MOTION):
            self.set_activity(helpers.LIVING_ROOM_ACTIVITY, activities.LivingRoom.PRESENT)
        else:
            self.set_activity(helpers.LIVING_ROOM_ACTIVITY, activities.LivingRoom.EMPTY)
