from datetime import datetime, timedelta
from typing import Any

import activities
import entities
import states
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
        needs_maintenance = self.flick.last_maintenance() < self.flick.last_cleaned_flat()
        is_not_cleaning = datetime.now() - timedelta(minutes=60) > self.flick.last_cleaned_flat()
        if needs_maintenance and is_not_cleaning:
            self.flick.go_to_maintenance_spot()
