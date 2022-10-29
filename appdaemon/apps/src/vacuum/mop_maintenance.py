from datetime import datetime

import activities
import entities
import helpers
import services
from app import App


class MopMaintenance(App):

    def initialize(self):
        self.log(f'Initializing mop maintenance.', level="DEBUG")
        self.listen_state(
            self.start_mop_maintenance,
            helpers.KITCHEN_ACTIVITY,
            old=activities.Kitchen.EMPTY,
            new=activities.Kitchen.PRESENT
        )

    async def start_mop_maintenance(self):
        self.log("Triggering mop maintenance routine", level="DEBUG")
        last_cleaned_kitchen = await self.helper_to_datetime(helpers.LAST_CLEANED_KITCHEN)
        last_cleaned_vacuum_mop = await self.helper_to_datetime(helpers.LAST_CLEANED_VACUUM_MOP)

        if last_cleaned_vacuum_mop < last_cleaned_kitchen:
            self.call_service(
                services.XIAOMI_MIIO_VACUUM_GOTO,
                entity_id=entities.VACUUM_ROBOROCK_VACUUM_A15,
                x_coord=mop_maintenance.x,
                y_coord=mop_maintenance.y
            )
            self.call_service(
                services.INPUT_DATETIME_SET_DATETIME,
                entity_id=helpers.LAST_CLEANED_VACUUM_MOP,
                datetime=self.datetime_to_helper(datetime.now())
            )


class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


mop_maintenance = Point(24900, 22200)
