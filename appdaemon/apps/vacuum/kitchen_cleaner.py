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
        self.log(f'Initializing kitchen clean at {time}.', level="DEBUG")
        self.run_daily(
            self.clean_kitchen,
            time
        )
        self.listen_state(
            self.clean_kitchen,
            helpers.KITCHEN_ACTIVITY,
            new=activities.EMPTY
        )

    async def clean_kitchen(self, kwargs):
        last_cooked = await self.helper_to_datetime(helpers.LAST_COOKED)
        last_vacuumed = await self.helper_to_datetime(helpers.LAST_CLEANED_KITCHEN)

        if last_vacuumed > last_cooked:
            self.log(
                f'Ignoring kitchen clean because we have not cooked for {(datetime.now() - last_cooked).days} '
                f'days, and we vacuumed on {self.datetime_to_helper(last_vacuumed)}.',
                level="INFO"
            )
            return

        hours_since_last_clean = (datetime.now() - last_vacuumed).total_seconds() // 3600
        if hours_since_last_clean < 20:
            self.log(
                f'Ignoring kitchen clean because we cleaned {hours_since_last_clean} ago',
                level="INFO"
            )
            return

        if not (await self.is_activity(helpers.LIVING_ROOM_ACTIVITY, activities.EMPTY)):
            self.log(
                f'Postponing clean until nobody is around',
                level="INFO"
            )
            return

        await self.__do_clean__(kwargs)

    async def __do_clean__(self, kwargs):
        self.log('Cleaning kitchen', level="DEBUG")
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
