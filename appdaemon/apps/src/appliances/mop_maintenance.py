from datetime import datetime, timedelta
from typing import Any

import entities
import states
from app import App
from rooms import *


class MopMaintenance(App):

    def initialize(self) -> None:
        self.log(f'Initializing mop maintenance.', level="DEBUG")
        self.listen_state(
            self.start_mop_maintenance,
            self.handlers.rooms.kitchen.activity._helper,
            old=Kitchen.Activity.EMPTY,
            new=Kitchen.Activity.PRESENT
        )

    def start_mop_maintenance(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        if self.state.is_value(entities.VACUUM_FLICK, states.CLEANING):
            return

        self.log(f'Triggering mop maintenance routine {entity} -> {attribute} old={old} new={new}', level="DEBUG")
        is_not_cleaning = datetime.now() - timedelta(minutes=60) > self.handlers.flick.last_cleaned_flat()
        if self.handlers.flick.needs_maintenance() and is_not_cleaning:
            self.handlers.flick.go_to_maintenance_spot()
            self.handlers.notifications.chore("Flick needs you 🐜🧹", "Greetings fellow human, my name is flick and I need your help! Empty my dustbin, replace my mop, and give me some fresh water")
