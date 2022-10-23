from datetime import datetime

import activities
import devices
import helpers
import services
import vacuum_location
from app import App


class KitchenCleaner(App):

    def initialize(self):
        time = "22:30:00"
        self.log(f'Initializing kitchen clean at {time}.', level="INFO")
        self.run_daily(
            self.clean_kitchen,
            time
        )

    async def clean_kitchen(self, kwargs):
        self.log("Triggering kitchen clean task", level="INFO")
        last_cooked = self.helper_to_datetime(helpers.LAST_COOKED)
        days_since_kitchen_got_dirty = datetime.now() - last_cooked
        if days_since_kitchen_got_dirty.days == 0:
            attempts = 0
            while self.get_state(helpers.LIVING_ROOM_ACTIVITY) == activities.WATCHING_TV and attempts < 12:
                self.log('TV is on, waiting until it is off', level="INFO")
                attempts += 1
                await self.sleep(10 * 60)
            self.log('Cleaning kitchen', level="INFO")
            self.call_service(
                services.VACUUM_CLEAN_SEGMENT,
                entity_id=devices.VACUUM_CLEANER,
                segments=vacuum_location.kitchen_segment
            )
            self.call_service(
                services.HELPER_DATETIME_SET,
                entity_id=helpers.LAST_CLEANED_KITCHEN,
                datetime=self.datetime_to_helper(datetime.now())
            )
        else:
            self.log(f'Ignoring kitchen clean because we have not cooked for {days_since_kitchen_got_dirty} days.',
                     level="INFO")
