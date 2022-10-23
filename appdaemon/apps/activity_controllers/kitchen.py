import activities
import devices
import helpers
from hass import Hass


class KitchenActivity(Hass):

    def initialize(self):
        self.log(f'Initializing kitchen activity controller.', level="INFO")

        self.listen_state(
            self.kitchen_activity_controller,
            devices.KITCHEN_MOTION
        )

    async def kitchen_activity_controller(self):
        self.log("Triggering kitchen activity controller")

        # Presence handling
        if self.is_on(devices.KITCHEN_MOTION):
            self.set_activity(helpers.KITCHEN_ACTIVITY, activities.PRESENT)
        else:
            self.set_activity(helpers.KITCHEN_ACTIVITY, activities.AWAY)
