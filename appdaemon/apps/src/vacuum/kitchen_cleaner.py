from datetime import datetime
from typing import Any

import activities
import flick
import helpers
from app import App


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
            self.activities.livingroom._helper,
            new=activities.LivingRoom.EMPTY
        )

    def clean_kitchen_daily(self, kwargs: Any) -> None:
        self.clean_kitchen("scheduler", datetime.now(), None, None, None)

    def clean_kitchen(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(f'Triggering kitchen clean {entity} -> {attribute} old={old} new={new}', level="DEBUG")

        last_cooked = helpers.helper_to_datetime(self.get_state(helpers.LAST_COOKED))
        last_vacuumed = self.flick.last_cleaned_kitchen()

        if last_vacuumed > last_cooked:
            self.log(
                f'Ignoring kitchen clean because we have not cooked for {(datetime.now() - last_cooked).days} '
                f'days, and we vacuumed on {last_vacuumed}.',
                level="INFO"
            )
            return

        hours_since_last_clean = (datetime.now() - last_vacuumed).total_seconds() // 3600
        if hours_since_last_clean < 20 or datetime.now().hour < 21:
            self.log(
                f'Ignoring kitchen clean because we cleaned {hours_since_last_clean} ago',
                level="INFO"
            )
            return

        if not self.activities.livingroom.get() == activities.LivingRoom.EMPTY \
                or not self.activities.kitchen.get() == activities.Kitchen.EMPTY \
                or not self.activities.studio.get() == activities.Studio.EMPTY:
            self.log(
                f'Postponing clean until nobody is around',
                level="INFO"
            )
            return

        self.log('Cleaning kitchen', level="DEBUG")
        self.flick.clean_room(flick.Room.kitchen)
