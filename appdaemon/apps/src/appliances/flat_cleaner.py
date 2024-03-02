from datetime import datetime
from typing import Any

import helpers
import selects
from app import App


class FlatCleaner(App):

    def initialize(self) -> None:
        self.listen_state(
            self.clean_flat,
            helpers.MODE,
            new=selects.Mode.AWAY,
        )

    def clean_flat(self, entity: Any, attribute: Any, old: Any, new: Any, kwargs: Any) -> None:
        self.log(f'Triggering flat clean {entity} -> {attribute} old={old} new={new}', level="DEBUG")

        days_since_last_clean = (datetime.now() - self.handlers.flick.last_cleaned_flat()).days
        if days_since_last_clean < 4:
            self.log(
                f'Ignoring flat clean because we cleaned {days_since_last_clean} days ago',
                level="INFO"
            )
            return

        self.log('Cleaning flat', level="DEBUG")
        self.handlers.flick.clean_flat()
