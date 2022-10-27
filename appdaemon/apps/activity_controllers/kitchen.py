import activities
import devices
import helpers
from app import App


class KitchenActivity(App):

    def initialize(self):
        self.log(f'Initializing kitchen activity controller.', level="DEBUG")

        self.listen_state(
            self.kitchen_activity_controller,
            devices.KITCHEN_MOTION
        )

    async def kitchen_activity_controller(self, entity, attribute, old, new, kwargs):
        self.log("Triggering kitchen activity controller", level="DEBUG")
        # Presence handling
        if await self.is_on(devices.KITCHEN_MOTION):
            self.set_activity(helpers.KITCHEN_ACTIVITY, activities.PRESENT)
        else:
            self.set_activity(helpers.KITCHEN_ACTIVITY, activities.AWAY)
