from datetime import datetime

import activities
import devices
import helpers
import services
import vacuum_location
from app import App


class MopMaintenance(App):

    def initialize(self):
        self.log(f'Initializing mop maintenance.', level="DEBUG")
        self.listen_state(
            self.start_mop_maintenance,
            helpers.KITCHEN_ACTIVITY,
            old=activities.EMPTY,
            new=activities.PRESENT
        )

    async def start_mop_maintenance(self):
        self.log("Triggering mop maintenance routine", level="DEBUG")
        last_cleaned_kitchen = await self.helper_to_datetime(helpers.LAST_CLEANED_KITCHEN)
        last_cleaned_vacuum_mop = await self.helper_to_datetime(helpers.LAST_CLEANED_VACUUM_MOP)

        if last_cleaned_vacuum_mop < last_cleaned_kitchen:
            self.call_service(
                services.VACUUM_GO_TO,
                entity_id=devices.VACUUM_CLEANER,
                x_coord=vacuum_location.mop_maintenance.x,
                y_coord=vacuum_location.mop_maintenance.y
            )
            self.call_service(
                services.HELPER_DATETIME_SET,
                entity_id=helpers.LAST_CLEANED_VACUUM_MOP,
                datetime=self.datetime_to_helper(datetime.now())
            )
