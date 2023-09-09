from datetime import datetime
from typing import Any

import helpers
from app import App
from rooms import *


class KitchenCleaner(App):

    def initialize(self) -> None:
        time = "22:30:00"
        self.log(f'Initializing kitchen clean at {time}.', level="DEBUG")
        self.run_daily(
            self.clean_kitchen_daily,
            time
        )
        self.listen_state(
            self.clean_kitchen,
            self.handlers.rooms.living_room.activity._helper,
            new=LivingRoom.Activity.EMPTY
        )

    def clean_kitchen_daily(self, kwargs: Any) -> None:
        self.clean_kitchen("scheduler", datetime.now(), None, None, None)

    def clean_kitchen(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(f'Triggering kitchen clean {entity} -> {attribute} old={old} new={new}', level="DEBUG")

        last_cooked = self.state.get_as_datetime(helpers.LAST_COOKED)
        last_vacuumed = self.handlers.rooms.kitchen.last_cleaned()

        if last_vacuumed > last_cooked:
            self.log(
                f'Ignoring kitchen clean because we have not cooked for {(datetime.now() - last_cooked).days} '
                f'days, and we vacuumed on {last_vacuumed}.',
                level="INFO"
            )
            return

        hours_since_last_clean = (datetime.now() - last_vacuumed).total_seconds() // 3600
        if hours_since_last_clean < 20:
            self.log(
                f'Ignoring kitchen clean because we cleaned {hours_since_last_clean} hours ago',
                level="INFO"
            )
            return

        if datetime.now().hour < 21:
            self.log(
                f'Ignoring kitchen clean because it is too early on the day, we will clean at by 21:00',
                level="INFO"
            )
            return

        if not self.handlers.rooms.living_room.activity.get() == LivingRoom.Activity.EMPTY \
                or not self.handlers.rooms.kitchen.activity.get() == Kitchen.Activity.EMPTY \
                or not self.handlers.rooms.studio.activity.get() == Studio.Activity.EMPTY:
            self.log(
                f'Postponing clean until nobody is around',
                level="INFO"
            )
            return

        self.log(f'Cleaning kitchen because it was last cleaned on {last_vacuumed}', level="INFO")
        self.handlers.rooms.kitchen.clean()
