from datetime import datetime, timedelta
from typing import Any

import activities
import entities
import helpers
import services
from utils import states
from app import App


class MopMaintenance(App):

    def initialize(self) -> None:
        self.log(f'Initializing mop maintenance.', level="DEBUG")
        self.listen_state(
            self.start_mop_maintenance,
            self.activities.kitchen._helper,
            old=activities.Kitchen.EMPTY,
            new=activities.Kitchen.PRESENT
        )

    def start_mop_maintenance(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.has_state(entities.VACUUM_FLICK, states.CLEANING):
            return

        self.log(f'Triggering mop maintenance routine {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        last_cleaned_kitchen = self.helper_to_datetime(helpers.LAST_CLEANED_FLAT)
        last_cleaned_vacuum_mop = self.helper_to_datetime(helpers.LAST_CLEANED_VACUUM_MOP)

        mop_is_dirty = last_cleaned_vacuum_mop < last_cleaned_kitchen
        is_not_cleaning = datetime.now() - timedelta(minutes=60) > last_cleaned_kitchen
        if mop_is_dirty and is_not_cleaning:
            self.call_service(
                services.VACUUM_SEND_COMMAND,
                entity_id=entities.VACUUM_FLICK,
                command="app_goto_target",
                params=[mop_maintenance.x, mop_maintenance.y]
            )
            self.call_service(
                services.INPUT_DATETIME_SET_DATETIME,
                entity_id=helpers.LAST_CLEANED_VACUUM_MOP,
                datetime=self.datetime_to_helper(datetime.now())
            )


class Point:
    def __init__(self, x_init: int, y_init: int) -> None:
        self.x = x_init
        self.y = y_init

    def __repr__(self) -> str:
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


mop_maintenance = Point(24900, 22200)
