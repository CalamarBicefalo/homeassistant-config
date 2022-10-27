import activities
import devices
import helpers
import states
from app import App


class LivingRoomActivity(App):

    def initialize(self):
        self.log(f'Initializing living room activity controller.', level="DEBUG")

        self.listen_state(
            self.living_room_activity_controller,
            [
                devices.LIVING_ROOM_MOTION,
                devices.TV
            ]
        )

    async def living_room_activity_controller(self, entity, attribute, old, new, kwargs):
        self.log("Triggering living room activity controller", level="DEBUG")

        # TV handling
        if await self.is_on(devices.TV):
            self.set_activity(helpers.LIVING_ROOM_ACTIVITY, activities.WATCHING_TV)
            return

        # Presence handling
        if await self.is_on(devices.LIVING_ROOM_MOTION):
            self.set_activity(helpers.LIVING_ROOM_ACTIVITY, activities.PRESENT)
        else:
            self.set_activity(helpers.LIVING_ROOM_ACTIVITY, activities.AWAY)
