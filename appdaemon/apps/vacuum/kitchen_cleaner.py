from datetime import datetime

import activities
import devices
import helpers
import services
import vacuum_location
from app import App


class KitchenCleaner(App):
    __cleaning_scheduled = False

    def initialize(self):
        time = "22:30:00"
        self.log(f'Initializing kitchen clean at {time}.', level="TRACE")
        self.run_daily(
            self.clean_kitchen,
            time
        )
        self.listen_state(
            self.clean_kitchen_if_scheduled,
            helpers.KITCHEN_ACTIVITY,
            new=activities.AWAY
        )

    async def clean_kitchen(self, kwargs):
        last_cooked = self.helper_to_datetime(helpers.LAST_COOKED)
        last_vacuumed = self.helper_to_datetime(helpers.LAST_CLEANED_KITCHEN)

        if last_vacuumed > last_cooked:
            self.log(
                f'Ignoring kitchen clean because we have not cooked for {(datetime.now() - last_cooked).days} '
                f'days, and we vacuumed on {self.datetime_to_helper(last_vacuumed)}.',
                level="INFO"
            )
            return

        self.__cleaning_scheduled = True
        await self.clean_kitchen_if_scheduled(kwargs)

    async def clean_kitchen_if_scheduled(self, kwargs):
        self.log('Cleaning kitchen', level="TRACE")
        if not (await self.is_activity(helpers.LIVING_ROOM_ACTIVITY, activities.AWAY)):
            self.log(
                f'Postponing clean until nobody is around',
                level="INFO"
            )
            return
        if self.__cleaning_scheduled:
            self.__cleaning_scheduled = False
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
