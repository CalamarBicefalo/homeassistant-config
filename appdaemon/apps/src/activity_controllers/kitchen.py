import activities
import entities
import helpers
from app import App


class KitchenActivity(App):

    def initialize(self):
        self.log(f'Initializing kitchen activity controller.', level="DEBUG")

        self.listen_state(
            self.kitchen_activity_controller,
            entities.BINARY_SENSOR_KITCHEN_MOTION
        )

    async def kitchen_activity_controller(self, entity, attribute, old, new, kwargs):
        self.log("Triggering kitchen activity controller", level="DEBUG")
        # Presence handling
        if await self.is_on(entities.BINARY_SENSOR_KITCHEN_MOTION):
            self.set_activity(helpers.KITCHEN_ACTIVITY, activities.Kitchen.PRESENT)
        else:
            self.set_activity(helpers.KITCHEN_ACTIVITY, activities.Kitchen.EMPTY)
