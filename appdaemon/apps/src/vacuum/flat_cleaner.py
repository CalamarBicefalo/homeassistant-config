from datetime import datetime
from typing import Any

import entities
import helpers
import modes
import services
from app import App


class FlatCleaner(App):

    def initialize(self) -> None:
        self.listen_state(
            self.clean_flat,
            helpers.HOMEASSISTANT_MODE,
            new=modes.Mode.AWAY,
        )

    def clean_flat(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(f'Triggering flat clean {entity} -> {attribute} old={old} new={new}', level="DEBUG")

        last_vacuumed = self.helper_to_datetime(helpers.LAST_CLEANED_FLAT)

        days_since_last_clean = (datetime.now() - last_vacuumed).days
        if days_since_last_clean < 4:
            self.log(
                f'Ignoring flat clean because we cleaned {days_since_last_clean} days ago',
                level="INFO"
            )
            return

        self.__do_clean__(kwargs)

    def __do_clean__(self, kwargs: Any) -> None:
        self.log('Cleaning flat', level="DEBUG")
        self.call_service(
            services.VACUUM_START,
            entity_id=entities.VACUUM_FLICK,
        )
        self.call_service(
            services.INPUT_DATETIME_SET_DATETIME,
            entity_id=helpers.LAST_CLEANED_FLAT,
            datetime=self.datetime_to_helper(datetime.now())
        )
