from datetime import datetime

import activities, devices, helpers, services, vacuum_location, helpers
from hass import Hass


class MopMaintenance(Hass):

    def initialize(self):
        self.log(f'Initializing mop maintenance.', level="INFO")
        self.listen_state(
            self.start_mop_maintenance,
            helpers.KITCHEN_ACTIVITY,
            old=activities.AWAY,
            new=activities.PRESENT
        )

    async def start_mop_maintenance(self):
        self.log("Triggering mop maintenance routine")
        last_cleaned_kitchen = self.helper_to_datetime(apps.constants.helpers.LAST_CLEANED_KITCHEN)
        last_cleaned_vacuum_mop = self.helper_to_datetime(apps.constants.helpers.LAST_CLEANED_VACUUM_MOP)

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
