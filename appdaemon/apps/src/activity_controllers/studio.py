import activities
import devices
import helpers
from app import App


class StudioActivity(App):

    def initialize(self):
        self.log(f'Initializing studio activity controller.', level="DEBUG")

        self.listen_state(
            self.studio_activity_controller,
            devices.STUDIO_MOTION
        )

        self.listen_state(
            self.studio_activity_controller,
            devices.STUDIO_CHAIR_PRESSURE
        )

        self.listen_state(
            self.studio_activity_controller,
            devices.DRUM_POWER_METER
        )

    async def studio_activity_controller(self, entity, attribute, old, new, kwargs):
        self.log("Triggering studio activity controller", level="DEBUG")

        # Work handling
        if await self.is_on(devices.STUDIO_CHAIR_PRESSURE):
            self.set_activity(helpers.STUDIO_ACTIVITY, activities.Studio.WORKING)
            return

        # Drum handling
        if await self.is_consuming_at_least(devices.DRUM_POWER_METER, watts=4):
            self.set_activity(helpers.STUDIO_ACTIVITY, activities.Studio.DRUMMING)
            return

        # Presence handling
        if await self.is_on(devices.STUDIO_MOTION):
            self.set_activity(helpers.STUDIO_ACTIVITY, activities.Studio.PRESENT)
        else:
            self.set_activity(helpers.STUDIO_ACTIVITY, activities.Studio.EMPTY)
