import activities
import entities
import helpers
from app import App


class StudioActivity(App):

    def initialize(self):
        self.log(f'Initializing studio activity controller.', level="DEBUG")

        self.listen_state(
            self.studio_activity_controller,
            entities.BINARY_SENSOR_STUDIO_MOTION
        )

        self.listen_state(
            self.studio_activity_controller,
            entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER
        )

        self.listen_state(
            self.studio_activity_controller,
            entities.SENSOR_DRUMS_PLUG_POWER
        )

    async def studio_activity_controller(self, entity, attribute, old, new, kwargs):
        self.log(f'Triggering studio activity controller {entity} -> {attribute} old={old} new={new}', level="DEBUG")

        # Work handling
        if await self.is_on(entities.BINARY_SENSOR_WORK_CHAIR_PS_WATER):
            self.set_activity(helpers.STUDIO_ACTIVITY, activities.Studio.WORKING)
            return

        # Drum handling
        if await self.is_consuming_at_least(entities.SENSOR_DRUMS_PLUG_POWER, watts=4):
            self.set_activity(helpers.STUDIO_ACTIVITY, activities.Studio.DRUMMING)
            return

        # Presence handling
        if await self.is_on(entities.BINARY_SENSOR_STUDIO_MOTION):
            self.set_activity(helpers.STUDIO_ACTIVITY, activities.Studio.PRESENT)
        else:
            self.set_activity(helpers.STUDIO_ACTIVITY, activities.Studio.EMPTY)
