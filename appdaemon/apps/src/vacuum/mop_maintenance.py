from datetime import datetime, timedelta

import activities
import entities
import helpers
import services
from utils.app import App


class MopMaintenance(App):

    def initialize(self):
        self.log(f'Initializing mop maintenance.', level="DEBUG")
        self.listen_state(
            self.start_mop_maintenance,
            activities.Kitchen.helper,
            old=activities.Kitchen.EMPTY,
            new=activities.Kitchen.PRESENT
        )

    def start_mop_maintenance(self, entity, attribute, old, new, kwargs):
        self.log(f'Triggering mop maintenance routine {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        last_cleaned_kitchen = self.helper_to_datetime(helpers.LAST_CLEANED_KITCHEN)
        last_cleaned_vacuum_mop = self.helper_to_datetime(helpers.LAST_CLEANED_VACUUM_MOP)

        mop_is_dirty = last_cleaned_vacuum_mop < last_cleaned_kitchen
        is_not_cleaning = datetime.now() - timedelta(minutes=60) > last_cleaned_kitchen
        if mop_is_dirty and is_not_cleaning:
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
